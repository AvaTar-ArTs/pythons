"""
Groq Cli

This module provides functionality for groq cli.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_4000 = 4000

#!/Users/steven/miniforge3/bin/python
"""
Simple Groq CLI for terminal usage
Usage: python groq-cli.py "Your question here"
"""

import os
import sys
import argparse
from groq import Groq


def main():
    """main function."""

    # Check for API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.info("❌ Error: GROQ_API_KEY not found in environment variables")
        logger.info("💡 Add your API key to ~/.env file:")
        logger.info("   GROQ_API_KEY=your_key_here")
        sys.exit(1)

    # Parse arguments
    parser = argparse.ArgumentParser(description="Groq CLI - Ask Groq questions from terminal")
    parser.add_argument("question", nargs="?", help="Your question for Groq")
    parser.add_argument(
        "-m", "--model", default="llama-3.3-70b-versatile", help="Groq model to use (default: llama-3.3-70b-versatile)"
    )
    parser.add_argument("-i", "--interactive", action="store_true", help="Start interactive mode")
    parser.add_argument("-f", "--file", help="Read question from file")
    parser.add_argument("--list-models", action="store_true", help="List available models")

    args = parser.parse_args()

    # Initialize Groq client
    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        logger.info(f"❌ Error initializing Groq client: {e}")
        sys.exit(1)

    # List models if requested
    if args.list_models:
        list_models(client)
        return

    # Get question
    if args.file:
        try:
            with open(args.file, "r") as f:
                question = f.read().strip()
        except FileNotFoundError:
            logger.info(f"❌ Error: File '{args.file}' not found")
            sys.exit(1)
    elif args.interactive:
        logger.info("🚀 Groq Interactive Mode (type 'quit' to exit)")
        logger.info("=" * 50)
        while True:
            try:
                question = input("\n💬 You: ").strip()
                if question.lower() in ["quit", "exit", "q"]:
                    logger.info("👋 Goodbye!")
                    break
                if not question:
                    continue
                response = ask_groq(client, question, args.model)
                logger.info(f"\n🤖 Groq: {response}")
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

    # Ask Groq
    response = ask_groq(client, question, args.model)
    logger.info(response)


def ask_groq(client, question, model):
    """Ask Groq a question and return the response"""
    try:
        response = client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": question}], max_tokens=CONSTANT_4000, temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"


def list_models(client):
    """List available Groq models"""
    try:
        models = client.models.list()
        logger.info("📋 Available Groq Models:")
        logger.info("=" * 40)
        for model in models.data:
            logger.info(f"• {model.id}")
        logger.info("\n💡 Use with: groq -m MODEL_NAME 'your question'")
    except Exception as e:
        logger.info(f"❌ Error listing models: {e}")


if __name__ == "__main__":
    main()
