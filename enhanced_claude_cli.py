#!/usr/bin/env python3
"""
Enhanced Claude CLI for terminal usage
Usage: python enhanced_claude_cli.py "Your question here"

This enhanced version fixes issues in the original script and adds:
- Proper error handling
- Logging setup
- Constants definition
- Type hints
- Better input validation
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
            logging.FileHandler('claude_cli.log'),
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


def ask_claude(client, question: str, model: str, max_tokens: int = 4000):
    """Ask Claude a question and return the response"""
    try:
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": question}],
        )
        return response.content[0].text
    except Exception as e:
        return f"❌ Error: {e}"


def main():
    """Main function with proper error handling and constants."""
    # Load environment variables
    load_env_d()
    load_dotenv_fallback()

    # Check for API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("❌ Error: ANTHROPIC_API_KEY not found in environment variables")
        logger.info("💡 Add your API key to ~/.env file:")
        logger.info("   ANTHROPIC_API_KEY=your_key_here")
        sys.exit(1)

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Enhanced Claude CLI - Ask Claude questions from terminal"
    )
    parser.add_argument("question", nargs="?", help="Your question for Claude")
    parser.add_argument(
        "-m",
        "--model",
        default="claude-3-5-sonnet-20241022",  # Updated to latest model
        help="Claude model to use (default: claude-3-5-sonnet-20241022)",
    )
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="Start interactive mode"
    )
    parser.add_argument("-f", "--file", help="Read question from file")
    parser.add_argument(
        "-t", "--tokens", type=int, default=4000, help="Max tokens for response (default: 4000)"
    )

    args = parser.parse_args()

    # Import here to avoid dependency issues if not needed
    try:
        from anthropic import Anthropic
    except ImportError:
        logger.error("❌ anthropic package not installed. Install with: pip install anthropic")
        sys.exit(1)

    # Initialize Claude client
    try:
        client = Anthropic(api_key=api_key)
    except Exception as e:
        logger.error(f"❌ Error initializing Claude client: {e}")
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
        logger.info("🤖 Claude Interactive Mode (type 'quit', 'exit', or 'q' to exit)")
        logger.info("=" * 60)
        while True:
            try:
                question = input("\n💬 You: ").strip()
                if question.lower() in ["quit", "exit", "q"]:
                    logger.info("👋 Goodbye!")
                    break
                if not question:
                    continue
                response = ask_claude(client, question, args.model, args.tokens)
                logger.info(f"\n🤖 Claude: {response}")
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

    # Ask Claude
    response = ask_claude(client, question, args.model, args.tokens)
    print(response)  # Use print instead of logger for direct output


if __name__ == "__main__":
    main()