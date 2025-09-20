#!/usr/bin/env python3

import ssl
import urllib.request

# Disable SSL verification before importing whisper
ssl._create_default_https_context = ssl._create_unverified_context

# Now import whisper
import whisper

def transcribe_audio(audio_file):
    """Transcribe audio file using Whisper"""
    try:
        print("Loading Whisper base model...")
        model = whisper.load_model("base")
        
        print(f"Transcribing: {audio_file}")
        result = model.transcribe(audio_file)
        
        # Print the transcription
        print("\n" + "="*60)
        print("TRANSCRIPTION:")
        print("="*60)
        print(result["text"])
        print("="*60)
        
        # Save to text file
        output_file = audio_file.replace('.m4a', '_transcript.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result["text"])
        
        print(f"\nTranscript saved to: {output_file}")
        
        return result["text"]
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    audio_file = "CEGSA Meeting with Daniel thorp September 12.m4a"
    transcribe_audio(audio_file)
