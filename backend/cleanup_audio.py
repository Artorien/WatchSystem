# cleanup_audio.py

from pathlib import Path
import os
import sys

BASE   = Path(__file__).resolve().parent
OUTDIR = BASE / "tts_worker" / "tts_output"

def main(max_keep: int = 2500) -> None:
    if not OUTDIR.exists():
        print(f"[cleanup] Folder not found: {OUTDIR}", file=sys.stderr)
        return

    mp3_files = sorted(
        OUTDIR.glob("*.mp3"),
        key=lambda p: p.stat().st_mtime,
    )

    excess = len(mp3_files) - max_keep
    if excess <= 0:
        print(f"[cleanup] {len(mp3_files)} file(s) – nothing to delete.")
        return

    to_delete = mp3_files[:excess]
    for f in to_delete:
        try:
            f.unlink()
            print(f"[cleanup] Removed {f.name}")
        except OSError as e:
            print(f"[cleanup] Could not delete {f}: {e}", file=sys.stderr)

    print(f"[cleanup] Done – kept {max_keep} newest file(s).")

if __name__ == "__main__":
    main()
