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

> ⚠️ Debian 12 uses an **externally-managed environment** for Python. Direct use of `pip` may fail with an error like `externally-managed-environment`. Work around this using either of these methods:

##### 📦 Method 1: Use a Python Virtual Environment

```bash
python3 -m venv ~/.venvs/yt-dlp
source ~/.venvs/yt-dlp/bin/activate
pip install -U yt-dlp
```

Then run:

```bash
~/.venvs/yt-dlp/bin/yt-dlp <url>
```

##### 📦 Method 2: Use pipx (clean and isolated)

```bash
sudo apt install pipx
pipx install yt-dlp
```

To run:

```bash
yt-dlp <url>
```

##### ⚠️ Avoid `--break-system-packages`

While possible with:

```bash
python3 -m pip install --break-system-packages -U yt-dlp
```

It’s **not recommended**, as it can break Debian’s Python system.

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

### 🚫 Handling 403 Forbidden or Redirect Errors

If you encounter:

```
ERROR: unable to download video data: HTTP Error 403: Forbidden
```

OR

```
ERROR: Unsupported URL: https://www.youtube.com/watch%5C%5C=...
```

Follow these steps:

✅ **Fix URL formatting**: Ensure the URL is properly quoted and not malformed. Avoid copy-pasting with `\` or extra characters. Example:

```bash
yt-dlp "https://www.youtube.com/watch?v=HfNKpT2jo7U"
```

✅ **Avoid smart quotes or shell escaping errors**.

✅ **Use cookies from your browser**:

```bash
yt-dlp --cookies-from-browser firefox "https://www.youtube.com/watch?v=HfNKpT2jo7U"
```

✅ **Still blocked? Use cookies.txt manually**:

1. Install [cookies.txt extension](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)
2. Export cookies to a file:

```bash
yt-dlp --cookies cookies.txt "https://www.youtube.com/watch?v=HfNKpT2jo7U"
```

✅ **Try with login credentials**:

```bash
yt-dlp -u your_email@gmail.com -p your_password "https://www.youtube.com/watch?v=HfNKpT2jo7U"
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
--cookies-from-browser firefox
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
* If login is required, prefer `--netrc`, `--cookies`, or `--cookies-from-browser` to bypass restrictions.
* Check your terminal for copy/paste errors, smart quotes, or malformed URLs.
* Use `pipx` or a virtual environment to safely manage Python packages in Debian 12.

## 📌 Resources

* Official Repo: [https://github.com/yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)
* Format selector help: `yt-dlp -F <video_url>`
* Embed subtitles: `--write-subs --sub-lang en --embed-subs`
   