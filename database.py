import json
import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
DB_PATH = DATA_DIR / "viva_coach.db"


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                topic TEXT NOT NULL,
                question TEXT NOT NULL,
                transcript TEXT NOT NULL,
                score INTEGER NOT NULL,
                covered_points TEXT NOT NULL,
                missing_points TEXT NOT NULL,
                feedback TEXT NOT NULL
            )
            """
        )


def save_attempt(
    topic,
    question,
    transcript,
    score,
    covered_points,
    missing_points,
    feedback,
):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO attempts (
                topic, question, transcript, score,
                covered_points, missing_points, feedback
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                topic,
                question,
                transcript,
                score,
                json.dumps(covered_points, ensure_ascii=False),
                json.dumps(missing_points, ensure_ascii=False),
                feedback,
            ),
        )


def get_recent_attempts(topic, limit=10):
    with get_connection() as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT created_at, question, score
            FROM attempts
            WHERE topic = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (topic, limit),
        ).fetchall()

    return [dict(row) for row in rows]

def get_topic_progress(topic):
    from collections import Counter

    with get_connection() as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT score, missing_points
            FROM attempts
            WHERE topic = ?
            ORDER BY id ASC
            """,
            (topic,),
        ).fetchall()

    scores = []
    missed_counts = Counter()

    for row in rows:
        scores.append(row["score"])
        missing = json.loads(row["missing_points"] or "[]")
        missed_counts.update(missing)

    average_score = sum(scores) / len(scores) if scores else 0

    return {
        "attempt_count": len(scores),
        "average_score": average_score,
        "score_history": scores[-20:],
        "weak_points": missed_counts.most_common(3),
    }