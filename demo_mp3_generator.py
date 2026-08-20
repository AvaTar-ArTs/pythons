#!/usr/bin/env python3
"""
AlchemyAPI Demo MP3 Generator
Creates demo MP3 files for the AlchemyAPI showcase
"""

import csv
import os

from pydub import AudioSegment
from pydub.generators import Sine


def create_demo_mp3(question_text, output_path, duration=15):
    """
    Creates a demo MP3 file with a tone and silence
    """
    # Create a short tone at the beginning
    tone = Sine(440).to_audio_segment(duration=1000)  # 1 second tone
    
    # Create silence for the rest
    silence_duration = (duration * 1000) - 1000  # Convert to milliseconds
    silence = AudioSegment.silent(duration=silence_duration)
    
    # Combine tone and silence
    audio = tone + silence
    
    # Export as MP3
    audio.export(output_path, format="mp3")
    print(f"🎵 Created demo MP3: {os.path.basename(output_path)}")

def process_quiz_demo(csv_path, output_folder, duration=15):
    """
    Processes quiz CSV and creates demo MP3 files
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"📁 Created output folder: {output_folder}")

    print(f"📊 Processing quiz from: {csv_path}")
    
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        questions = list(reader)
        
    print(f"📝 Found {len(questions)} questions to process")
    
    for i, row in enumerate(questions):
        question = row["Question"]
        options = ", ".join([f"{opt}: {row[opt]}" for opt in ["A", "B", "C", "D"] if opt in row])
        correct_answer = row["Correct"]

        # Create demo text
        demo_text = f"Question {i+1}: {question} Options: {options} Correct answer: {correct_answer}"

        output_path = os.path.join(output_folder, f"question_{i+1:02d}.mp3")
        create_demo_mp3(demo_text, output_path, duration)
        
        print(f"✅ Processed question {i + 1}/{len(questions)}")
        print("-" * 50)

def main():
    """Main execution function"""
    print("🔮 AlchemyAPI Demo MP3 Generator")
    print("=" * 50)
    
    # Define paths
    csv_path = "/Users/steven/tehSiTes/AlchemyAPI/quiz_sample.csv"
    output_folder = "/Users/steven/tehSiTes/AlchemyAPI/demo_mp3s"
    
    # Check if CSV exists
    if not os.path.exists(csv_path):
        print(f"❌ Quiz CSV file not found: {csv_path}")
        return False
    
    # Process the quiz and generate demo MP3s
    try:
        process_quiz_demo(csv_path, output_folder, duration=15)
        print("\n🎉 Demo MP3 generation completed successfully!")
        print(f"📁 Check the output folder: {output_folder}")
        
        # List generated files
        files = os.listdir(output_folder)
        print(f"\n📁 Generated {len(files)} MP3 files:")
        for file in sorted(files):
            if file.endswith('.mp3'):
                file_path = os.path.join(output_folder, file)
                file_size = os.path.getsize(file_path)
                print(f"  - {file} ({file_size} bytes)")
        
        return True
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        return False

if __name__ == "__main__":
    success = main()