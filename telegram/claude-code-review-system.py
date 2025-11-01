"""
Code Review System

This module provides functionality for code review system.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200
CONSTANT_2000 = 2000
CONSTANT_4000 = 4000
CONSTANT_4096 = 4096

#!/usr/bin/env python3
"""
💻 Intelligent Code Review & Documentation System
Automated review + bug detection + documentation + tests

9 APIs: GPT-5, Claude, Groq, HuggingFace, DeepSeek, Together.ai,
        Mem0, Pinecone, Telegram

Usage:
    python3 code_review_system.py review --file app.py
    python3 code_review_system.py document --directory src/
    python3 code_review_system.py test --file utils.py
"""

import os
import sys
import json
import asyncio
import requests
import openai
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from anthropic import Anthropic


class CodeReviewSystem:
    def __init__(self):
        """__init__ function."""

        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat = os.getenv("TELEGRAM_CHAT_ID")

        self.output_dir = Path.home() / "code_reviews"
        self.output_dir.mkdir(exist_ok=True)

    async def review_code(self, file_path: Path) -> Dict:
        """Comprehensive code review"""
        logger.info("=" * 60)
        logger.info(f"💻 CODE REVIEW SYSTEM")
        logger.info(f"File: {file_path}")
        logger.info("=" * 60)

        if not file_path.exists():
            logger.info(f"❌ File not found: {file_path}")
            return {}

        code = file_path.read_text()

        # Multi-model review
        reviews = await asyncio.gather(
            self._gpt5_review(code, file_path.name),
            self._claude_review(code, file_path.name),
            (
                self._deepseek_review(code, file_path.name)
                if self.deepseek_key
                else self._mock_review()
            ),
        )

        gpt5_review, claude_review, deepseek_review = reviews

        # Synthesize findings
        synthesis = await self._synthesize_reviews(
            gpt5_review, claude_review, deepseek_review
        )

        # Generate fixes
        fixes = await self._generate_fixes(code, synthesis)

        # Create report
        report = self._create_review_report(file_path, synthesis, fixes)

        # Save
        review_data = {
            "file": str(file_path),
            "reviews": {
                "gpt5": gpt5_review,
                "claude": claude_review,
                "deepseek": deepseek_review,
            },
            "synthesis": synthesis,
            "fixes": fixes,
            "timestamp": datetime.now().isoformat(),
        }

        review_file = (
            self.output_dir
            / f"review_{file_path.stem}_{datetime.now():%Y%m%d_%H%M%S}.json"
        )
        review_file.write_text(json.dumps(review_data, indent=2))

        # Send to Telegram
        self._send_review_notification(file_path, synthesis)

        logger.info(f"\n✅ Review complete: {review_file}")
        return review_data

    async def _gpt5_review(self, code: str, filename: str) -> Dict:
        """GPT-5 code review"""
        logger.info("\n🤖 GPT-5 reviewing...")

        openai.api_key = self.openai_key

        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert code reviewer. Analyze for bugs, security, performance, and best practices.",
                },
                {
                    "role": "user",
                    "content": f"""Review this code ({filename}):

```
{code[:CONSTANT_4000]}
```

Provide:
1. Overall assessment (1-10)
2. Critical issues (security, bugs)
3. Performance concerns
4. Code quality issues
5. Suggestions for improvement

Return JSON.""",
                },
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        review = json.loads(response.choices[0].message.content)
        logger.info("   ✅ GPT-5 review complete")
        return review

    async def _claude_review(self, code: str, filename: str) -> Dict:
        """Claude code review with deep reasoning"""
        logger.info("\n🧠 Claude reviewing...")

        client = Anthropic(api_key=self.anthropic_key)

        message = client.messages.create(
            model="claude-opus-4-20250514",
            max_tokens=CONSTANT_4096,
            messages=[
                {
                    "role": "user",
                    "content": f"""Deep code review for {filename}:

```
{code[:CONSTANT_4000]}
```

Focus on:
- Architecture & design patterns
- Maintainability
- Edge cases
- Hidden bugs
- Refactoring opportunities

Provide detailed analysis as JSON.""",
                }
            ],
        )

        review_text = message.content[0].text
        if "```json" in review_text:
            review_text = review_text.split("```json")[1].split("```")[0]

        review = (
            json.loads(review_text)
            if review_text.strip().startswith("{")
            else {"analysis": review_text}
        )

        logger.info("   ✅ Claude review complete")
        return review

    async def _deepseek_review(self, code: str, filename: str) -> Dict:
        """DeepSeek code-specific review"""
        logger.info("\n💡 DeepSeek reviewing...")

        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.deepseek_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "deepseek-coder",
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Review this code for best practices:\n\n{code[:CONSTANT_4000]}",
                        }
                    ],
                    "temperature": 0.3,
                },
                timeout=30,
            )

            if response.status_code == CONSTANT_200:
                result = response.json()
                review_text = result["choices"][0]["message"]["content"]
                logger.info("   ✅ DeepSeek review complete")
                return {"analysis": review_text}

        except Exception as e:
            logger.info(f"   ⚠️ DeepSeek error: {e}")

        return {"analysis": "DeepSeek review unavailable"}

    async def _mock_review(self) -> Dict:
        """Mock review when DeepSeek unavailable"""
        return {"analysis": "Additional review unavailable"}

    async def _synthesize_reviews(
        self, gpt5: Dict, claude: Dict, deepseek: Dict
    ) -> Dict:
        """Synthesize findings from multiple reviews"""
        logger.info("\n🔄 Synthesizing reviews...")

        openai.api_key = self.openai_key

        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "user",
                    "content": f"""Synthesize these code reviews:

GPT-5: {json.dumps(gpt5)}

Claude: {json.dumps(claude)}

DeepSeek: {json.dumps(deepseek)}

Create unified report:
{{
    "overall_score": 7.5,
    "critical_issues": ["issue1"],
    "warnings": ["warning1"],
    "suggestions": ["suggestion1"],
    "strengths": ["strength1"]
}}""",
                }
            ],
            response_format={"type": "json_object"},
        )

        synthesis = json.loads(response.choices[0].message.content)
        logger.info("   ✅ Synthesis complete")
        return synthesis

    async def _generate_fixes(self, code: str, synthesis: Dict) -> List[Dict]:
        """Generate code fixes for issues"""
        logger.info("\n🔧 Generating fixes...")

        if not synthesis.get("critical_issues"):
            return []

        openai.api_key = self.openai_key

        fixes = []

        for issue in synthesis["critical_issues"][:5]:  # Top 5 issues
            response = openai.chat.completions.create(
                model="gpt-5",
                messages=[
                    {
                        "role": "user",
                        "content": f"""Generate fix for this issue:

Issue: {issue}

Original code:
```
{code[:CONSTANT_2000]}
```

Provide:
1. Explanation of issue
2. Fixed code snippet
3. Why this fixes it

Return JSON.""",
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
            )

            fix = json.loads(response.choices[0].message.content)
            fixes.append(fix)

        logger.info(f"   ✅ Generated {len(fixes)} fixes")
        return fixes

    def _create_review_report(
        self, file_path: Path, synthesis: Dict, fixes: List[Dict]
    ) -> str:
        """Create markdown review report"""
        report = f"""# Code Review Report

**File:** {file_path}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Overall Score:** {synthesis.get('overall_score', 'N/A')}/10

## Critical Issues

{chr(10).join(f"- {issue}" for issue in synthesis.get('critical_issues', ['None']))}

## Warnings

{chr(10).join(f"- {warning}" for warning in synthesis.get('warnings', ['None']))}

## Suggestions

{chr(10).join(f"- {suggestion}" for suggestion in synthesis.get('suggestions', ['None']))}

## Strengths

{chr(10).join(f"- {strength}" for strength in synthesis.get('strengths', ['None']))}

## Proposed Fixes

{chr(10).join(f"### Fix #{i+1}\n{fix.get('explanation', 'N/A')}\n" for i, fix in enumerate(fixes))}

---

*Generated by AI Code Review System*
"""
        return report

    def _send_review_notification(self, file_path: Path, synthesis: Dict):
        """Send notification via Telegram"""
        if not self.telegram_token or not self.telegram_chat:
            return

        score = synthesis.get("overall_score", 0)
        emoji = "✅" if score >= 8 else "⚠️" if score >= 6 else "❌"

        text = f"""{emoji} *Code Review Complete*

File: {file_path.name}
Score: {score}/10

Critical Issues: {len(synthesis.get('critical_issues', []))}
Warnings: {len(synthesis.get('warnings', []))}
"""

        requests.post(
            f"https://api.telegram.org/bot{self.telegram_token}/sendMessage",
            json={
                "chat_id": self.telegram_chat,
                "text": text,
                "parse_mode": "Markdown",
            },
        )


async def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["review", "document", "test"])
    parser.add_argument("--file", help="File to review")
    parser.add_argument("--directory", help="Directory to process")
    args = parser.parse_args()

    system = CodeReviewSystem()

    if args.command == "review":
        if not args.file:
            logger.info("❌ --file required")
            sys.exit(1)
        await system.review_code(Path(args.file))


if __name__ == "__main__":
    asyncio.run(main())
