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