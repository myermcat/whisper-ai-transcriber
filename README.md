# Whisper AI Transcriber

A smart transcription tool that uses OpenAI's Whisper AI to transcribe audio and video files.

## 🆓 **Completely FREE!**

**Whisper AI is 100% free and does NOT use your OpenAI credits!**
- ✅ **Local Processing**: Runs entirely on your computer
- ✅ **No Internet Required**: Works offline after initial model download
- ✅ **No API Calls**: No server requests or usage limits
- ✅ **Open Source**: Free forever, no subscriptions

## Features

- 🎯 **Smart File Detection**: Automatically finds audio/video files in the `Inputs` folder
- 🎬 **Multiple Formats**: Supports MP3, MP4, WAV, M4A, AAC, OGG, WMA, FLAC, AVI, MOV, MKV
- 📝 **Interactive Selection**: Choose specific files or process all at once
- ⏱️ **Timestamps**: Generates transcripts with and without timestamps
- 📁 **Organized Output**: Saves results in the `Outputs` folder
- 📊 **Progress Tracking**: Real-time progress indicators and time estimates
- 🚀 **Performance Stats**: Shows processing speed and completion times

## Setup

1. Make sure you have Python 3 installed
2. Install Whisper: `pip install openai-whisper`
3. Add your audio/video files to the `Inputs` folder
4. Run the transcription script

## Usage

### Quick Start
```bash
python3 smart_transcribe.py
```

### How It Works

1. **No Files**: If the `Inputs` folder is empty or contains no valid audio/video files, the script will inform you and list supported formats.

2. **Single File**: If there's one valid file, you'll be asked:
   ```
   📁 Found one file: example.mp3
   Do you want to process it? (y/n):
   ```

3. **Multiple Files**: If there are multiple files, you'll see a menu:
   ```
   Found 3 valid file(s) in Inputs folder:
   --------------------------------------------------
   1. meeting1.mp3 (5.2 MB)
   2. interview.m4a (12.1 MB)
   3. lecture.mp4 (45.8 MB)
   0. Process all files
   4. Exit

   Choose an option (0-4):
   ```

## Output

The script creates two types of output files in the `Outputs` folder:

1. **Basic Transcript**: `filename_transcript.txt` - Clean text transcription
2. **Timestamped Transcript**: `filename_transcript_with_timestamps.txt` - Includes timing information

## Progress Tracking

The script now shows detailed progress information:

- 📊 **File Analysis**: File size and estimated duration
- ⏳ **Time Estimates**: Estimated processing time before starting
- 🎤 **Live Progress**: Animated progress dots during processing
- ⚡ **Performance Stats**: Actual processing time and speed (e.g., "3.2x real-time")
- 📈 **Batch Progress**: Progress tracking for multiple files with time remaining estimates

Example output:
```
🎬 Transcribing: meeting.mp3
📊 File size: 15.2 MB
⏱️  Estimated duration: ~15.1 minutes
⏳ Estimated processing time: ~7.6-30.2 minutes
🔄 Starting transcription...
🎤 Processing....
✅ Transcription completed in 180.5 seconds!
📈 Processing speed: 5.0x real-time
```

## Supported File Formats

- **Audio**: MP3, WAV, M4A, AAC, OGG, WMA, FLAC
- **Video**: MP4, AVI, MOV, MKV

## Scripts

- `smart_transcribe.py` - **Recommended**: Interactive file selection and processing
- `simple_transcribe.py` - Basic transcription script
- `transcribe.py` - Alternative transcription script

## Requirements

- Python 3.7+
- openai-whisper
- FFmpeg (for video processing)

## Installation

```bash
pip install openai-whisper
```

For video support, you may also need FFmpeg:
- **macOS**: `brew install ffmpeg`
- **Windows**: Download from https://ffmpeg.org/
- **Linux**: `sudo apt install ffmpeg`
