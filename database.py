import sqlite3
import json
from datetime import datetime, timezone

DB_NAME = "salemsniper.db"


def connect():
    return sqlite3.connect(DB_NAME)


def initialize():
    with connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                username TEXT,
                live_url TEXT UNIQUE,
                confidence REAL,
                details TEXT,
                created_at TEXT
            )
        """)


def save_result(result):
    try:
        with connect() as db:
            db.execute("""
                INSERT INTO results
                (platform, username, live_url,
                 confidence, details, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                result.get("platform"),
                result.get("username"),
                result.get("live_url"),
                result.get("confidence"),
                json.dumps(result, ensure_ascii=False),
                datetime.now(timezone.utc).isoformat()
            ))
        return True
    except sqlite3.IntegrityError:
        return False


def get_results(limit=20):
    with connect() as db:
        db.row_factory = sqlite3.Row
        rows = db.execute("""
            SELECT * FROM results
            ORDER BY id DESC LIMIT ?
        """, (limit,)).fetchall()

    return [dict(row) for row in rows]
