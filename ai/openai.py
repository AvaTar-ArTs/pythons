"""
Openai Cli

This module provides functionality for openai cli.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_4000 = 4000

#!/Users/steven/miniforge3/bin/python
"""
Simple OpenAI CLI for terminal usage
Usage: python openai-cli.py "Your question here"
"""

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
    parser = argparse.ArgumentParser(description="OpenAI CLI - Ask GPT questions from terminal")
    parser.add_argument("question", nargs="?", help="Your question for GPT")
    parser.add_argument("-m", "--model", default="gpt-4o", help="OpenAI model to use (default: gpt-4o)")
    parser.add_argument("-i", "--interactive", action="store_true", help="Start interactive mode")
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
            model=model, messages=[{"role": "user", "content": question}], max_tokens=CONSTANT_4000, temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"


if __name__ == "__main__":
    main()
