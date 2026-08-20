#!/usr/bin/env python3
"""
AI Router - Intelligent Request Routing System

This script implements a basic router that determines which AI in the ecosystem
is most appropriate for a given task based on simple heuristics.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional


class AIRouter:
    """
    A basic AI router that selects the most appropriate AI platform for a given task.
    """
    
    def __init__(self):
        self.platform_weights = {
            "Claude": {
                "coding": 9,
                "analysis": 10,
                "creative_writing": 8,
                "research": 9,
                "documentation": 8
            },
            "Cursor": {
                "coding": 10,
                "debugging": 10,
                "code_refactoring": 9,
                "code_review": 9,
                "technical_documentation": 7
            },
            "Gemini": {
                "general_questions": 8,
                "research": 8,
                "creative_writing": 7,
                "multimodal_tasks": 9,
                "web_search_integration": 9
            },
            "Qwen": {
                "coding": 8,
                "analysis": 7,
                "multilingual": 9,
                "technical_tasks": 8,
                "open_source_knowledge": 8
            },
            "Grok": {
                "coding": 7,
                "analysis": 8,
                "humor": 8,
                "real_world_reasoning": 8,
                "long_context": 7
            }
        }
        
        # Keywords that help identify task types
        self.task_identifiers = {
            "coding": [
                r"\b(code|program|function|method|class|variable|algorithm|debug|fix\b)",
                r"\b(python|javascript|java|c\+\+|ruby|go|rust|php|sql|html|css)\b",
                r"\b(library|framework|api|sdk|dependency|package)\b"
            ],
            "analysis": [
                r"\b(analyze|analyze|evaluate|assess|review|compare|contrast)\b",
                r"\b(data|information|results|metrics|performance|statistics)\b",
                r"\b(pattern|trend|correlation|relationship)\b"
            ],
            "creative_writing": [
                r"\b(write|create|draft|compose|story|narrative|poem|script)\b",
                r"\b(creative|fiction|character|plot|scene|dialogue)\b"
            ],
            "research": [
                r"\b(research|investigate|study|explore|find|discover)\b",
                r"\b(academic|scholarly|scientific|journal|paper|citation)\b"
            ],
            "documentation": [
                r"\b(document|explain|describe|tutorial|guide|manual|instructions?)\b",
                r"\b(how.*to|steps|process|procedure)\b"
            ],
            "debugging": [
                r"\b(debug|fix|troubleshoot|error|bug|exception|traceback)\b",
                r"\b(not.*working|fails|broken|issue|problem)\b"
            ]
        }
    
    def identify_task_type(self, query: str) -> str:
        """
        Identify the primary task type based on the query.
        """
        query_lower = query.lower()
        scores = {}
        
        for task_type, patterns in self.task_identifiers.items():
            score = 0
            for pattern in patterns:
                matches = re.findall(pattern, query_lower)
                score += len(matches)
            scores[task_type] = score
        
        # Return the task type with the highest score
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        else:
            # Default to analysis if no clear match
            return "analysis"
    
    def route_request(self, query: str) -> str:
        """
        Determine the most appropriate AI platform for the given query.
        """
        task_type = self.identify_task_type(query)
        
        # Calculate scores for each platform based on the task type
        platform_scores = {}
        for platform, weights in self.platform_weights.items():
            if task_type in weights:
                platform_scores[platform] = weights[task_type]
            else:
                # Default score if task type isn't specifically weighted
                platform_scores[platform] = 5
        
        # Return the platform with the highest score
        best_platform = max(platform_scores, key=platform_scores.get)
        
        return {
            "recommended_platform": best_platform,
            "task_type": task_type,
            "confidence": platform_scores[best_platform],
            "all_scores": platform_scores
        }


def main():
    """
    Main function to demonstrate the AI router.
    """
    router = AIRouter()
    
    print("AI Router - Intelligent Request Routing System")
    print("=" * 50)
    
    # Example queries to demonstrate routing
    example_queries = [
        "Write a Python function to sort an array using quicksort algorithm",
        "Analyze the performance metrics of our latest deployment",
        "Create a creative story about a robot learning to paint",
        "Research the latest developments in quantum computing",
        "Explain how to set up a React development environment",
        "Debug this JavaScript code that's causing a null pointer exception",
        "Compare the pros and cons of different database systems"
    ]
    
    for query in example_queries:
        result = router.route_request(query)
        print(f"\nQuery: {query}")
        print(f"Recommended Platform: {result['recommended_platform']}")
        print(f"Task Type: {result['task_type']}")
        print(f"Confidence Score: {result['confidence']}")
        print("All Scores:", result['all_scores'])


if __name__ == "__main__":
    main()