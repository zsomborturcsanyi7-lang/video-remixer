# YouTube Video Creator — Automatic Video Remixer

**Version:** 1.0  
**Author:** Zsombi & Hermes Agent (Nous Research)  
**Status:** Working prototype

---

## Description

The **YouTube Video Creator** is an automatic video remixing tool that downloads, processes, and remixes YouTube videos. The program uses **yt-dlp** for downloading and **FFmpeg** for cutting, mixing, and applying effects. The project also includes a simple downloader utility (`simple_video_downloader.py`).

---

## File Structure

```
youtube video készitö/
│
├── video_remixer.py            # Main remixer program (235 lines)
├── simple_video_downloader.py  # Simple YouTube downloader
├── run_remixer.bat             # Windows launcher script
├── video_remixer_config.json   # Configuration file
└── requirements.txt            # Python dependencies
```

---

## Usage

### Quick Start

```bash
# Windows batch file
run_remixer.bat

# With URL parameter
run_remixer.bat "https://www.youtube.com/watch?v=..."
```

### Manual Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start remixer
python video_remixer.py

# Pass a URL
python video_remixer.py "https://www.youtube.com/watch?v=..."
```

### Configuration

The `video_remixer_config.json` file allows setting:

- `output_folder` — Output directory
- `temp_folder` — Temporary files directory
- `crafting_videos_folder` — Base videos directory
- YouTube API settings

---

## Workflow

1. **Video Search** — Search for popular videos on YouTube (API or URL)
2. **Download** — Using yt-dlp
3. **Processing** — FFmpeg cutting, mixing, effects
4. **Output** — Save new video to output folder

---

## Dependencies

### Python
- **Python** 3.8+
- **google-api-python-client** — YouTube API
- **google-auth-oauthlib** — Authentication
- **google-auth-httplib2** — HTTP transport
- **yt-dlp** — Download
- **FFmpeg** — Video processing (must be installed at system level)

### System
- **FFmpeg** (`ffmpeg` command available in PATH)
- **yt-dlp** (`yt-dlp` command)

---

## Developer

Zsombi & Hermes Agent (Nous Research)
