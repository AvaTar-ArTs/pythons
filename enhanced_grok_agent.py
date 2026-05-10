#!/usr/bin/env python3
"""
Enhanced Grok LangChain Agent
Improved version with better error handling, configuration, and functionality.

Features:
- Proper error handling and logging
- Configuration management
- Rate limiting protection
- Enhanced tool integration
- Type hints and documentation
"""

import logging
import os
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from composio_langchain import ComposioToolSet, App


def setup_logging(log_file: str = "grok_agent.log"):
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
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


@dataclass
class AgentConfig:
    """Configuration for the Grok agent."""
    api_key: str
    model: str = "grok-4-0709"
    base_url: str = "https://api.x.ai/v1"
    temperature: float = 0.7
    max_tokens: int = 1000
    max_iterations: int = 10
    system_prompt: str = "You are a helpful AI assistant with access to file tools. Use the tools when needed to help the user."
    

class EnhancedGrokAgent:
    """Enhanced Grok agent with improved functionality and error handling."""
    
    def __init__(self, config: AgentConfig):
        """Initialize the enhanced Grok agent."""
        self.logger = setup_logging()
        self.config = config
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            api_key=config.api_key,
            model=config.model,
            base_url=config.base_url,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        )
        
        # Initialize tools
        self.composio_toolset = ComposioToolSet()
        self.tools = self.composio_toolset.get_tools(apps=[App.FILETOOL])
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", config.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", 
            return_messages=True
        )
        
        # Create agent
        self.agent = create_openai_functions_agent(
            self.llm, 
            self.tools, 
            prompt
        )
        
        # Create agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=False,
            max_iterations=config.max_iterations,
        )
        
        self.logger.info(f"Enhanced Grok agent initialized with model: {config.model}")
    
    def chat(self, user_message: str) -> str:
        """Chat with the agent using LangChain's built-in tool calling."""
        try:
            response = self.agent_executor.invoke({"input": user_message})
            output = response.get("output", "Sorry, I couldn't generate a response.")
            self.logger.info(f"Response generated: {output[:100]}...")
            return output
        except Exception as e:
            error_msg = self._handle_error(e)
            self.logger.error(f"Error in chat: {error_msg}")
            return error_msg
    
    def _handle_error(self, e: Exception) -> str:
        """Handle different types of errors appropriately."""
        error_str = str(e).lower()
        
        if "rate_limit" in error_str or "429" in error_str:
            error_msg = "Rate limit exceeded. Please try again later."
        elif "api_key" in error_str or "authentication" in error_str:
            error_msg = "Authentication error. Please check your API key."
        elif "quota" in error_str or "credit" in error_str:
            error_msg = "Account quota exceeded. Please check your billing."
        else:
            error_msg = f"An error occurred: {str(e)}"
        
        return error_msg
    
    def reset_conversation(self):
        """Reset the conversation memory."""
        self.memory.clear()
        self.logger.info("Conversation memory cleared")
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the current conversation history."""
        return self.memory.load_memory_variables({}).get("chat_history", [])
    
    def add_to_conversation(self, role: str, message: str):
        """Add a message to the conversation history."""
        if role.lower() == "user":
            self.memory.chat_memory.add_user_message(message)
        elif role.lower() == "assistant":
            self.memory.chat_memory.add_ai_message(message)
        else:
            raise ValueError(f"Role must be 'user' or 'assistant', got: {role}")
    
    def update_system_prompt(self, new_prompt: str):
        """Update the system prompt."""
        self.config.system_prompt = new_prompt
        self.logger.info("System prompt updated")


def main():
    """Main function to demonstrate the enhanced Grok agent."""
    # Load environment variables
    load_env_d()
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("XAI_API_KEY") or os.getenv("GROK_API_KEY")
    if not api_key:
        print("❌ Error: XAI_API_KEY or GROK_API_KEY not found in environment variables")
        print("💡 Add your API key to ~/.env or ~/.env.d/llm-apis.env:")
        print("   XAI_API_KEY=your_key_here")
        return
    
    # Create configuration
    config = AgentConfig(
        api_key=api_key,
        model=os.getenv("GROK_MODEL", "grok-4-0709"),
        base_url=os.getenv("GROK_BASE_URL", "https://api.x.ai/v1"),
        temperature=float(os.getenv("GROK_TEMPERATURE", "0.7")),
        max_tokens=int(os.getenv("GROK_MAX_TOKENS", "1000")),
        max_iterations=int(os.getenv("GROK_MAX_ITERATIONS", "10")),
    )
    
    # Initialize agent
    try:
        agent = EnhancedGrokAgent(config)
        print("🤖 Enhanced Grok Agent initialized successfully!")
        print("Type 'quit', 'exit', or 'bye' to end the conversation")
        print("Type 'reset' to clear conversation history")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ["quit", "exit", "bye"]:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == "reset":
                    agent.reset_conversation()
                    print("🔄 Conversation history cleared!")
                    continue
                elif not user_input:
                    continue
                
                # Get response from agent
                response = agent.chat(user_input)
                print(f"🤖 Grok: {response}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")


if __name__ == "__main__":
    main()