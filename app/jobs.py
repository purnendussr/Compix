import os
from threading import Thread
from app.ffmpeg import compress_video
from app.model import get_connection

def update_status(video_id, status, output_path=None):
    conn = get_connection()
    cursor = conn.cursor()

    if output_path:
        cursor.execute(
            "UPDATE videos SET status=?, output_path=? WHERE id=?",
            (status, output_path, video_id)
        )
    else:
        cursor.execute(
            "UPDATE videos SET status=? WHERE id=?",
            (status, video_id)
        )

    conn.commit()
    conn.close()

def process_video(video_id, input_path, output_path):
    try:
        update_status(video_id, "PROCESSING")

        compress_video(input_path, output_path)

        update_status(video_id, "DONE", output_path)

        if os.path.exists(input_path):
            os.remove(input_path)

    except Exception as e:
        print("❌ ERROR during video processing:", e)
        update_status(video_id, "FAILED")

def start_background_job(video_id, input_path, output_path):
    Thread(
        target=process_video,
        args=(video_id, input_path, output_path),
        daemon=True
    ).start()
