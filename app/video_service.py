from datetime import datetime
from app.db import get_connection


def create_video(video_id: str, filename: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO videos (video_id, filename, status, progress, created_at) VALUES (?, ?, ?, ?, ?)",
        (video_id, filename, "UPLOADING", 0, datetime.utcnow().isoformat())
    )

    conn.commit()
    conn.close()


def update_status(video_id: str, status: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE videos SET status=? WHERE video_id=?",
        (status, video_id)
    )

    conn.commit()
    conn.close()


def update_progress(video_id: str, progress: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE videos SET progress=? WHERE video_id=?",
        (progress, video_id)
    )

    conn.commit()
    conn.close()


def get_status(video_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT status, progress FROM videos WHERE video_id=?",
        (video_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"status": row[0], "progress": row[1]}
    return {"status": "NOT_FOUND", "progress": 0}
