import os
from threading import Thread
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
    Thread(
        target=process_video,
        args=(video_id, input_path, output_path),
        daemon=True
    ).start()
