# Background Music

Put your fallback music file here:
- `assets/audio/background.mp3`

Behavior in `scripts/full_auto_youtube.py`:
1. If source video has audio, keep source audio.
2. If source video has no audio and `background.mp3` exists, use it.
3. If both are missing, output video without audio.

Optional override:
- Set env var `BACKGROUND_MUSIC_FILE` to a custom relative/absolute path.

Note:
- YouTube Studio Audio Library does not provide a public API for automatic track fetching in this workflow.
- Download the music manually and place it as `background.mp3`.
