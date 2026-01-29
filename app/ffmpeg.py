import subprocess
import os

FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"  # keep as-is

def compress_video(input_path: str, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    command = [
        FFMPEG_PATH,
        "-y",
        "-i", input_path,

        # video
        "-vf", "scale=1280:-2",
        "-c:v", "libx264",
        "-preset", "fast",
        "-pix_fmt", "yuv420p",
        "-profile:v", "main",
        "-movflags", "+faststart",

        # audio
        "-c:a", "aac",
        "-b:a", "96k",
        "-ac", "2",

        output_path
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)
