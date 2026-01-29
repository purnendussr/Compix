import os
import math
import requests

API = "http://127.0.0.1:8000"
FILE = "Takey Olpo Kachhe Da...mp4"
CHUNK_SIZE = 5 * 1024 * 1024  # 5 MB

file_size = os.path.getsize(FILE)
total_chunks = math.ceil(file_size / CHUNK_SIZE)

# Step 1: init
res = requests.post(
    f"{API}/videos/init",
    json={
        "filename": os.path.basename(FILE),
        "total_chunks": total_chunks
    }
).json()

video_id = res["video_id"]
print("Video ID:", video_id)

# Step 2: upload chunks
with open(FILE, "rb") as f:
    for i in range(total_chunks):
        chunk = f.read(CHUNK_SIZE)

        print(f"Uploading chunk {i + 1}/{total_chunks}")

        requests.post(
            f"{API}/videos/chunk",
            params={
                "video_id": video_id,
                "chunk_index": i
            },
            files={"file": chunk}
        )

# Step 3: complete
requests.post(
    f"{API}/videos/complete",
    params={
        "video_id": video_id,
        "filename": os.path.basename(FILE)
    }
)

print("Upload complete, compression started")
