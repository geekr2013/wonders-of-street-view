# Wonders of Street View

Daily travel shorts pipeline for YouTube growth and monetization readiness.

## What This Version Improves
- English-first titles/descriptions/tags with country flag emoji in title metadata
- Multi-template packaging to reduce repetitive patterns
- Series-based content strategy:
  - `City Walks`
  - `History Trails`
  - `Nature Escapes`
- Source attribution logging (`logs/source_log.jsonl`)
- 60 destinations in `config/locations.json`

## Active Workflow
- `.github/workflows/youtube-auto-upload.yml`
- Schedule: `0 0 * * *` (daily 00:00 UTC / 09:00 KST)
- Manual run: enabled (`workflow_dispatch`)

## Required Secrets
- `PEXELS_API_KEY`
- `YOUTUBE_TOKEN_BASE64`

## Optional Environment Variables
- `BACKGROUND_MUSIC_FILE`
  - Optional override for a specific fallback track
  - If not set, random selection from `assets/audio/background_01.mp3` to `background_06.mp3`
  - If none exist, fallback to `assets/audio/background.mp3`

## Content and Attribution Outputs
- Final video: `output/*_short_*.mp4`
- Metadata JSON: `output/*_metadata.json`
- Source log: `logs/source_log.jsonl`

## Core Script
- `scripts/full_auto_youtube.py`
  - Select location
  - Build series-aware metadata package
  - Fetch source video from Pexels
  - Compose short with overlay hook + subtitle
  - Keep source audio or apply fallback BGM
  - Upload to YouTube
  - Save metadata and source attribution log

## Notes
- Legacy workflows are in `workflows/legacy/`.
- Archived docs are in `docs/archive/`.
