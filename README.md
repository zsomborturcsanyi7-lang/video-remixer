# video-remixer

Automated video downloading and processing tool driven by FFmpeg and yt-dlp.

## Overview & Purpose
video-remixer provides programmatic automation for fetching online video streams, extracting audio layers, applying audio effects, and splicing clips into custom video remixes.

## Key Features
- High-efficiency video downloading using `yt-dlp`.
- Automated audio track swapping and overlay mixing.
- Customizable vágó and concatenation workflows using FFmpeg subprocesses.
- CLI arguments for batch job processing.

## Tech Stack & Dependencies
- **Language**: Python 3.9+
- **Media Engine**: FFmpeg
- **Downloader**: yt-dlp

## Project Structure
```text
video-remixer/
├── remixer.py
├── video_remixer_config.json
├── requirements.txt
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.9+
- FFmpeg installed and added to environment PATH

### Steps
```bash
git clone https://github.com/zsomborturcsanyi7-lang/video-remixer.git
cd video-remixer

pip install -r requirements.txt
```

## Usage Examples
```bash
python remixer.py --url "https://youtube.com/watch?v=EXAMPLE" --output remix.mp4
```

## Status & License
Status: Functional Script.
License: MIT
