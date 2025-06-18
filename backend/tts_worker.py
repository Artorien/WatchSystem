#!/usr/bin/env python3
from __future__ import annotations
import os, pathlib, sys, subprocess, shutil, time, logging
from typing import Sequence
import psycopg as psycopg2
from dotenv import load_dotenv
import httpx
from openai import OpenAI, OpenAIError

try:
    from playsound import playsound
except ImportError:
    playsound = None

load_dotenv()

OUT_DIR   = pathlib.Path(__file__).with_suffix("") / "tts_output"
OUT_DIR.mkdir(parents=True, exist_ok=True)
PLAY_LOCK = OUT_DIR / ".playing.lock"

LOCK_TIMEOUT  = float(os.getenv("PLAY_LOCK_TIMEOUT", "60"))
STALE_SEC     = float(os.getenv("PLAY_LOCK_STALE_SEC", "15"))
VOICE         = os.getenv("VOICE_NAME", "alloy")

PRIMARY_MODEL = os.getenv("TTS_MODEL", "tts-1-hd")
FALLBACK_MODELS = [m.strip() for m in os.getenv(
    "TTS_FALLBACK_MODELS",
    "gpt-4o-mini-tts,tts-1,tts-1-1106,tts-1-hd-1106"
).split(",") if m.strip()]
MODEL_CHAIN: Sequence[str] = [PRIMARY_MODEL] + [
    m for m in FALLBACK_MODELS if m not in {PRIMARY_MODEL, ""}
]

TTS_SPEED      = float(os.getenv("TTS_SPEED", "1.0"))
AUDIO_FMT      = os.getenv("TTS_FMT", "mp3")
FIRST_BYTE_SEC = float(os.getenv("FIRST_BYTE_TIMEOUT_SEC", "3"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), max_retries=0)

DB = dict(
    dbname   = os.getenv("DB_NAME"),
    user     = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    host     = os.getenv("DB_HOST", "localhost"),
    port     = os.getenv("DB_PORT", "5432"),
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)

def _is_stale() -> bool:
    try:
        return (time.time() - PLAY_LOCK.stat().st_mtime) > STALE_SEC
    except FileNotFoundError:
        return False

def _force_clear():
    try:
        PLAY_LOCK.unlink()
    except FileNotFoundError:
        pass

def acquire_play_lock(timeout: float = LOCK_TIMEOUT):
    deadline = time.time() + timeout
    while True:
        try:
            fd = os.open(PLAY_LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            return
        except FileExistsError:
            if _is_stale() or time.time() >= deadline:
                _force_clear()
                continue
            time.sleep(0.2)

def release_play_lock():
    if not _is_stale():
        _force_clear()

def synthesize_to_file(text: str, out: pathlib.Path):
    out.unlink(missing_ok=True)
    for model in MODEL_CHAIN:
        try:
            c = client.with_options(timeout=httpx.Timeout(
                connect=FIRST_BYTE_SEC, write=FIRST_BYTE_SEC,
                read=FIRST_BYTE_SEC, timeout=FIRST_BYTE_SEC * 4))
            with c.audio.speech.with_streaming_response.create(
                model=model, input=text, voice=VOICE,
                response_format=AUDIO_FMT, speed=TTS_SPEED) as r:
                r.stream_to_file(out)
            return
        except (OpenAIError, httpx.TimeoutException):
            out.unlink(missing_ok=True)
    raise RuntimeError("All TTS models failed")

def play_audio(mp3: pathlib.Path):
    acquire_play_lock()
    try:
        p = str(mp3)
        if sys.platform.startswith("darwin"):
            subprocess.run(["afplay", p], check=True)
        elif sys.platform.startswith("win"):
            try:
                if playsound:
                    playsound(p)
                else:
                    raise RuntimeError
            except Exception:
                wm = shutil.which("wmplayer")
                if wm:
                    subprocess.run([wm, "/play", "/close", p], check=True)
        else:
            subprocess.run(["mpg123", "-q", p], check=True)
    finally:
        release_play_lock()

if PLAY_LOCK.exists() and _is_stale():
    _force_clear()

def main():
    with psycopg2.connect(**DB) as conn, conn.cursor() as cur:
        conn.autocommit = False
        cur.execute(
            """
            SELECT id, content
              FROM captions
             WHERE played = false
             ORDER BY id
             LIMIT 1
             FOR UPDATE SKIP LOCKED
            """
        )
        row = cur.fetchone()
        if not row:
            logging.info("No unplayed captions.")
            return

        _id, text = row
        mp3 = OUT_DIR / f"{_id}.{AUDIO_FMT}"

        try:
            synthesize_to_file(text, mp3)
            cur.execute("UPDATE captions SET played = true WHERE id = %s", (_id,))
            conn.commit()
            logging.info("Play %s", mp3.name)
            play_audio(mp3)
        except Exception as exc:
            conn.rollback()
            logging.error("Caption %s failed: %s", _id, exc, exc_info=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.warning("Interrupted — exiting.")
