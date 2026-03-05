# Wonders of Street View

Daily travel shorts pipeline that builds a 60-second vertical video from free footage and uploads it to YouTube.

## Overview
- Picks a random destination from `config/locations.json` (now **60 locations**)
- Searches free stock video via Pexels API
- Creates a Shorts-ready 1080x1920 video with subtitle overlay
- Audio behavior:
  - If source video has audio: keep it
  - If source video has no audio: use `assets/audio/background.mp3` (or `BACKGROUND_MUSIC_FILE`)
  - If neither exists: export without audio
- Uploads to YouTube via YouTube Data API
- Cleans temporary files and stores metadata/log artifacts

## Active Workflow
- File: `.github/workflows/youtube-auto-upload.yml`
- Schedule: `0 0 * * *` (daily 00:00 UTC / 09:00 KST)
- Manual run: `workflow_dispatch` enabled

## Required Secrets
- `PEXELS_API_KEY`
- `YOUTUBE_TOKEN_BASE64`

## Optional Settings
- `BACKGROUND_MUSIC_FILE`
  - Relative or absolute path to background music mp3
  - Default: `assets/audio/background.mp3`

## Local Run
```bash
python3 scripts/full_auto_youtube.py
```

## Project Structure
- `config/locations.json` : destination database (60 records)
- `scripts/full_auto_youtube.py` : end-to-end generation + upload
- `assets/audio/README.md` : background music setup
- `.github/workflows/youtube-auto-upload.yml` : scheduler workflow
- `docs/DOCS_INDEX.md` : documentation map

## Notes
- Legacy workflows are stored in `workflows/legacy/`.
- Older docs are archived in `docs/archive/`.
