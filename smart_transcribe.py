#!/usr/bin/env python3

import os
import ssl
import urllib.request
from pathlib import Path

# Disable SSL verification before importing whisper
ssl._create_default_https_context = ssl._create_unverified_context

# Now import whisper
import whisper

class WhisperTranscriber:
    def __init__(self):
        self.model = None
        self.supported_formats = {'.mp3', '.mp4', '.wav', '.m4a', '.aac', '.ogg', '.wma', '.flac', '.avi', '.mov', '.mkv'}
        self.inputs_dir = Path("Inputs")
        self.outputs_dir = Path("Outputs")
        
        # Create directories if they don't exist
        self.inputs_dir.mkdir(exist_ok=True)
        self.outputs_dir.mkdir(exist_ok=True)
    
    def load_model(self, model_size="base"):
        """Load Whisper model"""
        print(f"Loading Whisper {model_size} model...")
        self.model = whisper.load_model(model_size)
        print("Model loaded successfully!")
    
    def get_valid_files(self):
        """Get all valid audio/video files from Inputs folder"""
        if not self.inputs_dir.exists():
            return []
        
        valid_files = []
        for file_path in self.inputs_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                valid_files.append(file_path)
        
        return sorted(valid_files)
    
    def transcribe_file(self, file_path):
        """Transcribe a single audio/video file"""
        try:
            print(f"\n{'='*60}")
            print(f"Transcribing: {file_path.name}")
            print(f"{'='*60}")
            
            result = self.model.transcribe(str(file_path))
            
            # Print the transcription
            print("\nTRANSCRIPTION:")
            print("-" * 40)
            print(result["text"])
            print("-" * 40)
            
            # Save to text file in Outputs folder
            output_filename = f"{file_path.stem}_transcript.txt"
            output_path = self.outputs_dir / output_filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result["text"])
            
            print(f"\nTranscript saved to: {output_path}")
            
            # Also save with timestamps if available
            if "segments" in result and result["segments"]:
                timestamp_filename = f"{file_path.stem}_transcript_with_timestamps.txt"
                timestamp_path = self.outputs_dir / timestamp_filename
                
                with open(timestamp_path, 'w', encoding='utf-8') as f:
                    for segment in result["segments"]:
                        start_time = segment["start"]
                        end_time = segment["end"]
                        text = segment["text"].strip()
                        f.write(f"[{start_time:.2f}s - {end_time:.2f}s] {text}\n")
                
                print(f"Transcript with timestamps saved to: {timestamp_path}")
            
            return result["text"]
            
        except Exception as e:
            print(f"Error transcribing {file_path.name}: {e}")
            return None
    
    def show_file_selection_menu(self, files):
        """Show interactive file selection menu"""
        print(f"\nFound {len(files)} valid file(s) in Inputs folder:")
        print("-" * 50)
        
        for i, file_path in enumerate(files, 1):
            file_size = file_path.stat().st_size / (1024 * 1024)  # Size in MB
            print(f"{i}. {file_path.name} ({file_size:.1f} MB)")
        
        print(f"0. Process all files")
        print(f"{len(files) + 1}. Exit")
        
        while True:
            try:
                choice = input(f"\nChoose an option (0-{len(files) + 1}): ").strip()
                choice_num = int(choice)
                
                if choice_num == 0:
                    return "all"
                elif 1 <= choice_num <= len(files):
                    return files[choice_num - 1]
                elif choice_num == len(files) + 1:
                    return "exit"
                else:
                    print(f"Please enter a number between 0 and {len(files) + 1}")
            except ValueError:
                print("Please enter a valid number")
    
    def run(self):
        """Main execution function"""
        print("🎤 Whisper AI Transcriber")
        print("=" * 40)
        
        # Check for valid files
        valid_files = self.get_valid_files()
        
        if not valid_files:
            print("❌ No valid audio/video files found in Inputs folder.")
            print(f"Supported formats: {', '.join(sorted(self.supported_formats))}")
            print("\nPlease add audio/video files to the 'Inputs' folder and try again.")
            return
        
        # Load model
        self.load_model()
        
        # Handle single file case
        if len(valid_files) == 1:
            file_path = valid_files[0]
            response = input(f"\n📁 Found one file: {file_path.name}\nDo you want to process it? (y/n): ").strip().lower()
            
            if response in ['y', 'yes']:
                self.transcribe_file(file_path)
            else:
                print("Processing cancelled.")
            return
        
        # Handle multiple files case
        choice = self.show_file_selection_menu(valid_files)
        
        if choice == "exit":
            print("Goodbye!")
            return
        
        if choice == "all":
            print(f"\n🔄 Processing all {len(valid_files)} files...")
            for i, file_path in enumerate(valid_files, 1):
                print(f"\n[{i}/{len(valid_files)}] Processing {file_path.name}...")
                self.transcribe_file(file_path)
        else:
            self.transcribe_file(choice)
        
        print(f"\n✅ Processing complete! Check the 'Outputs' folder for results.")

if __name__ == "__main__":
    transcriber = WhisperTranscriber()
    transcriber.run()
