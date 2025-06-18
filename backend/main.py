#!/usr/bin/env python3
from __future__ import annotations
import os, sys, json, time, logging, subprocess, threading, atexit, tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional
from psycopg_pool import ConnectionPool
from apify_client import ApifyClient
from flask import Flask, request, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("main")

ROOT_DIR = Path(__file__).resolve().parent
TTS_SCRIPT   = ROOT_DIR / "tts_worker.py"
INTRO_SCRIPT = ROOT_DIR / "intro_worker.py"
IDLE_SCRIPT  = ROOT_DIR / "idle_player.py"

import os, sys
print("DBG:", {k: os.getenv(k) for k in ("DB_NAME", "DB_USER", "DB_PASSWORD")}, file=sys.stderr)

db_pool = ConnectionPool(
    conninfo=(
        f"dbname={os.getenv('DB_NAME')} "
        f"user={os.getenv('DB_USER')} "
        f"password={os.getenv('DB_PASSWORD')} "
        f"host={os.getenv('DB_HOST','localhost')} "
        f"port={os.getenv('DB_PORT','5432')}"
    ), min_size=1, max_size=10, timeout=30,
)

client = ApifyClient(os.getenv("APIFY_API_TOKEN"))
TWITTER_ACTOR_ID   = os.getenv("TWITTER_ACTOR_ID")
INSTAGRAM_ACTOR_ID = os.getenv("INSTAGRAM_ACTOR_ID")
FACEBOOK_ACTOR_ID  = os.getenv("FACEBOOK_ACTOR_ID")

FILTERING_ENABLED  = True
automation_enabled = True
global_platforms: List[str] = []

app = Flask(__name__)
CORS(app)

_worker_lock = threading.RLock()
_tts_proc:  Optional[subprocess.Popen] = None
_idle_proc: Optional[subprocess.Popen] = None
last_voice_activity = time.time()
SILENCE_BEFORE_IDLE = 20.0

def _stop_proc(proc: Optional[subprocess.Popen], name: str, timeout: int = 30):
    if not proc or proc.poll() is not None:
        return None
    proc.terminate()
    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill(); proc.wait()
    return None

def _stop_all_audio():
    global _tts_proc, _idle_proc
    with _worker_lock:
        _tts_proc  = _stop_proc(_tts_proc,  "tts_worker")
        _idle_proc = _stop_proc(_idle_proc, "idle_player")

def _start_idle():
    global _idle_proc, _tts_proc
    with _worker_lock:
        if _idle_proc and _idle_proc.poll() is None: return
        _tts_proc = _stop_proc(_tts_proc, "tts_worker")
        _idle_proc = subprocess.Popen(
            [sys.executable, str(IDLE_SCRIPT)],
            env=os.environ.copy(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

def _start_tts():
    global _tts_proc, _idle_proc
    with _worker_lock:
        if _tts_proc and _tts_proc.poll() is None: return
        _idle_proc = _stop_proc(_idle_proc, "idle_player")
        _tts_proc = subprocess.Popen(
            [sys.executable, str(TTS_SCRIPT)],
            env=os.environ.copy(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

def _run_intro_once():
    global last_voice_activity
    _stop_all_audio()
    subprocess.run([sys.executable, str(INTRO_SCRIPT)], env=os.environ.copy())
    last_voice_activity = time.time()

def _manager_loop():
    global last_voice_activity
    while True:
        time.sleep(1)
        with db_pool.connection() as c, c.cursor() as cur:
            cur.execute("SELECT EXISTS(SELECT 1 FROM intro_captions WHERE played = false)")
            intro_exists, = cur.fetchone()
            cur.execute("SELECT EXISTS(SELECT 1 FROM captions WHERE played = false)")
            tts_exists,   = cur.fetchone()
        if intro_exists:
            last_voice_activity = time.time()
            _run_intro_once()
        elif tts_exists:
            last_voice_activity = time.time()
            _start_tts()
        else:
            if time.time() - last_voice_activity >= SILENCE_BEFORE_IDLE:
                _start_idle()
            else:
                _stop_proc(_idle_proc, "idle_player")

threading.Thread(target=_manager_loop, daemon=True).start()

def get_hashtags() -> List[str]:
    with db_pool.connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT hashtag FROM hashtags")
        return [r[0] for r in cur.fetchall()]

def run_moderation_script(results: List[Dict[str, Any]]):
    moderation_path = ROOT_DIR / "moderation.py"
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".json") as tf:
        json.dump(results, tf)
        tmp = tf.name
    try:
        subprocess.run([sys.executable, str(moderation_path), tmp],
                       check=True, env=os.environ.copy())
    finally:
        try: os.remove(tmp)
        except FileNotFoundError: pass

def insert_direct(results: List[Dict[str, Any]]):
    with db_pool.connection() as conn, conn.cursor() as cur:
        for r in results:
            cur.execute(
                "INSERT INTO captions (hashtag, content, time_stamp)"
                " VALUES (%s,%s,%s)",
                (r["hashtag"], r["content"], r["time_stamp"]),
            )
        conn.commit()

def process_results(results: List[Dict[str, Any]]):
    (run_moderation_script if FILTERING_ENABLED else insert_direct)(results)
    cleanup = ROOT_DIR / "cleanup_audio.py"
    subprocess.run([sys.executable, str(cleanup)], check=False)

def scrape_facebook(tags: List[str]):
    out: List[Dict[str, Any]] = []
    for tag in tags:
        run = client.actor(FACEBOOK_ACTOR_ID).call(
            run_input={"searchQuery": tag, "maxItems": 10}, wait_secs=120)
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            out.append({
                "hashtag": tag, "platform": "facebook",
                "content": item.get("text", ""),
                "time_stamp": item.get("time"),
            })
    if out: process_results(out)

def scrape_facebook_async(tags: List[str]):
    threading.Thread(target=scrape_facebook, args=(tags,), daemon=True).start()

def run_scraping_job(hashtags: List[str], platforms: List[str]):
    results: List[Dict[str, Any]] = []
    for tag in hashtags:
        for platform in platforms:
            if platform == "facebook":
                scrape_facebook_async([tag]); continue
            actor_input = {
                "twitter":   {"searchTerms": [tag], "maxItems": 10, "sort": "Latest"},
                "instagram": {"hashtags":   [tag], "resultsLimit": 10, "resultsType": "posts"},
            }[platform]
            actor_id = {
                "twitter": TWITTER_ACTOR_ID,
                "instagram": INSTAGRAM_ACTOR_ID
            }[platform]
            run = client.actor(actor_id).call(run_input=actor_input, wait_secs=120)
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                results.append({
                    "hashtag": tag,
                    "platform": platform,
                    "content": item.get("fullText" if platform=="twitter" else "caption", ""),
                    "time_stamp": item.get("createdAt" if platform=="twitter" else "timestamp"),
                })
    if results: process_results(results)

def scheduled_scrape():
    if not automation_enabled or not global_platforms: return
    tags = get_hashtags()
    if not tags: return
    _stop_all_audio()
    run_scraping_job(tags, global_platforms)

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=scheduled_scrape,
    trigger=IntervalTrigger(minutes=10),
    id="scrape_job",
    name="Scheduled scrape",
    replace_existing=True,
)

@app.route("/filtering_on", methods=["POST"])
def filtering_on():
    global FILTERING_ENABLED
    _stop_all_audio()
    FILTERING_ENABLED = True
    return jsonify(filtering=True), 200

@app.route("/filtering_off", methods=["POST"])
def filtering_off():
    global FILTERING_ENABLED
    _stop_all_audio()
    FILTERING_ENABLED = False
    return jsonify(filtering=False), 200

@app.route("/stop-automation", methods=["POST"])
def stop_auto():
    global automation_enabled
    _stop_all_audio()
    automation_enabled = False
    return jsonify(automation="paused"), 200

@app.route("/start-automation", methods=["POST"])
def start_auto():
    global automation_enabled
    _stop_all_audio()
    automation_enabled = True
    return jsonify(automation="resumed"), 200

@app.route("/scrape", methods=["POST"])
def scrape():
    _stop_all_audio()
    data = request.get_json(force=True)
    platforms = data.get("platforms")
    tags = get_hashtags()
    if not tags: return jsonify(error="No hashtags in DB"), 400
    if not isinstance(platforms, list): return jsonify(error="Missing/invalid 'platforms'"), 400
    bad = [p for p in platforms if p not in ("twitter", "instagram", "facebook")]
    if bad: return jsonify(error=f"Invalid platform(s): {bad}"), 400
    global global_platforms
    global_platforms = platforms
    threading.Thread(target=run_scraping_job, args=(tags, platforms), daemon=True).start()
    return jsonify(message="Scrape job started"), 202

def _shutdown():
    _stop_all_audio()
    scheduler.shutdown()

atexit.register(_shutdown)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
