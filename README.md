🎬 Compix — Video Processing Backend API

Compix is a production-style backend system that allows users to upload videos, compress them asynchronously using FFmpeg, and download optimized outputs — with real-time progress tracking and automatic storage management.

🚀 Features

📤 Video Upload API

⚙️ Asynchronous Background Processing

🎥 FFmpeg Video Compression

📊 Live Compression Progress Tracking (%)

🗄 Database-Backed Job Status (SQLite)

🔒 Upload Validation (File Type & Size Limits)

🧹 Automatic Cleanup of Old Files

🌐 RESTful API Design

🧠 How Compix Works

User uploads a video

Compix stores metadata in a database

Compression runs in a background thread

FFmpeg progress is tracked in real-time

User checks processing status via API

Compressed video becomes available for download

Old files are automatically cleaned to save storage

🧱 Tech Stack
Layer	Technology
Backend Framework	FastAPI
Video Processing	FFmpeg
Database	SQLite
Async Jobs	Python Threads
API Documentation	Swagger / OpenAPI
📡 API Endpoints
Method	Endpoint	Description
POST	/upload	Upload video for compression
GET	/status/{video_id}	Get processing status & progress
GET	/download/{video_id}	Download compressed video
📊 Status Flow
UPLOADING → PROCESSING → DONE
                     ↘ FAILED


Example response:

{
  "status": "PROCESSING",
  "progress": 57
}

🔒 Upload Restrictions

Allowed formats: .mp4, .mov, .mkv

Max size: 200MB

🧹 Automatic File Cleanup

Compix runs a background cleanup worker that deletes processed videos older than 24 hours, ensuring storage remains under control.

▶️ Running Compix Locally
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn python-multipart

# Start server
python -m uvicorn app.main:app --reload


Open API docs at:
👉 http://127.0.0.1:8000/docs

💡 What Compix Demonstrates

Compix is designed to showcase backend engineering skills:

Asynchronous job processing

External tool integration (FFmpeg)

Real-time progress monitoring

Database-backed task tracking

Secure file handling

Automated system maintenance

🧑‍💻 Author

Purnendu Sekhar Singha Roy
Backend Developer | Python | System Design Enthusiast
