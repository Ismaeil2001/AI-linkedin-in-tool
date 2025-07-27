import json
import os

def load_seen_posts(file_path):
    if not os.path.exists(file_path):
        return set()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return set(data)
    except Exception as e:
        print(f"⚠️ Failed to load seen posts: {e}")
        return set()

def save_seen_posts(file_path, seen_hashes):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(list(seen_hashes), f, indent=2)
        print(f"💾 Saved {len(seen_hashes)} hashes to {file_path}")
    except Exception as e:
        print(f"❌ Failed to save seen posts: {e}")
