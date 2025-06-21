# yt-dlp on Debian 12 - Installation and Usage Guide

## ✅ Installation Steps

### 1. Install Required Dependencies

```bash
sudo apt update
sudo apt install -y python3 python3-pip ffmpeg
```

* `python3` and `pip`: required for Python-based tools.
* `ffmpeg`: used to merge and process audio/video files.

### 2. Install `yt-dlp`

#### Option A: Install via pip (Recommended)

```bash
python3 -m pip install -U yt-dlp
```

Ensure pip binaries are in your path:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Add the above line to your `~/.bashrc` or `~/.zshrc` to persist it.

#### Option B: Download the Binary

```bash
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp
```

## ▶️ Basic Usage

### Download a Single Video:

```bash
yt-dlp https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Download Best Quality:

```bash
yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 <url>
```

### Custom Output Filename:

```bash
yt-dlp -o '%(title)s.%(ext)s' <url>
```

## 📂 Downloading Playlists or Series

### Full Playlist Download:

```bash
yt-dlp -o '%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s' <playlist_url>
```

### Handling Authentication (User ID/Password):

```bash
yt-dlp -u <your_username> -p <your_password> <playlist_url>
```

Or use a `netrc` file for secure login:

```bash
yt-dlp --netrc <url>
```

**\~/.netrc** example:

```
machine youtube.com
login your_email@example.com
password your_password
```

## 🛠️ Optional Configuration File

Create at: `~/.config/yt-dlp/config`

Example content:

```
-f bestvideo+bestaudio
--merge-output-format mp4
-o ~/Videos/%(title)s.%(ext)s
--embed-thumbnail
--add-metadata
```

## 💡 Updating yt-dlp

Keep `yt-dlp` up-to-date with:

```bash
yt-dlp -U
```

## ✅ Recommendations

* Always use `-f bestvideo+bestaudio` to ensure high quality.
* Use `--embed-thumbnail --add-metadata` for organizing your media library.
* For series or courses: always use `-o '%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s'` to preserve order.
* If login is required, prefer `--netrc` or encrypted password manager over plain text.

## 📌 Resources

* Official Repo: [https://github.com/yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)
* Format selector help: `yt-dlp -F <video_url>`
* Embed subtitles: `--write-subs --sub-lang en --embed-subs`
