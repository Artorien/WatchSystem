#!/usr/bin/env python3
from __future__ import annotations
# ── stdlib ─────────────────────────────────────────────────────────────────
import json, os, sys, re, subprocess
from pathlib import Path
from typing import List, Dict
# ── 3rd-party ──────────────────────────────────────────────────────────────
import psycopg as psycopg2           # pip install psycopg
from openai import OpenAI            # pip install openai
# ── regex cleaners ─────────────────────────────────────────────────────────
emoji_pat   = re.compile('[\U0001F300-\U0001FAFF\U00002700-\U000027BF]+')
url_pat     = re.compile(r'https?://\S+')
mention_pat = re.compile(r'@\w+')
hashtag_pat = re.compile(r'(?:\s|^)#\w+')

def clean(text: str) -> str:
    text = emoji_pat.sub('', text)
    text = url_pat.sub('', text)
    text = mention_pat.sub('', text)
    text = hashtag_pat.sub(' ', text)
    text = text.replace('\n', ' ')
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

# ── OpenAI moderation ──────────────────────────────────────────────────────
client    = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
THRESHOLD = float(os.getenv("MODERATION_THRESHOLD", 0.10))
AD_WORDS  = {
    "buy","sale","offer","discount","limited","promo","price","shipping",
    "shop","available","click","order","subscribe","link","dm","code","coupon"
}

def is_offensive(text: str) -> bool:
    resp = client.moderations.create(input=text, model="omni-moderation-latest")
    r    = resp.results[0]

    if r.flagged:
        return True

    s = r.category_scores
    if any(w in text.lower() for w in AD_WORDS):
        return True

    return (
        s.harassment_threatening > THRESHOLD or s.harassment > THRESHOLD or
        s.hate_threatening       > THRESHOLD or s.hate       > THRESHOLD or
        s.sexual_minors          > THRESHOLD or s.sexual     > THRESHOLD or
        s.self_harm              > THRESHOLD
    )

# ── DB helpers ─────────────────────────────────────────────────────────────
def init_db():
    return psycopg2.connect(
        dbname   = os.getenv("DB_NAME"),
        user     = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        host     = os.getenv("DB_HOST", "localhost"),
        port     = os.getenv("DB_PORT", "5432"),
    )

def already_exists(cur, table: str, txt: str) -> bool:
    cur.execute(f"SELECT 1 FROM {table} WHERE LOWER(content) = LOWER(%s) LIMIT 1", (txt,))
    return cur.fetchone() is not None

def store(records: List[Dict]):
    conn = init_db();  cur = conn.cursor()

    for rec in records:
        txt = clean(rec["content"])
        if not (0 < len(txt) <= 264):
            continue

        if (already_exists(cur, "captions", txt) or
            already_exists(cur, "flagged",  txt)):
            continue

        dest = "flagged" if is_offensive(txt) else "captions"
        cur.execute(
            f"INSERT INTO {dest} (hashtag, content, time_stamp)"
            f"VALUES (%s, %s, %s)",
            (rec["hashtag"], txt, rec.get("time_stamp")),
        )

    conn.commit(); cur.close(); conn.close()

# ── payload loader ─────────────────────────────────────────────────────────
def load_payload() -> List[Dict[str, Any]]:
    if len(sys.argv) > 1:                            # called with a temp file
        arg = sys.argv[1]
        p   = Path(arg)
        if p.exists():                              # temp file path
            return json.loads(p.read_text(encoding='utf-8'))
        else:                                       # raw JSON in argv
            return json.loads(arg)

    stdin_raw = sys.stdin.read().strip()
    return json.loads(stdin_raw) if stdin_raw else []

# ── entrypoint ─────────────────────────────────────────────────────────────
def main():
    payload = load_payload()
    if not payload:
        return
    if isinstance(payload, dict):
        payload = [payload]

    store(payload)

    # fire up tts_worker in background
    tts = Path(__file__).parent / "tts_worker.py"
    try:
        subprocess.Popen([sys.executable, str(tts)], env=os.environ.copy())
    except Exception as e:
        print("Could not launch tts_worker:", e, file=sys.stderr)

if __name__ == "__main__":
    main()
