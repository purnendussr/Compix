import subprocess
import os
import re

FFMPEG_PATH = "ffmpeg"


def compress_video(input_path: str, output_path: str, progress_callback=None):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    command = [
        FFMPEG_PATH,
        "-y",
        "-i", input_path,

        "-vf", "scale=1280:-2",
        "-c:v", "libx264",
        "-preset", "fast",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",

        "-c:a", "aac",
        "-b:a", "96k",

        output_path
    ]

    print("🎬 Running FFmpeg command:")
    print(" ".join(command))

    process = subprocess.Popen(
        command,
        stderr=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        universal_newlines=True,
        bufsize=1
    )

    duration = None

    for line in process.stderr:
        # Extract total duration
        if "Duration" in line:
            match = re.search(r"Duration: (\d+):(\d+):(\d+)\.(\d+)", line)
            if match:
                h, m, s, _ = map(int, match.groups())
                duration = h * 3600 + m * 60 + s

        # Extract current time and compute progress
        if "time=" in line and duration and progress_callback:
            time_match = re.search(r"time=(\d+):(\d+):(\d+)\.(\d+)", line)
            if time_match:
                h, m, s, _ = map(int, time_match.groups())
                current_time = h * 3600 + m * 60 + s
                percent = int((current_time / duration) * 100)
                progress_callback(min(percent, 100))

    process.wait()

    if process.returncode != 0:
        raise RuntimeError("FFmpeg compression failed")

    print("✅ FFmpeg compression successful")
