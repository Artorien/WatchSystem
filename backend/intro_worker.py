#!/usr/bin/env python3
from __future__ import annotations
import os, pathlib, sys, subprocess, shutil, time, logging
from typing import List, Tuple, Sequence
import psycopg as psycopg2
from dotenv import load_dotenv
import httpx
from openai import OpenAI, OpenAIError

load_dotenv()
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)-8s %(message)s")

ROOT_DIR    = pathlib.Path(__file__).resolve().parent
PLAY_LOCK   = ROOT_DIR / "tts_worker" / "tts_output" / ".playing.lock"
LOCK_TIMEOUT = float(os.getenv("PLAY_LOCK_TIMEOUT", "60"))
STALE_SEC    = float(os.getenv("PLAY_LOCK_STALE_SEC", "10"))

OUT_DIR = ROOT_DIR / "intro_output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DB = dict(
    dbname   = os.getenv("DB_NAME"),
    user     = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    host     = os.getenv("DB_HOST", "localhost"),
    port     = os.getenv("DB_PORT", "5432"),
)

VOICE          = os.getenv("VOICE_NAME", "alloy")
PRIMARY_MODEL  = os.getenv("INTRO_TTS_MODEL", "tts-1-hd")
FALLBACKS      = [m.strip() for m in os.getenv(
        "INTRO_TTS_FALLBACK_MODELS",
        "gpt-4o-mini-tts,tts-1,tts-1-1106,tts-1-hd-1106").split(",") if m.strip()]
MODEL_CHAIN: Sequence[str] = [PRIMARY_MODEL] + [
    m for m in FALLBACKS if m not in {PRIMARY_MODEL, ""}]

TTS_SPEED      = float(os.getenv("INTRO_TTS_SPEED", "1.0"))
AUDIO_FMT      = os.getenv("INTRO_TTS_FMT", "mp3")
FIRST_BYTE_SEC = float(os.getenv("INTRO_FIRST_BYTE_TIMEOUT_SEC", "3"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), max_retries=0)

def _is_stale() -> bool:
    try: return (time.time() - PLAY_LOCK.stat().st_mtime) > STALE_SEC
    except FileNotFoundError: return False

def _force_clear():
    try: PLAY_LOCK.unlink()
    except FileNotFoundError: pass

def acquire_play_lock(timeout: float = LOCK_TIMEOUT):
    deadline = time.time() + timeout
    while True:
        try:
            fd = os.open(PLAY_LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd); return
        except FileExistsError:
            if _is_stale() or time.time() >= deadline:
                _force_clear(); continue
            time.sleep(0.2)

def release_play_lock():
    if not _is_stale(): _force_clear()

def fetch_unplayed(cur) -> List[Tuple[int, str]]:
    cur.execute("""SELECT id, text FROM intro_captions
                   WHERE played = false ORDER BY id
                   FOR UPDATE SKIP LOCKED""")
    return cur.fetchall()

def mark_played(cur, _id: int):
    cur.execute("UPDATE intro_captions SET played = true WHERE id = %s", (_id,))

def synthesize_to_file(text: str, out_file: pathlib.Path):
    out_file.unlink(missing_ok=True)
    last_err: Exception | None = None
    for m in MODEL_CHAIN:
        try:
            c = client.with_options(timeout=httpx.Timeout(
                connect=FIRST_BYTE_SEC, write=FIRST_BYTE_SEC,
                read=FIRST_BYTE_SEC, timeout=FIRST_BYTE_SEC * 4))
            with c.audio.speech.with_streaming_response.create(
                model=m, input=text, voice=VOICE,
                response_format=AUDIO_FMT, speed=TTS_SPEED) as resp:
                resp.stream_to_file(out_file)
            return
        except (OpenAIError, httpx.TimeoutException) as exc:
            last_err = exc
            out_file.unlink(missing_ok=True)
    raise RuntimeError("intro TTS failed") from last_err

def play_audio(path: pathlib.Path):
    acquire_play_lock()
    try:
        p = str(path)
        if sys.platform.startswith("darwin"):
            subprocess.run(["afplay", p], check=True)
        elif sys.platform.startswith("win"):
            try:
                from playsound import playsound as ps
                ps(p)
            except Exception:
                wm = shutil.which("wmplayer")
                if wm: subprocess.run([wm, "/play", "/close", p], check=True)
        else:
            subprocess.run(["mpg123", "-q", p], check=True)
    finally:
        release_play_lock()

def main():
    with psycopg2.connect(**DB) as conn, conn.cursor() as cur:
        conn.autocommit = False
        rows = fetch_unplayed(cur)
        if not rows: return
        for _id, text in rows:
            mp3 = OUT_DIR / f"{_id}.{AUDIO_FMT}"
            try:
                synthesize_to_file(text, mp3)
                play_audio(mp3)
                mark_played(cur, _id)
                conn.commit()
            except Exception as exc:
                conn.rollback()
                logging.error("Intro %s failed: %s", _id, exc, exc_info=True)

if __name__ == "__main__":
    main()
