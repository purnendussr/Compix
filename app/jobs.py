import os
from threading import Thread
<<<<<<< HEAD
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
=======
from app.ffmpeg_utils import compress_video
from app.video_service import update_status, update_progress


def process_video(video_id: str, input_path: str, output_path: str):
    try:
        print(f"🎬 Starting processing for {video_id}")
        update_status(video_id, "PROCESSING")

        # Run compression and update progress in DB
        compress_video(
            input_path,
            output_path,
            progress_callback=lambda p: update_progress(video_id, p)
        )

        # Remove original file after successful compression
        if os.path.exists(input_path):
            os.remove(input_path)

        update_progress(video_id, 100)
        update_status(video_id, "DONE")

        print(f"✅ Compression finished for {video_id}")

    except Exception as e:
        update_status(video_id, "FAILED")
        print(f"❌ Error processing {video_id}: {e}")


def start_background_job(video_id: str, input_path: str, output_path: str):
>>>>>>> f0e89cb46db45e463cc55613063a5f0a0f69682a
    Thread(
        target=process_video,
        args=(video_id, input_path, output_path),
        daemon=True
    ).start()
