# 📂 Install - Unzip Google Drive Zip Files with Timestamp

This guide provides a Bash and Python script to automatically **unzip multiple ZIP files** from a directory (e.g., `~/Downloads`) and **rename each output folder or file with a timestamp** to avoid conflicts.

---

## ✅ Prerequisites

* ZIP files stored in the `~/Downloads` folder
* Python 3 or Bash installed
* Basic Linux terminal access

---

## 🐚 Bash Script: `unzip_with_timestamp.sh`

```bash
#!/bin/bash

DOWNLOAD_DIR="$HOME/Downloads"
DEST_DIR="$HOME/UnzippedFiles"
mkdir -p "$DEST_DIR"

for zipfile in "$DOWNLOAD_DIR"/*.zip; do
  if [[ -f "$zipfile" ]]; then
    timestamp=$(date +%Y%m%d_%H%M%S)
    filename=$(basename "$zipfile" .zip)
    target="$DEST_DIR/${filename}_$timestamp"
    mkdir -p "$target"
    unzip -q "$zipfile" -d "$target"
    echo "✅ Unzipped: $zipfile -> $target"
  fi
done
```

### ▶️ How to Run

```bash
chmod +x unzip_with_timestamp.sh
./unzip_with_timestamp.sh
```

---

## 🐍 Python Script: `unzip_with_timestamp.py`

```python
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
```

### ▶️ How to Run

```bash
python3 unzip_with_timestamp.py
```

---

## 📘 Notes

* Timestamp format used: `YYYYMMDD_HHMMSS`
* All outputs are stored in `~/UnzippedFiles`
* Scripts safely ignore non-`.zip` files

---

## ✅ Done

You can now safely unzip Google Drive ZIP files and keep each run uniquely timestamped to avoid overwriting results.
