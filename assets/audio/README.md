# Background Music

Put fallback music files here:
- `assets/audio/background_01.mp3`
- `assets/audio/background_02.mp3`
- `assets/audio/background_03.mp3`
- `assets/audio/background_04.mp3`
- `assets/audio/background_05.mp3`
- `assets/audio/background_06.mp3`

Runtime behavior:
1. If source video has audio, original audio is used.
2. If source has no audio, one of `background_01~06.mp3` is selected randomly.
3. If none of the six files exist, fallback to `assets/audio/background.mp3`.
4. If that also does not exist, output is exported without audio.

Optional override:
- Set `BACKGROUND_MUSIC_FILE` to force a specific file path.

Emoji compatibility note:
- Country flag emoji is used in YouTube metadata title only.
- Emoji is intentionally not used in FFmpeg subtitle overlays to avoid font/rendering compatibility issues.
