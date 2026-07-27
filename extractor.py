import os
import sqlite3
import shutil

# 1. PASTE YOUR BACKUP FOLDER PATH IN THE QUOTES IN LINE 8
# Mac example: "/Users/YourName/Library/Application Support/MobileSync/Backup/YOUR_DEVICE_ID"
# Windows example: "C:\\Users\\YourName\\AppData\\Roaming\\Apple Computer\\MobileSync\\Backup\\YOUR_DEVICE_ID"
BACKUP_DIR = ""

# 2. WHERE YOU WANT THE FILES TO GO
EXPORT_DIR = "./iPhone_Export"

def extract_files():
    manifest_db = os.path.join(BACKUP_DIR, "Manifest.db")
    
    if not os.path.exists(manifest_db):
        print(f"Error: Could not find Manifest.db in {BACKUP_DIR}")
        print("Make sure you are pointing to the exact folder containing your device's backup.")
        return

    # Create clean export folders
    notes_dir = os.path.join(EXPORT_DIR, "Notes")
    memos_dir = os.path.join(EXPORT_DIR, "VoiceMemos")
    os.makedirs(notes_dir, exist_ok=True)
    os.makedirs(memos_dir, exist_ok=True)

    # Connect to the backup map
    conn = sqlite3.connect(manifest_db)
    cursor = conn.cursor()

    print("Searching for Notes and Voice Memos...")

    # Look for the Notes database and Voice Memo audio files
    query = """
    SELECT fileID, domain, relativePath 
    FROM Files 
    WHERE relativePath LIKE '%NoteStore.sqlite%' 
       OR relativePath LIKE 'Media/Recordings/%.m4a'
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    extracted_count = 0

    for fileID, domain, relativePath in rows:
        # Apple stores the actual file inside a subfolder named after the first 2 letters of the hash
        subfolder = fileID[:2]
        physical_file_path = os.path.join(BACKUP_DIR, subfolder, fileID)

        # Fallback for very old iOS backups that didn't use subfolders
        if not os.path.exists(physical_file_path):
            physical_file_path = os.path.join(BACKUP_DIR, fileID)
            
        if os.path.exists(physical_file_path):
            filename = os.path.basename(relativePath)
            
            if ".m4a" in filename:
                dest_path = os.path.join(memos_dir, filename)
                shutil.copy2(physical_file_path, dest_path)
                print(f"Extracted Voice Memo: {filename}")
                extracted_count += 1
            elif "NoteStore.sqlite" in filename:
                dest_path = os.path.join(notes_dir, f"{domain}_{filename}")
                shutil.copy2(physical_file_path, dest_path)
                print(f"Extracted Notes DB: {filename}")
                extracted_count += 1

    conn.close()
    print(f"\nDone! Successfully extracted {extracted_count} files to {EXPORT_DIR}")

if __name__ == "__main__":
    extract_files()
