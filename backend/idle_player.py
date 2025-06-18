#!/usr/bin/env python3
from __future__ import annotations
import os, sys, random, time, subprocess, shutil, signal
from pathlib import Path
from typing import List

# ── folders with ready-made audio ────────────────────────────────────────────
TTS_DIR   = Path(__file__).resolve().parent / "tts_worker"  / "tts_output"
INTRO_DIR = Path(__file__).resolve().parent / "intro_worker" / "intro_output"
GAP_SEC   = 5       # pause between tracks

# ── cross-platform playback helper ──────────────────────────────────────────
try:
    from playsound import playsound        # blocking on Windows
except ImportError:
    playsound = None

def play_sync(mp3: Path) -> None:
    p = str(mp3)
    if sys.platform.startswith("darwin"):              # macOS
        subprocess.run(["afplay", p], check=False)
    elif sys.platform.startswith("win"):               # Windows
        if playsound:
            try:
                playsound(p)
            except Exception:
                pass
        else:
            wmp = shutil.which("wmplayer")
            if wmp:
                subprocess.run([wmp, "/play", "/close", p], check=False)
    else:                                              # Linux / other
        subprocess.run(["mpg123", "-q", p], check=False)

# ── graceful shutdown flag ──────────────────────────────────────────────────
_running = True
for sig in (signal.SIGTERM, signal.SIGINT):
    signal.signal(sig, lambda *_: globals().__setitem__("_running", False))

# ── main loop ────────────────────────────────────────────────────────────────
def gather_tracks() -> List[Path]:
    return list(TTS_DIR.glob("*.mp3")) + list(INTRO_DIR.glob("*.mp3"))

def main() -> None:
    TTS_DIR.mkdir(parents=True, exist_ok=True)
    INTRO_DIR.mkdir(parents=True, exist_ok=True)

    while _running:
        tracks = gather_tracks()
        if not tracks:
            time.sleep(30)           # nothing to play yet
            continue

        random.shuffle(tracks)
        for track in tracks:
            if not _running:         # got SIGTERM
                break
            print(f"[idle_player] playing {track.name}")
            play_sync(track)
            for _ in range(GAP_SEC):
                if not _running:
                    break
                time.sleep(1)

if __name__ == "__main__":
    main()
