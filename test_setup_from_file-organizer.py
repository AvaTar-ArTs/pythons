#!/usr/bin/env python3
"""
Test script to verify the transcription analyzer setup
"""

import os


def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import whisper
        print("✅ whisper imported successfully")
    except ImportError as e:
        print(f"❌ whisper import failed: {e}")
        return False
    
    try:
        import moviepy
        print("✅ moviepy imported successfully")
    except ImportError as e:
        print(f"❌ moviepy import failed: {e}")
        return False
    
    try:
        from openai import OpenAI
        print("✅ openai imported successfully")
    except ImportError as e:
        print(f"❌ openai import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment configuration."""
    print("\nTesting environment...")
    
    # Load environment variables from ~/.env
    from dotenv import load_dotenv
    load_dotenv(os.path.expanduser("~/.env"))
    
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and api_key != 'your_openai_api_key_here':
        print("✅ OpenAI API key is configured")
        return True
    else:
        print("❌ OpenAI API key not configured")
        print("   Please set OPENAI_API_KEY in .env file")
        return False

def test_ffmpeg():
    """Test if FFmpeg is available."""
    print("\nTesting FFmpeg...")
    
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg is available")
            return True
        else:
            print("❌ FFmpeg not working properly")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ FFmpeg not found")
        print("   Please install FFmpeg for video processing")
        return False

def test_whisper_model():
    """Test if Whisper model can be loaded."""
    print("\nTesting Whisper model...")
    
    try:
        import whisper
        print("Loading Whisper model (this may take a moment)...")
        model = whisper.load_model("tiny")  # Use tiny for testing
        print("✅ Whisper model loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Whisper model loading failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Transcription Analyzer - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Environment", test_environment),
        ("FFmpeg", test_ffmpeg),
        ("Whisper Model", test_whisper_model)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 20)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with error: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("TEST RESULTS")
    print("=" * 50)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! The transcription analyzer is ready to use.")
        print("\nNext steps:")
        print("1. Add some MP3 or MP4 files to test with")
        print("2. Run: python transcription_analyzer.py your_file.mp4")
    else:
        print("\n⚠️  Some tests failed. Please address the issues above.")
        print("\nTroubleshooting:")
        print("1. Run: pip install -r requirements.txt")
        print("2. Install FFmpeg: brew install ffmpeg (macOS)")
        print("3. Set your OpenAI API key in .env file")

if __name__ == "__main__":
    main()