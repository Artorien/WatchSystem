from __future__ import annotations

import os, pathlib, sys, subprocess
import psycopg2
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OUT_DIR = pathlib.Path(__file__).with_suffix("") / "tts_output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
VOICE  = os.getenv("VOICE_NAME", "alloy")

DB = dict(
    dbname   = os.getenv("DB_NAME"),
    user     = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    host     = os.getenv("DB_HOST", "localhost"),
    port     = os.getenv("DB_PORT", "5432"),
)

# macOS built-in player; adjust for Linux/Windows if needed
PLAYER = ["afplay"]          # e.g. ["mpg123", "-q"] on Linux, or use playsound lib

def fetch_unplayed(cur):
    cur.execute("SELECT id, content FROM not_flagged WHERE played = false ORDER BY id")
    return cur.fetchall()

def mark_played(cur, _id: int):
    cur.execute("UPDATE not_flagged SET played = true WHERE id = %s", (_id,))

def synthesize(text: str) -> bytes:
    resp = client.audio.speech.create(
        model="tts-1",
        input=text,
        voice=VOICE,
    )
    return resp.content                     # raw MP3 bytes

def play_audio(path: pathlib.Path):
    try:
        subprocess.run(PLAYER + [str(path)], check=True)
    except Exception as e:
        print(f"   (audio player error: {e})", file=sys.stderr)

def main() -> None:
    conn = psycopg2.connect(**DB)
    cur  = conn.cursor()

    rows = fetch_unplayed(cur)
    if not rows:
        print("Nothing to voice.")
        cur.close(); conn.close()
        return

    print(f"Generating TTS for {len(rows)} comment(s)…")

    for _id, text in rows:
        try:
            audio = synthesize(text)
            out_file = OUT_DIR / f"{_id}.mp3"
            out_file.write_bytes(audio)
            mark_played(cur, _id)          # mark first, so we never loop
            conn.commit()
            print(f" ✔ id {_id} → playing {out_file.name}")
            play_audio(out_file)           # blocks until playback finishes
        except Exception as e:
            conn.rollback()
            print(f" ✖ id {_id} failed: {e}", file=sys.stderr)

    cur.close(); conn.close()

if __name__ == "__main__":
    main()
