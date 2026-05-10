#!/usr/bin/env python3
"""
Enhanced AI CLI Tool - Unified Interface for Multiple AI Models

This script provides a unified command-line interface for interacting with various AI models
including Claude, ChatGPT, and other LLMs. It includes improved error handling,
configuration management, and interactive features.

Features:
- Support for multiple AI providers (Anthropic, OpenAI, etc.)
- Interactive mode with conversation history
- Configuration management
- Error handling and logging
- Conversation saving/loading
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path
from typing import Optional, Dict, Any


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('ai_cli.log'),
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
        from dotenv import load_dotenv
        load_dotenv(os.path.expanduser("~/.env"))
    except ImportError:
        pass  # dotenv is optional


class AIClient:
    """Base class for AI clients."""
    
    def __init__(self, provider: str, model: str = None):
        self.provider = provider
        self.model = model or self._get_default_model()
        self.conversation_history = []
        self.logger = setup_logging()
        
    def _get_default_model(self) -> str:
        """Get default model for the provider."""
        defaults = {
            'anthropic': 'claude-3-5-sonnet-20241022',
            'openai': 'gpt-4o',
            'grok': 'grok-beta',
        }
        return defaults.get(self.provider, 'gpt-3.5-turbo')
    
    def validate_api_key(self) -> bool:
        """Validate that the required API key is available."""
        key_var = self._get_api_key_variable()
        api_key = os.getenv(key_var)
        
        if not api_key:
            self.logger.error(f"❌ {key_var} not found in environment variables")
            self.logger.info(f"💡 Add your API key to ~/.env or ~/.env.d/llm-apis.env:")
            self.logger.info(f"   {key_var}=your_key_here")
            return False
        return True
    
    def _get_api_key_variable(self) -> str:
        """Get the environment variable name for the API key."""
        key_vars = {
            'anthropic': 'ANTHROPIC_API_KEY',
            'openai': 'OPENAI_API_KEY',
            'grok': 'XAI_API_KEY',
        }
        return key_vars.get(self.provider, 'OPENAI_API_KEY')
    
    def chat(self, message: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Send a message and get a response. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement the chat method")
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []
    
    def save_conversation(self, filename: str):
        """Save conversation history to a JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, indent=2)
        self.logger.info(f"💾 Conversation saved to {filename}")
    
    def load_conversation(self, filename: str):
        """Load conversation history from a JSON file."""
        with open(filename, 'r', encoding='utf-8') as f:
            self.conversation_history = json.load(f)
        self.logger.info(f"📂 Conversation loaded from {filename}")


class AnthropicClient(AIClient):
    """Anthropic Claude client implementation."""
    
    def __init__(self, model: str = None):
        super().__init__('anthropic', model)
        
        # Import here to avoid dependency issues if not needed
        try:
            from anthropic import Anthropic
            self.Anthropic = Anthropic
        except ImportError:
            self.logger.error("❌ anthropic package not installed. Install with: pip install anthropic")
            raise
    
    def validate_api_key(self) -> bool:
        """Validate Anthropic API key."""
        if not super().validate_api_key():
            return False
        
        try:
            api_key = os.getenv('ANTHROPIC_API_KEY')
            self.client = self.Anthropic(api_key=api_key)
            return True
        except Exception as e:
            self.logger.error(f"❌ Error initializing Anthropic client: {e}")
            return False
    
    def chat(self, message: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Send a message to Claude and get a response."""
        try:
            # Add user message to conversation history
            self.conversation_history.append({"role": "user", "content": message})
            
            # Create the message
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=self.conversation_history[-10:]  # Use last 10 messages to avoid context limits
            )
            
            # Extract assistant's response
            assistant_message = response.content[0].text
            
            # Add assistant's response to conversation history
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
            
        except Exception as e:
            error_msg = f"❌ Error communicating with Claude: {str(e)}"
            self.logger.error(error_msg)
            return error_msg


class OpenAIClient(AIClient):
    """OpenAI ChatGPT client implementation."""
    
    def __init__(self, model: str = None):
        super().__init__('openai', model)
        
        # Import here to avoid dependency issues if not needed
        try:
            from openai import OpenAI
            self.OpenAI = OpenAI
        except ImportError:
            self.logger.error("❌ openai package not installed. Install with: pip install openai")
            raise
    
    def validate_api_key(self) -> bool:
        """Validate OpenAI API key."""
        if not super().validate_api_key():
            return False
        
        try:
            api_key = os.getenv('OPENAI_API_KEY')
            self.client = self.OpenAI(api_key=api_key)
            return True
        except Exception as e:
            self.logger.error(f"❌ Error initializing OpenAI client: {e}")
            return False
    
    def chat(self, message: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Send a message to ChatGPT and get a response."""
        try:
            # Add user message to conversation history
            self.conversation_history.append({"role": "user", "content": message})
            
            # Use max_completion_tokens for newer models
            if "gpt-4" in self.model or "gpt-5" in self.model:
                # GPT-4 and newer models may have different requirements
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_history,
                    temperature=min(temperature, 1.0),  # Temperature must be ≤ 2.0 for OpenAI
                    max_completion_tokens=max_tokens,
                )
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_history,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            
            # Extract assistant's response
            assistant_message = response.choices[0].message.content
            
            # Add assistant's response to conversation history
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
            
        except Exception as e:
            error_msg = f"❌ Error communicating with ChatGPT: {str(e)}"
            self.logger.error(error_msg)
            return error_msg


def create_client(provider: str, model: str = None) -> AIClient:
    """Factory function to create the appropriate AI client."""
    clients = {
        'anthropic': AnthropicClient,
        'openai': OpenAIClient,
    }
    
    if provider not in clients:
        raise ValueError(f"Unsupported provider: {provider}. Supported: {list(clients.keys())}")
    
    return clients[provider](model)


def interactive_mode(client: AIClient):
    """Run the interactive CLI mode."""
    logger = setup_logging()
    logger.info("🤖 AI Agent - Interactive Mode")
    logger.info("=" * 50)
    
    # Set a helpful system message
    system_message = "You are a helpful AI assistant. Be concise, accurate, and friendly in your responses."
    client.conversation_history.append({"role": "system", "content": system_message})
    
    logger.info("✅ Agent initialized successfully!")
    logger.info("Commands:")
    logger.info("  • Type 'quit', 'exit', or 'bye' to end")
    logger.info("  • Type 'reset' to clear conversation history")
    logger.info("  • Type 'save <filename>' to save conversation")
    logger.info("  • Type 'load <filename>' to load conversation")
    logger.info("  • Type 'models' to see available models")
    logger.info("-" * 50)
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ["quit", "exit", "bye", "q"]:
                logger.info("👋 Goodbye!")
                break
            elif user_input.lower() == "reset":
                client.reset_conversation()
                client.conversation_history.append({"role": "system", "content": system_message})
                logger.info("🔄 Conversation history cleared!")
                continue
            elif user_input.lower().startswith("save "):
                filename = user_input[5:].strip()
                if filename:
                    client.save_conversation(filename)
                else:
                    logger.info("❌ Please provide a filename: save <filename>")
                continue
            elif user_input.lower().startswith("load "):
                filename = user_input[5:].strip()
                if filename:
                    client.load_conversation(filename)
                else:
                    logger.info("❌ Please provide a filename: load <filename>")
                continue
            elif user_input.lower() == "models":
                logger.info(f"📋 Current model: {client.model}")
                logger.info(f"   Provider: {client.provider}")
                continue
            elif not user_input:
                continue
            
            # Get response from agent
            response = client.chat(user_input)
            logger.info(f"🤖 {client.provider.title()}: {response}")
            
        except KeyboardInterrupt:
            logger.info("\n👋 Goodbye!")
            break
        except Exception as e:
            logger.error(f"❌ Error: {str(e)}")


def main():
    """Main entry point with command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Enhanced AI CLI Tool - Unified Interface for Multiple AI Models',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python enhanced_ai_cli.py --provider anthropic "Hello Claude!"     # Use Claude
  python enhanced_ai_cli.py --provider openai "Hello ChatGPT!"      # Use ChatGPT
  python enhanced_ai_cli.py --interactive --provider openai         # Interactive mode
  python enhanced_ai_cli.py --model gpt-4o "Analyze this code..."  # Specific model
        """
    )
    
    parser.add_argument(
        'question',
        nargs='?',
        help='Your question for the AI'
    )
    
    parser.add_argument(
        '--provider',
        choices=['anthropic', 'openai'],
        default='openai',
        help='AI provider to use (default: openai)'
    )
    
    parser.add_argument(
        '--model',
        help='Specific model to use (default varies by provider)'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Start interactive mode'
    )
    
    parser.add_argument(
        '-t', '--temperature',
        type=float,
        default=0.7,
        help='Response creativity (0.0 to 1.0, default: 0.7)'
    )
    
    parser.add_argument(
        '--max-tokens',
        type=int,
        default=1000,
        help='Maximum tokens in response (default: 1000)'
    )
    
    parser.add_argument(
        '-f', '--file',
        help='Read question from file'
    )
    
    args = parser.parse_args()
    
    # Load environment variables
    load_env_d()
    load_dotenv_fallback()
    
    # Create client
    try:
        client = create_client(args.provider, args.model)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    # Validate API key
    if not client.validate_api_key():
        sys.exit(1)
    
    # Get question
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                question = f.read().strip()
        except FileNotFoundError:
            client.logger.error(f"❌ Error: File '{args.file}' not found")
            sys.exit(1)
    elif args.interactive:
        interactive_mode(client)
        return
    elif args.question:
        question = args.question
    else:
        # Read from stdin
        question = sys.stdin.read().strip()
        if not question:
            client.logger.error("❌ No question provided")
            parser.print_help()
            sys.exit(1)
    
    # Get response
    response = client.chat(question, args.temperature, args.max_tokens)
    print(response)


if __name__ == "__main__":
    main()