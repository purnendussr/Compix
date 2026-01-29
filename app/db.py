import sqlite3

DB_NAME = "videos.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            video_id TEXT PRIMARY KEY,
            filename TEXT,
            status TEXT,
            progress INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()
