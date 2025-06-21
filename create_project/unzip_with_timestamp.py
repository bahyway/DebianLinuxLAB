import os
import zipfile
from datetime import datetime

DOWNLOAD_DIR = os.path.expanduser('~/Downloads')
DEST_DIR = os.path.expanduser('~/UnzippedFiles')
os.makedirs(DEST_DIR, exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

for entry in os.listdir(DOWNLOAD_DIR):
    if entry.endswith('.zip'):
        zip_path = os.path.join(DOWNLOAD_DIR, entry)
        filename = os.path.splitext(entry)[0]
        output_folder = os.path.join(DEST_DIR, f"{filename}_{timestamp}")
        os.makedirs(output_folder, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_folder)
        print(f"✅ Extracted {entry} to {output_folder}")