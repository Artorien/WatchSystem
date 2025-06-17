import os, json, subprocess, sys, atexit
from pathlib import Path

import psycopg2
from apify_client import ApifyClient
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

load_dotenv()

app = Flask(__name__)
CORS(app)


def init_db():
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    if not db_password:
        raise ValueError("Database password is missing. Check your environment variables.")

    return psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host="db",
        port="5432",
    )


APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
TWITTER_ACTOR_ID = os.getenv("TWITTER_ACTOR_ID")
INSTAGRAM_ACTOR_ID = os.getenv("INSTAGRAM_ACTOR_ID")

client = ApifyClient(APIFY_API_TOKEN)

globalHashtags = []
globalPlatforms = []


def run_scraping_job(hashtags, platforms):
    results = []

    for tag in hashtags:
        for platform in platforms:
            try:
                if platform == "twitter":
                    run = client.actor(TWITTER_ACTOR_ID).call(
                        run_input={
                            "searchTerms": [tag],
                            "maxItems": 10,
                            "sort": "Latest",
                        }
                    )
                elif platform == "instagram":
                    run = client.actor(INSTAGRAM_ACTOR_ID).call(
                        run_input={
                            "hashtags": [tag],
                            "resultsLimit": 10,
                            "resultsType": "posts",
                        }
                    )
                else:
                    error_msg = f"Unsupported platform: {platform}"
                    print(error_msg)
                    return {"error": error_msg, "status_code": 500}
            except Exception as e:
                print(f"Apify error for {platform}: {e}")
                return {"error": f"Apify error: {str(e)}", "status_code": 500}

            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                if platform == "twitter":
                    content = item.get("fullText", "")
                    ts = item.get("createdAt")
                else:
                    content = item.get("caption", "")
                    ts = item.get("timestamp")
                results.append(
                    {
                        "hashtag": tag,
                        "platform": platform,
                        "content": content,
                        "time_stamp": ts,
                    }
                )

    if not results:
        print("No results to process.")
        return {"result": [], "status_code": 201}

    try:
        conn = init_db()
        cursor = conn.cursor()
        for row in results:
            cursor.execute(
                "INSERT INTO captions (text, social_media, time_stamp) VALUES (%s, %s, %s)",
                (row["content"], row["platform"], row["time_stamp"])
            )
        conn.commit()
    except Exception as db_exc:
        print(f"Database error: {db_exc}")
        return {"error": "Database operation failed", "status_code": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

    try:
        moderation_path = Path(__file__).resolve().parent / "moderation.py"
        subprocess.run(
            [sys.executable, str(moderation_path), json.dumps(results)],
            check=True,
            env=os.environ.copy(),
        )
    except subprocess.CalledProcessError as exc:
        print(f"Moderation subprocess failed: {exc}")
        return {"error": str(exc), "status_code": 500}

    return {"result": results, "status_code": 201}


@app.route("/scrape", methods=["POST"])
def scrape():
    global globalHashtags, globalPlatforms

    data = request.json or {}

    hashtags = data.get("hashtags")
    platforms = data.get("platforms")

    if not hashtags:
        return jsonify({"error": "Missing 'hashtags'"}), 400
    if not platforms or not isinstance(platforms, list):
        return jsonify({"error": "Missing or invalid 'platforms' list"}), 400

    for p in platforms:
        if p not in {"twitter", "instagram"}:
            return jsonify({"error": f"Invalid platform '{p}'"}), 400

    globalHashtags = hashtags
    globalPlatforms = platforms

    try:
        result = run_scraping_job(hashtags, platforms)

        if isinstance(result, tuple):
            status_code = result.pop("status_code", 200)
            return jsonify(result), status_code
        status_code = result.pop("status_code", 200)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


scheduler = BackgroundScheduler()
scheduler.start()

scheduler.add_job(
    func=lambda: run_scraping_job(globalHashtags, globalPlatforms)
    if globalHashtags and globalPlatforms
    else None,
    trigger=IntervalTrigger(minutes=2),
    id="scrape_job",
    name="Scheduled scraping job",
    replace_existing=True
)

atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
