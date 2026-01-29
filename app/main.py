<<<<<<< HEAD
from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.responses import FileResponse
import uuid
import os

from app.model import init_db, get_connection
from app.jobs import start_background_job

UPLOAD_DIR = "uploads"
TMP_DIR = os.path.join(UPLOAD_DIR, "tmp")
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)
=======
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
>>>>>>> f0e89cb46db45e463cc55613063a5f0a0f69682a
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI()

<<<<<<< HEAD
@app.on_event("startup")
def startup():
    init_db()

# ------------------ DOWNLOAD ------------------

@app.get("/videos/{video_id}/download")
def download_video(video_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT output_path, status FROM videos WHERE id=?",
        (video_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(404, "Video not found")

    output_path, status = row

    if status != "DONE":
        raise HTTPException(400, f"Video not ready. Status: {status}")
=======

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
>>>>>>> f0e89cb46db45e463cc55613063a5f0a0f69682a

    return FileResponse(
        output_path,
        media_type="video/mp4",
        filename=f"{video_id}.mp4"
    )
<<<<<<< HEAD

# ------------------ SIMPLE UPLOAD ------------------

@app.post("/videos")
async def upload_video(file: UploadFile = File(...)):
    video_id = str(uuid.uuid4())

    input_path = os.path.join(UPLOAD_DIR, f"{video_id}_{file.filename}")
    output_path = os.path.join(OUTPUT_DIR, f"{video_id}.mp4")

    with open(input_path, "wb") as f:
        f.write(await file.read())

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO videos VALUES (?, ?, ?, ?)",
        (video_id, input_path, output_path, "UPLOADED")
    )
    conn.commit()
    conn.close()

    start_background_job(video_id, input_path, output_path)

    return {"video_id": video_id, "status": "PROCESSING"}

# ------------------ RESUMABLE UPLOAD ------------------

@app.post("/videos/init")
def init_upload(
    filename: str = Body(...),
    total_chunks: int = Body(...)
):
    video_id = str(uuid.uuid4())
    os.makedirs(os.path.join(TMP_DIR, video_id), exist_ok=True)
    return {"video_id": video_id, "total_chunks": total_chunks}

@app.post("/videos/chunk")
async def upload_chunk(
    video_id: str,
    chunk_index: int,
    file: UploadFile = File(...)):
    temp_dir = os.path.join(TMP_DIR, video_id)

    if not os.path.exists(temp_dir):
        raise HTTPException(404, "Upload session not found")

    with open(os.path.join(temp_dir, f"{chunk_index}.part"), "wb") as f:
        f.write(await file.read())

    return {"chunk": chunk_index, "status": "ok"}

@app.post("/videos/complete")
def complete_upload(video_id: str, filename: str):
    temp_dir = os.path.join(TMP_DIR, video_id)

    if not os.path.exists(temp_dir):
        raise HTTPException(404, "Upload session not found")

    input_path = os.path.join(UPLOAD_DIR, f"{video_id}_{filename}")
    output_path = os.path.join(OUTPUT_DIR, f"{video_id}.mp4")

    with open(input_path, "wb") as final:
        for part in sorted(os.listdir(temp_dir), key=lambda x: int(x.split(".")[0])):
            with open(os.path.join(temp_dir, part), "rb") as p:
                final.write(p.read())

    for f in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, f))
    os.rmdir(temp_dir)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO videos VALUES (?, ?, ?, ?)",
        (video_id, input_path, output_path, "UPLOADED")
    )
    conn.commit()
    conn.close()

    start_background_job(video_id, input_path, output_path)

    return {"video_id": video_id, "status": "PROCESSING"}
=======
>>>>>>> f0e89cb46db45e463cc55613063a5f0a0f69682a
