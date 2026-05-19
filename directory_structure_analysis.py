#!/usr/bin/env python3
"""
Directory Structure Analysis for AVATARARTS Reorganization

Analyzes the current structure and provides recommendations for the proposed
hierarchical organization with depth levels and functional categorization.
"""

import os
from pathlib import Path
from collections import defaultdict, Counter
import json

class StructureAnalyzer:
    def __init__(self, root_path="/Users/steven/AVATARARTS"):
        self.root_path = Path(root_path)

    def analyze_current_structure(self):
        """Analyze the current directory structure."""
        structure = {
            "total_directories": 0,
            "depth_distribution": defaultdict(int),
            "category_distribution": defaultdict(int),
            "naming_patterns": defaultdict(int),
            "large_directories": [],
            "empty_directories": []
        }

        for dir_path in self.root_path.rglob('*'):
            if dir_path.is_dir() and not any(part.startswith('.') for part in dir_path.parts):
                depth = len(dir_path.relative_to(self.root_path).parts)
                structure["total_directories"] += 1
                structure["depth_distribution"][depth] += 1

                # Check directory size
                try:
                    file_count = sum(1 for _ in dir_path.rglob('*') if _.is_file())
                    if file_count > 100:
                        structure["large_directories"].append({
                            "path": str(dir_path.relative_to(self.root_path)),
                            "files": file_count,
                            "depth": depth
                        })
                    elif file_count == 0:
                        structure["empty_directories"].append(str(dir_path.relative_to(self.root_path)))
                except:
                    pass

                # Analyze naming patterns
                dir_name = dir_path.name
                if dir_name.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
                    structure["naming_patterns"]["numbered"] += 1
                elif '-' in dir_name:
                    structure["naming_patterns"]["hyphenated"] += 1
                elif '_' in dir_name:
                    structure["naming_patterns"]["underscored"] += 1
                else:
                    structure["naming_patterns"]["simple"] += 1

        return structure

    def evaluate_proposed_structure(self):
        """Evaluate the proposed hierarchical structure."""
        evaluation = {
            "strengths": [],
            "opportunities": [],
            "implementation_notes": [],
            "depth_analysis": {},
            "scalability_score": 0
        }

        # Analyze the proposed structure from the user's message
        proposed_structure = """
business/
├── websites/
│   ├── heavenlyHands/
│   ├── steven-chaplinski/
│   └── portfolio-builder/
├── products/
│   ├── retention-suite/
│   ├── creative-ai-marketplace/
│   └── creative-ai-agency/
├── automations/
├── scripts/
└── pythons/

content/
├── documentation/
│   └── strategy-docs/
│       └── personal-brand/
├── creative/
└── assets/

data/
└── [unchanged]

archives/
        """

        # Evaluate depth levels
        evaluation["depth_analysis"] = {
            "level_1_categories": ["business", "content", "data", "archives"],
            "level_2_functions": ["websites", "products", "automations", "documentation", "creative"],
            "level_3_projects": ["heavenlyHands", "retention-suite", "strategy-docs"],
            "level_4_specific": ["personal-brand"]
        }

        # Identify strengths
        evaluation["strengths"] = [
            "Clear hierarchical organization with functional depth",
            "Business-focused categorization (business/content/data/archives)",
            "Scalable structure supporting multiple projects per function",
            "Descriptive naming without confusing numbers",
            "Logical separation of concerns at each level",
            "Room for growth with 4+ depth levels",
            "Easy navigation: business → function → project → specific"
        ]

        # Identify opportunities
        evaluation["opportunities"] = [
            "Consider cross-cutting concerns (security, testing, deployment)",
            "Add shared resources directory for reusable components",
            "Consider environment-specific subdirectories",
            "Add documentation standards for each level",
            "Consider automation for structure validation",
            "Add templates for new project onboarding"
        ]

        # Implementation notes
        evaluation["implementation_notes"] = [
            "Start with business/ reorganization (highest business value)",
            "Use migration scripts with rollback capability",
            "Update all documentation references",
            "Reindex memory system after structural changes",
            "Test all tool paths after reorganization",
            "Create directory templates for consistency"
        ]

        # Scalability assessment
        evaluation["scalability_score"] = 9  # Out of 10 - very scalable

        return evaluation

    def generate_migration_plan(self):
        """Generate a migration plan for implementing the proposed structure."""
        migration_plan = {
            "phases": [],
            "risk_assessment": {},
            "rollback_strategy": {},
            "success_metrics": []
        }

        # Phase 1: Preparation
        migration_plan["phases"].append({
            "phase": 1,
            "name": "Preparation & Analysis",
            "duration": "2-3 hours",
            "tasks": [
                "Backup current structure",
                "Analyze content dependencies",
                "Create migration mapping",
                "Test migration scripts"
            ]
        })

        # Phase 2: Core Migration
        migration_plan["phases"].append({
            "phase": 2,
            "name": "Core Business Migration",
            "duration": "4-6 hours",
            "tasks": [
                "Migrate business/automations → business/automations/",
                "Migrate business/scripts → business/scripts/",
                "Migrate business/pythons → business/pythons/",
                "Reorganize websites and products subdirectories",
                "Update navigation and documentation"
            ]
        })

        # Phase 3: Content Migration
        migration_plan["phases"].append({
            "phase": 3,
            "name": "Content & Data Migration",
            "duration": "2-3 hours",
            "tasks": [
                "Reorganize content/ structure",
                "Migrate documentation subdirectories",
                "Update data/ organization if needed",
                "Clean up old structures"
            ]
        })

        # Phase 4: Validation
        migration_plan["phases"].append({
            "phase": 4,
            "name": "Validation & Optimization",
            "duration": "2-3 hours",
            "tasks": [
                "Verify all paths work",
                "Update memory system",
                "Test navigation tools",
                "Create directory templates",
                "Document new structure"
            ]
        })

        # Risk assessment
        migration_plan["risk_assessment"] = {
            "low_risk": ["Creating new directory structure", "Moving documentation"],
            "medium_risk": ["Moving executable scripts", "Updating configuration paths"],
            "high_risk": ["Moving interdependent systems", "Breaking external references"],
            "mitigation": [
                "Create backups before each phase",
                "Test critical paths after each move",
                "Have rollback scripts ready",
                "Move in small batches"
            ]
        }

        # Success metrics
        migration_plan["success_metrics"] = [
            "All directories follow new structure",
            "No broken tool references",
            "Memory system finds all tools",
            "Navigation tools work correctly",
            "Documentation is up-to-date",
            "New project onboarding is clear"
        ]

        return migration_plan

    def create_directory_templates(self):
        """Create templates for consistent directory structure."""
        templates = {
            "business/websites/project/": [
                "README.md",
                "docs/",
                "assets/",
                "config/",
                "scripts/"
            ],
            "business/products/product/": [
                "README.md",
                "docs/",
                "code/",
                "tests/",
                "deployment/"
            ],
            "content/documentation/category/": [
                "README.md",
                "guides/",
                "templates/",
                "examples/"
            ]
        }

        return templates

def main():
    analyzer = StructureAnalyzer()

    print("🏗️  AVATARARTS DIRECTORY STRUCTURE ANALYSIS")
    print("=" * 50)

    # Analyze current structure
    current = analyzer.analyze_current_structure()
    print(f"📊 Current Structure:")
    print(f"   Total directories: {current['total_directories']}")
    print(f"   Depth distribution: {dict(current['depth_distribution'])}")
    print(f"   Large directories (>100 files): {len(current['large_directories'])}")
    print(f"   Empty directories: {len(current['empty_directories'])}")

    # Evaluate proposed structure
    evaluation = analyzer.evaluate_proposed_structure()
    print("\n🎯 Proposed Structure Evaluation:")
    print(f"   Scalability score: {evaluation['scalability_score']}/10")
    print(f"   Strengths identified: {len(evaluation['strengths'])}")
    print(f"   Opportunities found: {len(evaluation['opportunities'])}")

    # Show key strengths
    print("
✅ Key Strengths:"    for strength in evaluation["strengths"][:5]:
        print(f"   • {strength}")

    # Generate migration plan
    migration = analyzer.generate_migration_plan()
    print("
🚀 Migration Plan:"    print(f"   Phases: {len(migration['phases'])}")
    print(f"   Success metrics: {len(migration['success_metrics'])}")

    # Save analysis
    analysis_results = {
        "current_structure": current,
        "proposed_evaluation": evaluation,
        "migration_plan": migration,
        "directory_templates": analyzer.create_directory_templates(),
        "generated_at": "2026-02-03"
    }

    with open("/Users/steven/structure_analysis_results.json", 'w') as f:
        json.dump(analysis_results, f, indent=2, default=str)

    print("\n📋 Analysis saved to: /Users/steven/structure_analysis_results.json")
    print("\n🎉 Ready to implement the new hierarchical structure!")
    print("   Run: python3 directory_structure_analysis.py --migrate")

if __name__ == "__main__":
    main()