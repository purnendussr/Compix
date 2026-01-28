from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import uuid
import os
import time
from threading import Thread

from app.jobs import start_background_job
from app.db import init_db
from app.video_service import create_video, get_status
from app.cleanup import cleanup_old_files

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

ALLOWED_EXTENSIONS = {".mp4", ".mov", ".mkv"}
MAX_FILE_SIZE_MB = 200

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI()


# ---------------- CLEANUP BACKGROUND LOOP ----------------
def cleanup_loop():
    while True:
        cleanup_old_files()
        time.sleep(3600)  # Run every hour


# ---------------- STARTUP EVENT ----------------
@app.on_event("startup")
def startup():
    init_db()
    Thread(target=cleanup_loop, daemon=True).start()


# ---------------- UPLOAD ----------------
@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")

    video_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_DIR, f"{video_id}_{file.filename}")
    output_path = os.path.join(OUTPUT_DIR, f"{video_id}.mp4")

    create_video(video_id, file.filename)

    with open(input_path, "wb") as f:
        f.write(content)

    start_background_job(video_id, input_path, output_path)

    return {"video_id": video_id, "status": "PROCESSING"}


# ---------------- STATUS CHECK ----------------
@app.get("/status/{video_id}")
def check_status(video_id: str):
    return get_status(video_id)


# ---------------- DOWNLOAD ----------------
@app.get("/download/{video_id}")
def download_video(video_id: str):
    output_path = os.path.join(OUTPUT_DIR, f"{video_id}.mp4")
    status_info = get_status(video_id)

    if status_info["status"] != "DONE":
        return {"video_id": video_id, **status_info}

    if not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        output_path,
        media_type="video/mp4",
        filename=f"{video_id}.mp4"
    )
