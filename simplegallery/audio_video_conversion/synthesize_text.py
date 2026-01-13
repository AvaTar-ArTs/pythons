#!/usr/bin/env python3
"""
Local TTS System for As a Man Thinketh
Uses system TTS capabilities to create audio files
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Dict


class LocalTTSProvider:
    """Local TTS provider using system capabilities"""
    
    def __init__(self):
        self.output_dir = Path("as_a_man_thinketh_audio_local")
        self.output_dir.mkdir(exist_ok=True)
        self.setup_tts_engine()
    
    def setup_tts_engine(self):
        """Setup the TTS engine"""
        # Check available TTS engines
        self.engines = []
        
        # Check for say command (macOS)
        if subprocess.run(['which', 'say'], capture_output=True).returncode == 0:
            self.engines.append(('say', self.synthesize_say))
        
        # Check for espeak
        if subprocess.run(['which', 'espeak'], capture_output=True).returncode == 0:
            self.engines.append(('espeak', self.synthesize_espeak))
        
        # Check for festival
        if subprocess.run(['which', 'festival'], capture_output=True).returncode == 0:
            self.engines.append(('festival', self.synthesize_festival))
        
        print(f"Available TTS engines: {[e[0] for e in self.engines]}")
    
    def synthesize_say(self, text: str, output_path: str) -> bool:
        """Synthesize using macOS say command"""
        try:
            # Clean text for TTS
            clean_text = self.clean_text_for_tts(text)
            
            # Use say command with high quality voice
            cmd = [
                'say', 
                '-v', 'Samantha',  # High quality voice
                '-r', '180',       # Rate (words per minute)
                '-o', output_path,
                clean_text
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            print(f"Say error: {e}")
            return False
    
    def synthesize_espeak(self, text: str, output_path: str) -> bool:
        """Synthesize using espeak"""
        try:
            clean_text = self.clean_text_for_tts(text)
            
            cmd = [
                'espeak',
                '-s', '150',       # Speed
                '-v', 'en',        # Voice
                '-w', output_path,
                clean_text
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            print(f"Espeak error: {e}")
            return False
    
    def synthesize_festival(self, text: str, output_path: str) -> bool:
        """Synthesize using festival"""
        try:
            clean_text = self.clean_text_for_tts(text)
            
            # Create a temporary script for festival
            script_content = f'(voice_cmu_us_slt_arctic_hts) (SayText "{clean_text}")'
            script_file = output_path.replace('.wav', '.scm')
            
            with open(script_file, 'w') as f:
                f.write(script_content)
            
            cmd = ['festival', '--tts', script_file]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Clean up script file
            os.remove(script_file)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"Festival error: {e}")
            return False
    
    def clean_text_for_tts(self, text: str) -> str:
        """Clean text for TTS processing"""
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Fix common issues
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        text = text.replace('—', '-')
        
        # Limit length for TTS
        if len(text) > 1000:
            text = text[:1000] + "..."
        
        return text
    
    def synthesize_with_fallback(self, text: str, output_path: str) -> bool:
        """Try all engines until one works"""
        for engine_name, engine_func in self.engines:
            print(f"Trying {engine_name}...", end=" ")
            if engine_func(text, output_path):
                print("✓")
                return True
            else:
                print("✗")
        
        print("All engines failed")
        return False

class AsAManThinkethLocalTTS:
    """Local TTS system for As a Man Thinketh"""
    
    def __init__(self):
        self.tts = LocalTTSProvider()
        self.setup_chapters()
    
    def setup_chapters(self):
        """Setup chapters with real content"""
        # Load the real content
        with open('/tmp/as_a_man_thinketh_gutenberg.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        book_lines = lines[40:983]
        book_text = '\n'.join(book_lines)
        
        # Parse chapters
        self.chapters = self._parse_chapters(book_text)
        print(f"Loaded {len(self.chapters)} chapters")
    
    def _parse_chapters(self, book_text: str) -> Dict:
        """Parse chapters from the book text"""
        chapters = {}
        
        # Define chapter markers
        chapter_markers = [
            "THOUGHT AND CHARACTER",
            "EFFECT OF THOUGHT ON CIRCUMSTANCES", 
            "EFFECT OF THOUGHT ON HEALTH AND THE BODY",
            "THOUGHT AND PURPOSE",
            "THE THOUGHT-FACTOR IN ACHIEVEMENT",
            "VISIONS AND IDEALS",
            "SERENITY"
        ]
        
        # Split text into sections
        sections = book_text.split('\n\n')
        current_chapter = None
        current_content = []
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            # Check if this is a chapter header
            is_chapter_header = False
            for marker in chapter_markers:
                if marker in section.upper():
                    is_chapter_header = True
                    break
            
            if is_chapter_header:
                # Save previous chapter
                if current_chapter and current_content:
                    chapters[current_chapter] = {
                        'title': current_chapter.replace('_', ' ').title(),
                        'sections': current_content
                    }
                
                # Start new chapter
                current_chapter = section.lower().replace(' ', '_').replace('\n', '')
                current_content = []
            else:
                if current_chapter and len(section) > 50:  # Only add substantial content
                    current_content.append(section)
        
        # Add the last chapter
        if current_chapter and current_content:
            chapters[current_chapter] = {
                'title': current_chapter.replace('_', ' ').title(),
                'sections': current_content
            }
        
        return chapters
    
    def synthesize_chapter(self, chapter_key: str) -> bool:
        """Synthesize a chapter"""
        if chapter_key not in self.chapters:
            print(f"Chapter {chapter_key} not found")
            return False
        
        chapter = self.chapters[chapter_key]
        chapter_dir = self.tts.output_dir / chapter_key
        chapter_dir.mkdir(exist_ok=True)
        
        print(f"\nSynthesizing {chapter['title']}...")
        
        # Synthesize each section
        for i, section in enumerate(chapter['sections'], 1):
            section_file = chapter_dir / f"section_{i:02d}.wav"
            print(f"  Section {i}...", end=" ")
            
            if self.tts.synthesize_with_fallback(section, str(section_file)):
                print("✓")
            else:
                print("✗")
                return False
        
        print(f"✓ Chapter {chapter['title']} completed")
        return True
    
    def synthesize_all(self) -> bool:
        """Synthesize all chapters"""
        print("Starting synthesis of all chapters...")
        
        for chapter_key in self.chapters.keys():
            if not self.synthesize_chapter(chapter_key):
                print(f"Failed to synthesize {chapter_key}")
                return False
        
        print("\n🎉 All chapters synthesized successfully!")
        return True
    
    def list_chapters(self):
        """List all chapters"""
        print("\nAvailable chapters:")
        for key, chapter in self.chapters.items():
            print(f"  {key}: {chapter['title']} ({len(chapter['sections'])} sections)")

def main():
    """Main function"""
    try:
        tts_system = AsAManThinkethLocalTTS()
        
        if len(sys.argv) > 1:
            command = sys.argv[1]
            if command == "list":
                tts_system.list_chapters()
            elif command == "all":
                tts_system.synthesize_all()
            elif command in tts_system.chapters:
                tts_system.synthesize_chapter(command)
            else:
                print(f"Unknown command: {command}")
                print("Usage: python local_tts_system.py [list|all|<chapter_key>]")
        else:
            tts_system.list_chapters()
            choice = input("\nSynthesize all chapters? (y/N): ").strip().lower()
            if choice == 'y':
                tts_system.synthesize_all()
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()