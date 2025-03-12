import os
import hashlib
import json
import time
import shutil

UPLOADS_FOLDER = "Uploads"
DOWNLOADS_FOLDER = "Downloads"
DB_FILE = "files.json"

# Ensure directories exist
os.makedirs(UPLOADS_FOLDER, exist_ok=True)
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

def compute_sha256(file_path):
    """Compute SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

def load_db():
    """Load existing file database (or create one if missing)."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db(db):
    """Save file metadata to JSON database."""
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

def check_for_new_files():
    """Monitor 'Uploads' folder for new ZIP files and process them."""
    db = load_db()
    
    for filename in os.listdir(UPLOADS_FOLDER):
        file_path = os.path.join(UPLOADS_FOLDER, filename)

        if filename.endswith(".zip") and filename not in db:
            print(f"🔍 Processing new file: {filename}")
            file_hash = compute_sha256(file_path)

            # Save metadata
            db[filename] = {
                "hash": file_hash,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "Stored"
            }
            save_db(db)

            # Move file to Downloads folder (simulating sync)
            new_path = os.path.join(DOWNLOADS_FOLDER, filename)
            shutil.move(file_path, new_path)
            print(f"✅ {filename} moved to {DOWNLOADS_FOLDER}/")

    print("📡 No new files. Waiting...")

if __name__ == "__main__":
    print("🚀 File Sync Service Started...")
    while True:
        check_for_new_files()
        time.sleep(5)  # Check every 5 seconds
