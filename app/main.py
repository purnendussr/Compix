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
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI()

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

    return FileResponse(
        output_path,
        media_type="video/mp4",
        filename=f"{video_id}.mp4"
    )

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
