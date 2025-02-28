import os
import time
import subprocess

WATCH_FOLDER = "/var/spool/cups-pdf"
SCRIPT = "/home/pi/LabelPrinter/app.py"

def watch_folder():
    print(f"Watching {WATCH_FOLDER} for new files...")
    processed_files = set()

    while True:
        files = os.listdir(WATCH_FOLDER)
        for file in files:
            file_path = os.path.join(WATCH_FOLDER, file)
            if file not in processed_files and file.endswith(('.pdf', '.jpg', '.png')):
                print(f"New file detected: {file}")
                subprocess.run(["python3", SCRIPT, file_path])
                processed_files.add(file)
        time.sleep(2)

if __name__ == "__main__":
    watch_folder()
