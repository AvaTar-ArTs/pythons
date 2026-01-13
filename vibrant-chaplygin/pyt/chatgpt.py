#!/usr/bin/env python3
"""
ChatGPT Agent - A simple conversational AI agent using OpenAI's API
"""

import os
import sys
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
import json


class ChatGPTAgent:
    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize the ChatGPT Agent

        Args:
            api_key: OpenAI API key (if None, will try to load from environment)
            model: OpenAI model to use (if None, will try to load from environment or default to gpt-3.5-turbo)
        """
        # Load environment variables from multiple sources
        load_dotenv()

        # Try to load from your .env.d directory
        env_d_path = os.path.expanduser("~/.env.d/llm-apis.env")
        if os.path.exists(env_d_path):
            load_dotenv(env_d_path)

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY environment variable or pass api_key parameter."
            )

        self.client = OpenAI(api_key=self.api_key)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.conversation_history = []

    def add_system_message(self, message: str):
        """Add a system message to set the agent's behavior"""
        self.conversation_history.append({"role": "system", "content": message})

    def chat(
        self, message: str, temperature: float = 0.7, max_tokens: int = CONSTANT_1000
    ) -> str:
        """
        Send a message to the ChatGPT agent and get a response

        Args:
            message: User message
            temperature: Response creativity (0.0 to 1.0)
            max_tokens: Maximum tokens in response

        Returns:
            Agent's response
        """
        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "content": message})

        try:
            # Use max_completion_tokens for newer models like GPT-5
            if "gpt-4" in self.model or "gpt-5" in self.model:
                # GPT-5 only supports temperature=1
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_history,
                    temperature=1.0,
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
            self.conversation_history.append(
                {"role": "assistant", "content": assistant_message}
            )

            return assistant_message

        except Exception as e:
            return f"Error: {str(e)}"

    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = []

    def save_conversation(self, filename: str):
        """Save conversation history to a JSON file"""
        with open(filename, "w") as f:
            json.dump(self.conversation_history, f, indent=2)

    def load_conversation(self, filename: str):
        """Load conversation history from a JSON file"""
        with open(filename, "r") as f:
            self.conversation_history = json.load(f)


def main():
    """Interactive CLI for the ChatGPT Agent"""
    logger.info("🤖 ChatGPT Agent - Interactive Mode")
    logger.info("=" * 40)

    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.info("⚠️  OpenAI API key not found!")
        logger.info("Please set your API key in one of these ways:")
        logger.info(
            "1. Set environment variable: export OPENAI_API_KEY='your-key-here'"
        )
        logger.info("2. Create a .env file with: OPENAI_API_KEY=your-key-here")
        logger.info("3. Pass it as a parameter when creating the agent")
        return

    try:
        # Initialize agent
        agent = ChatGPTAgent(api_key=api_key)

        # Set a helpful system message
        agent.add_system_message(
            "You are a helpful AI assistant. Be concise, accurate, and friendly in your responses."
        )

        logger.info("✅ Agent initialized successfully!")
        logger.info("Type 'quit', 'exit', or 'bye' to end the conversation")
        logger.info("Type 'reset' to clear conversation history")
        logger.info("Type 'save <filename>' to save conversation")
        logger.info("Type 'load <filename>' to load conversation")
        logger.info("-" * 40)

        while True:
            try:
                user_input = input("\n👤 You: ").strip()

                if user_input.lower() in ["quit", "exit", "bye"]:
                    logger.info("👋 Goodbye!")
                    break
                elif user_input.lower() == "reset":
                    agent.reset_conversation()
                    agent.add_system_message(
                        "You are a helpful AI assistant. Be concise, accurate, and friendly in your responses."
                    )
                    logger.info("🔄 Conversation history cleared!")
                    continue
                elif user_input.lower().startswith("save "):
                    filename = user_input[5:].strip()
                    if filename:
                        agent.save_conversation(filename)
                        logger.info(f"💾 Conversation saved to {filename}")
                    else:
                        logger.info("❌ Please provide a filename")
                    continue
                elif user_input.lower().startswith("load "):
                    filename = user_input[5:].strip()
                    if filename:
                        agent.load_conversation(filename)
                        logger.info(f"📂 Conversation loaded from {filename}")
                    else:
                        logger.info("❌ Please provide a filename")
                    continue
                elif not user_input:
                    continue

                # Get response from agent
                response = agent.chat(user_input)
                logger.info(f"🤖 Agent: {response}")

            except KeyboardInterrupt:
                logger.info("\n👋 Goodbye!")
                break
            except Exception as e:
                logger.info(f"❌ Error: {str(e)}")

    except Exception as e:
        logger.info(f"❌ Failed to initialize agent: {str(e)}")


if __name__ == "__main__":
    main()
