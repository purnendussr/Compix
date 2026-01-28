import os
import time

OUTPUT_DIR = "outputs"
MAX_AGE_HOURS = 24


def cleanup_old_files():
    if not os.path.exists(OUTPUT_DIR):
        return

    now = time.time()
    cutoff = now - MAX_AGE_HOURS * 3600

    for filename in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, filename)

        try:
            if os.path.isfile(path) and os.path.getmtime(path) < cutoff:
                os.remove(path)
                print(f"🗑 Deleted old file: {filename}")
        except Exception as e:
            print(f"⚠️ Failed to delete {filename}: {e}")
