"""
Simple OpenAI CLI for terminal usage
Usage: python openai-cli.py "Your question here"
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
                            value = value.strip().strip("'").strip("'")
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
from openai import OpenAI


def main():
    """main function."""

    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.info("❌ Error: OPENAI_API_KEY not found in environment variables")
        logger.info("💡 Add your API key to ~/.env file:")
        logger.info("   OPENAI_API_KEY=your_key_here")
        sys.exit(1)

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="OpenAI CLI - Ask GPT questions from terminal"
    )
    parser.add_argument("question", nargs="?", help="Your question for GPT")
    parser.add_argument(
        "-m", "--model", default="gpt-4o", help="OpenAI model to use (default: gpt-4o)"
    )
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="Start interactive mode"
    )
    parser.add_argument("-f", "--file", help="Read question from file")

    args = parser.parse_args()

    # Initialize OpenAI client
    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        logger.info(f"❌ Error initializing OpenAI client: {e}")
        sys.exit(1)

    # Get question
    if args.file:
        try:
            with open(args.file, "r") as f:
                question = f.read().strip()
        except FileNotFoundError:
            logger.info(f"❌ Error: File '{args.file}' not found")
            sys.exit(1)
    elif args.interactive:
        logger.info("🤖 OpenAI Interactive Mode (type 'quit' to exit)")
        logger.info("=" * 50)
        while True:
            try:
                question = input("\n💬 You: ").strip()
                if question.lower() in ["quit", "exit", "q"]:
                    logger.info("👋 Goodbye!")
                    break
                if not question:
                    continue
                response = ask_openai(client, question, args.model)
                logger.info(f"\n🤖 GPT: {response}")
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
            logger.info("❌ No question provided")
            parser.print_help()
            sys.exit(1)

    # Ask OpenAI
    response = ask_openai(client, question, args.model)
    logger.info(response)


def ask_openai(client, question, model):
    """Ask OpenAI a question and return the response"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": question}],
            max_tokens=CONSTANT_4000,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"


if __name__ == "__main__":
    main()
