#!/usr/bin/env python3

import os
import ssl
import urllib.request
import time
import threading
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
        self.processing_active = False
        
        # Create directories if they don't exist
        self.inputs_dir.mkdir(exist_ok=True)
        self.outputs_dir.mkdir(exist_ok=True)
    
    def load_model(self, model_size="base"):
        """Load Whisper model"""
        print(f"🔄 Loading Whisper {model_size} model...")
        print("   (This may take a moment on first run - downloading model)")
        self.model = whisper.load_model(model_size)
        print("✅ Model loaded successfully!")
    
    def show_progress_with_percentage(self, start_time, estimated_duration):
        """Show progress with percentage and time estimates"""
        dots = 0
        while self.processing_active:
            elapsed_time = time.time() - start_time
            
            # Calculate estimated progress (rough approximation)
            if estimated_duration > 0:
                estimated_progress = min(95, (elapsed_time / (estimated_duration * 60)) * 100)
                remaining_time = max(0, (estimated_duration * 60) - elapsed_time)
                
                print(f"\r🎤 Processing{'.' * (dots % 4)}{' ' * (3 - dots % 4)} "
                      f"~{estimated_progress:.0f}% complete, ~{remaining_time/60:.1f}min left", 
                      end="", flush=True)
            else:
                print(f"\r🎤 Processing{'.' * (dots % 4)}{' ' * (3 - dots % 4)} "
                      f"Elapsed: {elapsed_time/60:.1f}min", 
                      end="", flush=True)
            
            dots += 1
            time.sleep(2)  # Update every 2 seconds
    
    def get_file_duration_estimate(self, file_path):
        """Get rough estimate of file duration for time estimation"""
        try:
            # Get file size and estimate duration based on typical bitrates
            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            
            # Rough estimates based on typical audio/video bitrates
            if file_path.suffix.lower() in ['.mp3', '.wav', '.m4a', '.aac', '.ogg']:
                # Audio: ~1MB per minute for decent quality
                estimated_minutes = file_size_mb
            else:
                # Video: ~10-50MB per minute depending on quality
                estimated_minutes = file_size_mb / 20  # Conservative estimate
            
            return max(1, estimated_minutes)  # At least 1 minute
        except:
            return 5  # Default estimate if we can't determine
    
    def get_valid_files(self):
        """Get all valid audio/video files from Inputs folder"""
        if not self.inputs_dir.exists():
            return []
        
        valid_files = []
        for file_path in self.inputs_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                valid_files.append(file_path)
        
        return sorted(valid_files)
    
    def ask_timestamp_preference(self):
        """Ask user if they want timestamps in the transcript"""
        while True:
            choice = input("\n📝 Do you want timestamps in the transcript? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")

    def transcribe_file(self, file_path, include_timestamps=None):
        """Transcribe a single audio/video file with progress tracking"""
        try:
            print(f"\n{'='*60}")
            print(f"🎬 Transcribing: {file_path.name}")
            print(f"{'='*60}")
            
            # Get file info and estimates
            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            estimated_minutes = self.get_file_duration_estimate(file_path)
            
            print(f"📊 File size: {file_size_mb:.1f} MB")
            print(f"⏱️  Estimated duration: ~{estimated_minutes:.1f} minutes")
            print(f"⏳ Estimated processing time: ~{estimated_minutes * 0.5:.1f}-{estimated_minutes * 2:.1f} minutes")
            
            # Ask about timestamps if not specified
            if include_timestamps is None:
                include_timestamps = self.ask_timestamp_preference()
            
            print(f"\n🔄 Starting transcription...")
            print(f"📝 Output format: {'With timestamps' if include_timestamps else 'Plain text'}")
            
            # Start progress indicator with percentage
            self.processing_active = True
            progress_thread = threading.Thread(
                target=self.show_progress_with_percentage, 
                args=(time.time(), estimated_minutes * 1.5)  # Use 1.5x estimated time for processing
            )
            progress_thread.daemon = True
            progress_thread.start()
            
            # Record start time
            start_time = time.time()
            
            # Perform transcription
            result = self.model.transcribe(str(file_path))
            
            # Stop progress indicator
            self.processing_active = False
            progress_thread.join(timeout=1)
            
            # Calculate actual processing time
            processing_time = time.time() - start_time
            
            print(f"\r✅ Transcription completed in {processing_time:.1f} seconds!")
            print(f"📈 Processing speed: {estimated_minutes * 60 / processing_time:.1f}x real-time")
            
            # Print the transcription
            print("\n" + "="*60)
            print("📝 TRANSCRIPTION:")
            print("="*60)
            print(result["text"])
            print("="*60)
            
            # Save transcript based on user preference
            if include_timestamps and "segments" in result and result["segments"]:
                # Save with timestamps
                output_filename = f"{file_path.stem}_transcript_with_timestamps.txt"
                output_path = self.outputs_dir / output_filename
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    for segment in result["segments"]:
                        start_time = segment["start"]
                        end_time = segment["end"]
                        text = segment["text"].strip()
                        f.write(f"[{start_time:.2f}s - {end_time:.2f}s] {text}\n")
                
                print(f"\n💾 Transcript with timestamps saved to: {output_path}")
            else:
                # Save plain text
                output_filename = f"{file_path.stem}_transcript.txt"
                output_path = self.outputs_dir / output_filename
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(result["text"])
                
                print(f"\n💾 Plain text transcript saved to: {output_path}")
            
            return result["text"]
            
        except Exception as e:
            self.processing_active = False
            print(f"\r❌ Error transcribing {file_path.name}: {e}")
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
            
            # Ask about timestamps once for all files
            include_timestamps = self.ask_timestamp_preference()
            print(f"📝 Using {'timestamps' if include_timestamps else 'plain text'} for all files")
            
            total_start_time = time.time()
            
            for i, file_path in enumerate(valid_files, 1):
                print(f"\n📁 [{i}/{len(valid_files)}] Processing {file_path.name}...")
                self.transcribe_file(file_path, include_timestamps)
                
                # Show progress for batch processing
                if i < len(valid_files):
                    elapsed = time.time() - total_start_time
                    avg_time_per_file = elapsed / i
                    remaining_files = len(valid_files) - i
                    estimated_remaining = avg_time_per_file * remaining_files
                    
                    print(f"⏳ Batch progress: {i}/{len(valid_files)} complete")
                    print(f"📊 Estimated time remaining: {estimated_remaining/60:.1f} minutes")
        else:
            self.transcribe_file(choice)
        
        print(f"\n✅ Processing complete! Check the 'Outputs' folder for results.")

if __name__ == "__main__":
    transcriber = WhisperTranscriber()
    transcriber.run()
