import sqlite3

DB_PATH = "videos.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id TEXT PRIMARY KEY,
            input_path TEXT,
            output_path TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()
