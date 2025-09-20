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

> **Note**: This is the only transcription script you need. The old `simple_transcribe.py` and `transcribe.py` files have been removed as they were outdated and less functional.

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
- 🎤 **Live Progress**: Percentage complete with time remaining (updates every 2 seconds)
- ⚡ **Performance Stats**: Actual processing time and speed (e.g., "3.2x real-time")
- 📈 **Batch Progress**: Progress tracking for multiple files with time remaining estimates
- 📝 **Smart Output**: Choose timestamp format once, applies to all files

Example output:
```
🎬 Transcribing: meeting.mp3
📊 File size: 15.2 MB
⏱️  Estimated duration: ~15.1 minutes
⏳ Estimated processing time: ~7.6-30.2 minutes
📝 Do you want timestamps in the transcript? (y/n): y
🔄 Starting transcription...
📝 Output format: With timestamps
🎤 Processing.... ~45% complete, ~8.3min left
✅ Transcription completed in 180.5 seconds!
📈 Processing speed: 5.0x real-time
💾 Transcript with timestamps saved to: Outputs/meeting_transcript_with_timestamps.txt
```

## Supported File Formats

- **Audio**: MP3, WAV, M4A, AAC, OGG, WMA, FLAC
- **Video**: MP4, AVI, MOV, MKV

## Scripts

- `smart_transcribe.py` - **Main Script**: Interactive file selection, progress tracking, and batch processing

## 📝 **Complete Meeting Notes Workflow**

### **Step 1: Record Your Meeting**

#### **Online Meetings:**
- **Zoom**: Use built-in recording feature (saves as MP4/MP3)
- **Teams**: Record meeting → Download recording
- **Google Meet**: Use record feature → Export as MP4
- **Discord**: Use bot like Craig or OBS Studio
- **Any platform**: Use screen recording software (OBS, QuickTime, etc.)

#### **Offline/In-Person:**
- **Phone**: Use voice memo app (iPhone Voice Memos, Android Recorder)
- **Dictaphone**: Traditional voice recorder
- **Laptop**: Use built-in microphone with recording software
- **External mic**: Connect USB microphone for better quality

### **Step 2: Process Recordings**

1. **Clone this repository:**
   ```bash
   git clone https://github.com/myermcat/whisper-ai-transcriber.git
   cd whisper-ai-transcriber
   ```

2. **Add recordings to Inputs folder:**
   - Copy your audio/video files to the `Inputs/` folder
   - Supports: MP3, MP4, WAV, M4A, AAC, OGG, WMA, FLAC, AVI, MOV, MKV

3. **Run the transcription:**
   ```bash
   python3 smart_transcribe.py
   ```
   
   The script will:
   - Show you available files
   - Ask if you want timestamps (choose once for batch processing)
   - Process your selection with progress tracking
   - Save transcripts to `Outputs/` folder

### **Step 3: Generate Meeting Notes**

4. **Use AI for meeting summaries:**
   - Copy transcript content from `Outputs/` folder
   - Paste into ChatGPT, Claude, or any AI assistant
   - Use prompt: `"Please analyze this meeting transcript and create structured meeting notes with: 1) Key decisions made, 2) Action items with owners, 3) Important discussions, 4) Next steps. Format as a professional meeting summary."`

5. **Process multiple files:**
   - For multiple recordings, process them one at a time with AI
   - This gives better results than combining all transcripts

### **Pro Tips:**
- 🎤 **Better audio = better transcription** (use good microphone, reduce background noise)
- 📁 **Organize files** by date/meeting name before processing
- ⏱️ **Timestamps help** when referencing specific discussion points
- 🤖 **AI works best** with one transcript at a time for detailed analysis

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
