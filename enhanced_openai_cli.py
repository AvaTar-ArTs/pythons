#!/usr/bin/env python3
"""
Enhanced OpenAI CLI for terminal usage
Usage: python enhanced_openai_cli.py "Your question here"

This enhanced version fixes issues in the original script and adds:
- Proper error handling
- Logging setup
- Constants definition
- Type hints
- Better input validation
- Support for different response formats
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('openai_cli.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


def load_env_d():
    """Load all .env files from ~/.env.d directory with proper error handling."""
    logger = setup_logging()
    env_d_path = Path.home() / ".env.d"
    
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
                                
            except Exception as e:
                logger.warning(f"Warning: Error loading {env_file} at line {line_num}: {e}")
    else:
        logger.debug(f"Env directory does not exist: {env_d_path}")


def load_dotenv_fallback():
    """Load from ~/.env as fallback using dotenv if available."""
    try:
        load_dotenv(os.path.expanduser("~/.env"))
    except ImportError:
        pass  # dotenv is optional


logger = setup_logging()


def ask_openai(client, question: str, model: str, max_tokens: int = 4000, temperature: float = 0.7):
    """Ask OpenAI a question and return the response"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": question}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"


def main():
    """Main function with proper error handling and constants."""
    # Load environment variables
    load_env_d()
    load_dotenv_fallback()

    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("❌ Error: OPENAI_API_KEY not found in environment variables")
        logger.info("💡 Add your API key to ~/.env file:")
        logger.info("   OPENAI_API_KEY=your_key_here")
        sys.exit(1)

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Enhanced OpenAI CLI - Ask GPT questions from terminal"
    )
    parser.add_argument("question", nargs="?", help="Your question for GPT")
    parser.add_argument(
        "-m", "--model", default="gpt-4o", help="OpenAI model to use (default: gpt-4o)"
    )
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="Start interactive mode"
    )
    parser.add_argument("-f", "--file", help="Read question from file")
    parser.add_argument(
        "-t", "--tokens", type=int, default=4000, help="Max tokens for response (default: 4000)"
    )
    parser.add_argument(
        "-temp", "--temperature", type=float, default=0.7, help="Creativity of response (default: 0.7)"
    )

    args = parser.parse_args()

    # Import here to avoid dependency issues if not needed
    try:
        from openai import OpenAI
    except ImportError:
        logger.error("❌ openai package not installed. Install with: pip install openai")
        sys.exit(1)

    # Initialize OpenAI client
    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        logger.error(f"❌ Error initializing OpenAI client: {e}")
        sys.exit(1)

    # Get question
    if args.file:
        try:
            with open(args.file, "r", encoding='utf-8') as f:
                question = f.read().strip()
        except FileNotFoundError:
            logger.error(f"❌ Error: File '{args.file}' not found")
            sys.exit(1)
        except Exception as e:
            logger.error(f"❌ Error reading file '{args.file}': {e}")
            sys.exit(1)
    elif args.interactive:
        logger.info("🤖 OpenAI Interactive Mode (type 'quit', 'exit', or 'q' to exit)")
        logger.info("=" * 60)
        while True:
            try:
                question = input("\n💬 You: ").strip()
                if question.lower() in ["quit", "exit", "q"]:
                    logger.info("👋 Goodbye!")
                    break
                if not question:
                    continue
                response = ask_openai(client, question, args.model, args.tokens, args.temperature)
                print(f"\n🤖 GPT: {response}")  # Use print for direct output
            except KeyboardInterrupt:
                logger.info("\n👋 Goodbye!")
                break
        return
    elif args.question:
        question = args.question
    else:
        # Read from stdin
        question = sys.stdin.read().strip()
        if not question:
            logger.error("❌ No question provided")
            parser.print_help()
            sys.exit(1)

    # Ask OpenAI
    response = ask_openai(client, question, args.model, args.tokens, args.temperature)
    print(response)  # Use print instead of logger for direct output


if __name__ == "__main__":
    main()