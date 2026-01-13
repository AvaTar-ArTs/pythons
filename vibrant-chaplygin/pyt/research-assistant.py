#!/usr/bin/env python3
"""
🧠 AI Research Assistant with Memory
Persistent knowledge agent that learns from conversations

Features:
- Real-time web search (Perplexity)
- Deep analysis (Claude/GPT-5)
- Persistent memory (Mem0)
- Context-aware responses
- Conversation history

Usage:
    source ~/.env.d/loader.sh
    python3 research_assistant.py "What are the latest AI breakthroughs?"
"""

import os
import sys
import json
import requests
import openai
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class ResearchAssistant:
    """AI research assistant with persistent memory"""

    def __init__(self, user_id: str = "default"):
        """__init__ function."""

        # API Keys
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.perplexity_key = os.getenv("PERPLEXITY_API_KEY")
        self.mem0_key = os.getenv("MEM0_API_KEY")

        self.user_id = user_id

        # Local storage for conversation history
        self.history_dir = Path.home() / ".ai_research"
        self.history_dir.mkdir(exist_ok=True)
        self.history_file = self.history_dir / f"{user_id}_history.json"

        # Load conversation history
        self.conversation_history = self._load_history()

        self._validate_keys()

    def _validate_keys(self):
        """Check required API keys"""
        if not self.openai_key and not self.anthropic_key:
            logger.info("❌ Need either OPENAI_API_KEY or ANTHROPIC_API_KEY")
            sys.exit(1)

        if not self.perplexity_key:
            logger.info("⚠️ PERPLEXITY_API_KEY not set (web search disabled)")

    def _load_history(self) -> List[Dict]:
        """Load conversation history from file"""
        if self.history_file.exists():
            return json.loads(self.history_file.read_text())
        return []

    def _save_history(self):
        """Save conversation history to file"""
        self.history_file.write_text(json.dumps(self.conversation_history, indent=2))

    def search_web(self, query: str) -> Dict[str, Any]:
        """
        Step 1: Real-time web search with Perplexity
        """
        if not self.perplexity_key:
            return {"content": None, "sources": []}

        logger.info("🔍 Searching web...")

        try:
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.perplexity_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "sonar-pro",
                    "messages": [{"role": "user", "content": query}],
                    "search_recency_filter": "day",
                },
                timeout=30,
            )

            if response.status_code == CONSTANT_200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                sources = result.get("citations", [])

                logger.info(f"   ✅ Found {len(sources)} sources")

                return {
                    "content": content,
                    "sources": sources,
                    "timestamp": datetime.now().isoformat(),
                }

        except Exception as e:
            logger.info(f"   ⚠️ Search error: {e}")

        return {"content": None, "sources": []}

    def retrieve_context(self, query: str) -> List[Dict]:
        """
        Step 2: Retrieve relevant memories from Mem0
        """
        if not self.mem0_key:
            logger.info("⚠️ Mem0 not configured (memory disabled)")
            return []

        logger.info("🧠 Retrieving memories...")

        try:
            response = requests.post(
                "https://api.mem0.ai/v1/memories/search",
                headers={
                    "Authorization": f"Bearer {self.mem0_key}",
                    "Content-Type": "application/json",
                },
                json={"user_id": self.user_id, "query": query, "limit": 5},
                timeout=10,
            )

            if response.status_code == CONSTANT_200:
                memories = response.json().get("results", [])
                logger.info(f"   ✅ Retrieved {len(memories)} memories")
                return memories

        except Exception as e:
            logger.info(f"   ⚠️ Memory retrieval error: {e}")

        return []

    def analyze_with_ai(
        self,
        question: str,
        web_results: Dict[str, Any],
        memories: List[Dict],
        use_claude: bool = False,
    ) -> str:
        """
        Step 3: Deep analysis with GPT-5 or Claude
        """
        logger.info(f"💭 Analyzing with {'Claude' if use_claude else 'GPT-5'}...")

        # Build context
        context_parts = []

        if web_results.get("content"):
            context_parts.append(f"**Recent Web Search:**\n{web_results['content']}")

        if memories:
            memory_text = Path("\n").join([f"- {m.get('memory', m)}" for m in memories[:3]])
            context_parts.append(f"**Past Insights:**\n{memory_text}")

        if self.conversation_history:
            recent = self.conversation_history[-3:]
            history_text = Path("\n").join(
                [f"Q: {item['question']}\nA: {item['answer'][:CONSTANT_200]}..." for item in recent]
            )
            context_parts.append(f"**Recent Conversation:**\n{history_text}")

        context = Path("\n\n").join(context_parts)

        # System prompt
        system_prompt = """You are an expert research analyst. Your role is to:
1. Synthesize information from multiple sources
2. Provide well-reasoned, evidence-based insights
3. Reference past conversations when relevant
4. Be clear about certainty levels
5. Suggest follow-up questions

Format your response clearly with sections and bullet points."""

        user_prompt = f"""Context:
{context}

Question: {question}

Provide a comprehensive, well-structured answer."""

        try:
            if use_claude and self.anthropic_key:
                # Use Claude
                from anthropic import Anthropic

                client = Anthropic(api_key=self.anthropic_key)

                message = client.messages.create(
                    model="claude-opus-4-20250514",
                    max_tokens=CONSTANT_4096,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}],
                )

                answer = message.content[0].text

            else:
                # Use GPT-5
                openai.api_key = self.openai_key

                response = openai.chat.completions.create(
                    model="gpt-5",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.7,
                    max_tokens=CONSTANT_2000,
                )

                answer = response.choices[0].message.content

            logger.info(f"   ✅ Analysis complete ({len(answer)} chars)")
            return answer

        except Exception as e:
            logger.info(f"❌ Analysis error: {e}")
            sys.exit(1)

    def store_memory(self, question: str, answer: str):
        """
        Step 4: Store insights in Mem0 for long-term memory
        """
        if not self.mem0_key:
            return

        logger.info("💾 Storing memory...")

        try:
            response = requests.post(
                "https://api.mem0.ai/v1/memories",
                headers={
                    "Authorization": f"Bearer {self.mem0_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "user_id": self.user_id,
                    "messages": [
                        {"role": "user", "content": question},
                        {"role": "assistant", "content": answer},
                    ],
                },
                timeout=10,
            )

            if response.status_code == CONSTANT_200:
                logger.info("   ✅ Memory stored")

        except Exception as e:
            logger.info(f"   ⚠️ Memory storage error: {e}")

    def research(self, question: str, use_claude: bool = False, skip_web: bool = False) -> Dict[str, Any]:
        """
        Complete research pipeline

        Args:
            question: Research question
            use_claude: Use Claude instead of GPT-5
            skip_web: Skip web search (use memory only)

        Returns:
            Dictionary with answer, sources, context
        """
        logger.info("=" * 60)
        logger.info("🧠 AI RESEARCH ASSISTANT")
        logger.info("=" * 60)
        logger.info(f"\nUser: {self.user_id}")
        logger.info(f"Question: {question}\n")

        # Step 1: Web search
        web_results = {}
        if not skip_web:
            web_results = self.search_web(question)

        # Step 2: Retrieve memories
        memories = self.retrieve_context(question)

        # Step 3: Analyze
        answer = self.analyze_with_ai(question, web_results, memories, use_claude)

        # Step 4: Store memory
        self.store_memory(question, answer)

        # Update conversation history
        self.conversation_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "question": question,
                "answer": answer,
                "sources": web_results.get("sources", []),
                "model": "claude" if use_claude else "gpt-5",
            }
        )
        self._save_history()

        # Summary
        print()
        logger.info("=" * 60)
        logger.info("✅ RESEARCH COMPLETE!")
        logger.info("=" * 60)
        logger.info(f"\n{answer}\n")

        if web_results.get("sources"):
            logger.info("\n📚 Sources:")
            for i, source in enumerate(web_results["sources"][:5], 1):
                logger.info(f"   {i}. {source}")

        logger.info(f"\n💾 Conversation saved to: {self.history_file}")
        print()

        return {
            "question": question,
            "answer": answer,
            "sources": web_results.get("sources", []),
            "memories_used": len(memories),
            "model": "claude" if use_claude else "gpt-5",
        }

    def show_history(self, limit: int = 5):
        """Show recent conversation history"""
        logger.info("=" * 60)
        logger.info(f"📜 CONVERSATION HISTORY (Last {limit})")
        logger.info("=" * 60)

        recent = self.conversation_history[-limit:]

        for i, item in enumerate(recent, 1):
            timestamp = datetime.fromisoformat(item["timestamp"]).strftime("%Y-%m-%d %H:%M")
            logger.info(f"\n[{i}] {timestamp}")
            logger.info(f"Q: {item['question']}")
            logger.info(f"A: {item['answer'][:CONSTANT_200]}...")
            print()

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        self._save_history()
        logger.info("✅ Conversation history cleared")


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        logger.info("Usage: python3 research_assistant.py <question> [--user USER_ID] [--claude] [--history]")
        logger.info("\nExamples:")
        logger.info("  python3 research_assistant.py 'What are the latest AI breakthroughs?'")
        logger.info("  python3 research_assistant.py 'Explain quantum computing' --claude")
        logger.info("  python3 research_assistant.py --history")
        sys.exit(1)

    # Parse arguments
    args = sys.argv[1:]
    user_id = "default"
    use_claude = False
    show_history = False
    question_parts = []

    i = 0
    while i < len(args):
        if args[i] == "--user" and i + 1 < len(args):
            user_id = args[i + 1]
            i += 2
        elif args[i] == "--claude":
            use_claude = True
            i += 1
        elif args[i] == "--history":
            show_history = True
            i += 1
        else:
            question_parts.append(args[i])
            i += 1

    # Initialize assistant
    assistant = ResearchAssistant(user_id=user_id)

    if show_history:
        assistant.show_history()
        return

    if not question_parts:
        logger.info("❌ No question provided")
        sys.exit(1)

    question = " ".join(question_parts)

    # Do research
    result = assistant.research(question, use_claude=use_claude)


if __name__ == "__main__":
    main()
