#!/usr/bin/env python3
'\''
Transcript Analyzer
===================
Analyzes an existing text file (transcript) using OpenAI's GPT models.
Useful for re-analyzing transcripts without re-transcribing the audio.
"""

# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)
from pathlib import Path as PathLib

def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip(""").strip("\'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")

load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from termcolor import colored

# Load environment variables
load_dotenv(Path.home() / ".env")
    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)

def setup_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(colored("❌ Error: OPENAI_API_KEY not found.", "red"))
        sys.exit(1)
    return OpenAI(api_key=api_key)

def analyze_text(client, text, model="gpt-4o"):
    system_prompt = (
        "You are an expert lyric analyst. Provide a deep, structured analysis of the provided text, "
        "focusing on themes, emotion, imagery, and narrative arc."
    )
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Please analyze this transcript:\n\n{text}"}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(colored(f"❌ API Error: {e}", "red"))
        return None

def main():
    parser = argparse.ArgumentParser(description="Analyze text transcripts with AI.")
    parser.add_argument("input_file", help="Path to the text file to analyze.")
    parser.add_argument("-m", "--model", default="gpt-4o", help="Model to use (default: gpt-4o).")
    parser.add_argument("-o", "--output", help="Output file path (optional).")
    
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(colored(f"❌ File not found: {input_path}", "red"))
        sys.exit(1)
        
    print(colored(f"📖 Reading: {input_path.name}", "cyan"))
    text = input_path.read_text(encoding="utf-8")
    
    client = setup_client()
    
    print(colored(f"🧠 Analyzing with {args.model}...", "blue"))
    analysis = analyze_text(client, text, args.model)
    
    if analysis:
        if args.output:
            out_path = Path(args.output)
        else:
            out_path = input_path.with_name(f"{input_path.stem}_analysis_standalone.txt")
            
        out_path.write_text(analysis, encoding="utf-8")
        print(colored(f"✅ Analysis saved to: {out_path}", "green"))
    else:
        print(colored("⚠️ Analysis failed.", "yellow"))

if __name__ == "__main__":
    main()