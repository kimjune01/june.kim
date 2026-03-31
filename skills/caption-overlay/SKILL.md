---
name: caption-overlay
description: Overlay a face-cam on a content video with auto-generated captions (shorts/reels format). Use when user wants to combine face video + content video with captions.
argument-hint: <face_video> <content_video> [options]
allowed-tools: Bash, Read, Write
---

# Caption Overlay - Shorts/Reels Pipeline

Run the `auto_shorts` CLI from the captain-caption project to overlay a face-cam video on a content video with auto-generated captions.

## Steps

1. Activate the captain-caption virtual environment:
   ```bash
   source /Users/junekim/Documents/captain-caption/.venv/bin/activate
   ```

2. Run the pipeline with the provided arguments:
   ```bash
   auto_shorts <face_video> <content_video> [options]
   ```

   Available options:
   - `-o, --output` — output file path (default: `<content>_short.mp4` in current dir)
   - `--face_scale` — face height as fraction of content height (default: 0.4)
   - `--whisper_model` — Whisper model for captions (default: small)
   - `--task` — transcribe or translate (default: transcribe)
   - `--language` — source language, auto for detection (default: auto)
   - `--skip_bg_removal true` — skip if face already has transparent background
   - `--skip_captions true` — just overlay, no captions

3. Report the output file path to the user when complete.

## Examples

```bash
auto_shorts ~/Downloads/face.mp4 ~/Downloads/gameplay.mp4 -o ~/Downloads/output_short.mp4
auto_shorts face.mov content.mp4 --face_scale 0.3 --whisper_model medium
auto_shorts face.mp4 content.mp4 --skip_bg_removal true
```
