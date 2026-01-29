🎬 Compix — Video Processing Backend API

Compix is a production-style backend system that allows users to upload videos, compress them asynchronously using FFmpeg, and download optimized outputs — with real-time progress tracking and automatic storage management.

🚀 Features

📤 Video Upload API

⚙️ Asynchronous Background Processing

🎥 FFmpeg Video Compression

🗄 Database-Backed Job Status (SQLite)

🌐 RESTful API Design

🧠 How Compix Works

User uploads a video

Compix stores metadata in a database

Compression runs in a background thread

FFmpeg progress is tracked 

User checks processing status via API

Compressed video becomes available for download


🧱 Tech Stack
Backend Framework	FastAPI
Video Processing	FFmpeg
Database	SQLite
Async Jobs	Python Threads
API Documentation	Swagger
📡 API Endpoints
Method	Endpoint	Description
POST	/upload	Upload video for compression
GET	/status/{video_id}	Get processing status & progress
GET	/download/{video_id}	Download compressed video
📊 Status Flow
UPLOADING → PROCESSING → DONE
                     ↘ FAILED


🔒 Upload Restrictions

Allowed formats: .mp4, .mov, .mkv


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

External tool integration (FFmpeg)

Database-backed task tracking


🧑‍💻 Author

Purnendu Sekhar Singha Roy
Backend Developer | Python | System Design Enthusiast
