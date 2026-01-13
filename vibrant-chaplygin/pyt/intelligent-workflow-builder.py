#!/usr/bin/env python3
"""
🔮 INTELLIGENT WORKFLOW BUILDER
===============================

Analyzes your 748+ Python scripts and creates optimized AI-powered workflows

Features:
- 📊 Deep analysis of existing scripts
- 🔗 Intelligent dependency mapping  
- 🤖 AI-powered workflow generation
- ⚡ Parallel execution optimization
- 📈 ROI and time-saving calculations
- 🎯 Custom workflow templates

Based on analysis of:
- 748 Python scripts
- 199,212 lines of code
- Categories: Instagram (79), Leonardo (27), Image (19), Suno (17), OpenAI (16)
"""

import os
import ast
import json
import csv
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
from pathlib import Path
import anthropic
from openai import OpenAI


@dataclass
class Script:
    """Represents a Python script"""
    filename: str
    path: str
    category: str
    purpose: str
    services: List[str]
    operations: List[str]
    classes: List[str]
    functions: int
    size_kb: float
    lines: int
    dependencies: Set[str] = field(default_factory=set)
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)


@dataclass
class Workflow:
    """Represents an automated workflow"""
    name: str
    description: str
    scripts: List[Script]
    estimated_time_manual: int  # minutes
    estimated_time_auto: int  # minutes
    roi_score: float
    steps: List[Dict]
    ai_enhancements: List[str] = field(default_factory=list)


class IntelligentWorkflowBuilder:
    """
    Analyzes existing scripts and builds intelligent workflows
    """
    
    def __init__(self, pythons_dir: str = "/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)
        self.scripts: Dict[str, Script] = {}
        self.workflows: List[Workflow] = []
        self.categories = defaultdict(list)
        
        # AI clients
        self.claude = None
        self.openai_client = None
        
        if os.getenv('ANTHROPIC_API_KEY'):
            self.claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        if os.getenv('OPENAI_API_KEY'):
            self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def analyze_codebase(self):
        """Deep analysis of the codebase"""
        print("🔍 Analyzing codebase...")
        
        analysis_file = self.pythons_dir / "_analysis/current/DEEP_CONTENT_ANALYSIS.csv"
        
        if analysis_file.exists():
            print(f"   📄 Reading analysis from: {analysis_file}")
            self._load_from_csv(analysis_file)
        else:
            print("   🔄 Performing fresh analysis...")
            self._scan_directory()
        
        print(f"   ✅ Analyzed {len(self.scripts)} scripts")
        print(f"   📊 Found {len(self.categories)} categories")
        
        return self.scripts
    
    def _load_from_csv(self, csv_path: Path):
        """Load script analysis from existing CSV"""
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                services = [s.strip() for s in row.get('services', '').split(',') if s.strip()]
                operations = [o.strip() for o in row.get('operations', '').split(',') if o.strip()]
                classes = [c.strip() for c in row.get('classes', '').split(',') if c.strip()]
                
                script = Script(
                    filename=row['filename'],
                    path=str(self.pythons_dir / row['filename']),
                    category=row.get('category', 'Unknown'),
                    purpose=row.get('purpose', 'No description'),
                    services=services,
                    operations=operations,
                    classes=classes,
                    functions=int(row.get('function_count', 0)),
                    size_kb=float(row.get('size_kb', 0)),
                    lines=int(row.get('lines', 0))
                )
                
                self.scripts[script.filename] = script
                self.categories[script.category].append(script)
    
    def _scan_directory(self):
        """Scan directory for Python files"""
        for py_file in self.pythons_dir.glob("*.py"):
            if py_file.name.startswith('_'):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    tree = ast.parse(content)
                    
                script = Script(
                    filename=py_file.name,
                    path=str(py_file),
                    category=self._infer_category(py_file.name),
                    purpose=self._extract_purpose(content),
                    services=self._extract_services(content),
                    operations=self._extract_operations(content),
                    classes=[node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)],
                    functions=sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)),
                    size_kb=py_file.stat().st_size / 1024,
                    lines=len(content.splitlines())
                )
                
                self.scripts[script.filename] = script
                self.categories[script.category].append(script)
                
            except Exception as e:
                print(f"   ⚠️  Error analyzing {py_file.name}: {e}")
    
    def _infer_category(self, filename: str) -> str:
        """Infer category from filename"""
        if 'instagram' in filename:
            return 'Instagram Automation'
        elif 'leonardo' in filename:
            return 'Leonardo AI'
        elif 'image' in filename:
            return 'Image Processing'
        elif 'suno' in filename:
            return 'Suno Music'
        elif 'openai' in filename or 'claude' in filename:
            return 'AI Content Generation'
        elif 'youtube' in filename:
            return 'YouTube Automation'
        elif 'gallery' in filename:
            return 'Gallery Generation'
        elif 'transcribe' in filename or 'whisper' in filename:
            return 'Audio Transcription'
        else:
            return 'General Utility'
    
    def _extract_purpose(self, content: str) -> str:
        """Extract purpose from docstring"""
        lines = content.split('\n')
        for line in lines[:20]:
            if line.strip().startswith('"""') or line.strip().startswith("'''"):
                return line.strip(' "\\'')
        return "No description"
    
    def _extract_services(self, content: str) -> List[str]:
        """Extract API services used"""
        services = []
        service_keywords = {
            'OpenAI': ['openai', 'gpt', 'dall-e'],
            'Anthropic': ['anthropic', 'claude'],
            'Instagram': ['instabot', 'instagram'],
            'Leonardo': ['leonardo'],
            'Whisper': ['whisper'],
            'ElevenLabs': ['elevenlabs'],
            'Suno': ['suno'],
            'YouTube': ['youtube'],
        }
        
        content_lower = content.lower()
        for service, keywords in service_keywords.items():
            if any(kw in content_lower for kw in keywords):
                services.append(service)
        
        return services
    
    def _extract_operations(self, content: str) -> List[str]:
        """Extract operations performed"""
        operations = []
        op_keywords = {
            'upload': ['upload', 'post', 'publish'],
            'download': ['download', 'fetch', 'retrieve'],
            'generate': ['generate', 'create', 'produce'],
            'analyze': ['analyze', 'process', 'examine'],
            'transcribe': ['transcribe', 'speech_to_text'],
        }
        
        content_lower = content.lower()
        for op, keywords in op_keywords.items():
            if any(kw in content_lower for kw in keywords):
                operations.append(op)
        
        return operations
    
    def identify_workflow_patterns(self) -> List[Workflow]:
        """
        Identify common workflow patterns using AI
        """
        print("\n🔮 Identifying workflow patterns...")
        
        # Common patterns based on script analysis
        patterns = [
            {
                "name": "Instagram Content Pipeline",
                "categories": ["Leonardo AI", "Image Processing", "Instagram Automation"],
                "operations": ["generate", "upload", "analyze"]
            },
            {
                "name": "Music Production Workflow",
                "categories": ["Suno Music", "Audio Transcription", "Gallery Generation"],
                "operations": ["generate", "transcribe", "organize", "gallery"]
            },
            {
                "name": "YouTube Automation",
                "categories": ["YouTube Automation", "AI Content Generation", "Audio Transcription"],
                "operations": ["generate", "transcribe", "upload", "analyze"]
            },
            {
                "name": "Content Analysis Pipeline",
                "categories": ["AI Content Generation", "Image Processing", "Gallery Generation"],
                "operations": ["download", "analyze", "organize", "gallery"]
            }
        ]
        
        for pattern in patterns:
            workflow = self._build_workflow_from_pattern(pattern)
            if workflow:
                self.workflows.append(workflow)
                print(f"   ✅ Created: {workflow.name}")
        
        return self.workflows
    
    def _build_workflow_from_pattern(self, pattern: Dict) -> Optional[Workflow]:
        """Build a workflow from a pattern"""
        relevant_scripts = []
        
        for category in pattern['categories']:
            if category in self.categories:
                # Get scripts from this category that match operations
                for script in self.categories[category]:
                    if any(op in script.operations for op in pattern['operations']):
                        relevant_scripts.append(script)
        
        if not relevant_scripts:
            return None
        
        # Calculate time savings
        manual_time = len(relevant_scripts) * 30  # 30 min per script manually
        auto_time = 10  # 10 minutes automated
        roi_score = (manual_time - auto_time) / manual_time
        
        # Build workflow steps
        steps = []
        for i, script in enumerate(relevant_scripts[:5], 1):  # Limit to 5 scripts
            steps.append({
                "step": i,
                "name": script.filename,
                "operation": script.operations[0] if script.operations else "process",
                "ai_enhancement": self._suggest_ai_enhancement(script)
            })
        
        workflow = Workflow(
            name=pattern['name'],
            description=f"Automated workflow combining {len(relevant_scripts)} scripts",
            scripts=relevant_scripts[:10],  # Top 10 scripts
            estimated_time_manual=manual_time,
            estimated_time_auto=auto_time,
            roi_score=roi_score,
            steps=steps,
            ai_enhancements=self._get_workflow_ai_enhancements(relevant_scripts)
        )
        
        return workflow
    
    def _suggest_ai_enhancement(self, script: Script) -> str:
        """Suggest AI enhancement for a script"""
        if 'analyze' in script.operations:
            return "Use Claude for deep analysis"
        elif 'generate' in script.operations:
            return "Use OpenAI GPT-5 for generation"
        elif 'transcribe' in script.operations:
            return "Use Whisper for transcription"
        elif 'upload' in script.operations:
            return "Use Grok for real-time verification"
        else:
            return "Use Groq for fast processing"
    
    def _get_workflow_ai_enhancements(self, scripts: List[Script]) -> List[str]:
        """Get AI enhancements for the entire workflow"""
        enhancements = []
        
        services = set()
        for script in scripts:
            services.update(script.services)
        
        if 'OpenAI' in services:
            enhancements.append("✨ GPT-5 for content generation and analysis")
        if 'Anthropic' in services:
            enhancements.append("🧠 Claude for deep reasoning and long-context tasks")
        if 'Instagram' in services:
            enhancements.append("📱 Groq for fast Instagram API interactions")
        
        # Add multi-model suggestions
        enhancements.append("🔄 Multi-model consensus for critical decisions")
        enhancements.append("⚡ Parallel processing with Groq for speed")
        enhancements.append("🎯 Intelligent routing based on task type")
        
        return enhancements
    
    def generate_workflow_code(self, workflow: Workflow) -> str:
        """
        Generate executable workflow code using AI
        """
        if not self.claude:
            return "# Claude not configured"
        
        prompt = f"""Generate a Python workflow automation script for:

Workflow: {workflow.name}
Description: {workflow.description}

Scripts to combine:
{chr(10).join([f"- {s.filename}: {s.purpose}" for s in workflow.scripts[:5]])}

Requirements:
1. Use async/await for parallel execution
2. Integrate with AI APIs: OpenAI, Claude, Grok, Groq
3. Add error handling and logging
4. Include progress tracking
5. Optimize for speed (current manual time: {workflow.estimated_time_manual} min)

Generate production-ready code with:
- Class-based architecture
- Type hints
- Comprehensive error handling
- Progress indicators
- AI-powered enhancements
"""
        
        response = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    def generate_report(self) -> str:
        """Generate comprehensive workflow analysis report"""
        report = []
        report.append("="*80)
        report.append("🔮 INTELLIGENT WORKFLOW ANALYSIS REPORT")
        report.append("="*80)
        report.append("")
        
        # Codebase stats
        report.append("📊 CODEBASE STATISTICS")
        report.append("-"*80)
        report.append(f"Total Scripts: {len(self.scripts)}")
        report.append(f"Total Lines: {sum(s.lines for s in self.scripts.values()):,}")
        report.append(f"Total Size: {sum(s.size_kb for s in self.scripts.values()):.1f} KB")
        report.append(f"Categories: {len(self.categories)}")
        report.append("")
        
        # Top categories
        report.append("🏆 TOP CATEGORIES")
        report.append("-"*80)
        top_categories = sorted(
            self.categories.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )[:10]
        
        for i, (cat, scripts) in enumerate(top_categories, 1):
            report.append(f"{i:2}. {cat:30} {len(scripts):3} scripts")
        report.append("")
        
        # Identified workflows
        report.append("🔗 IDENTIFIED WORKFLOWS")
        report.append("-"*80)
        
        total_time_saved = 0
        for i, wf in enumerate(self.workflows, 1):
            time_saved = wf.estimated_time_manual - wf.estimated_time_auto
            total_time_saved += time_saved
            
            report.append(f"\n{i}. {wf.name}")
            report.append(f"   Description: {wf.description}")
            report.append(f"   Scripts: {len(wf.scripts)}")
            report.append(f"   Time Saved: {time_saved} min/run ({wf.roi_score*100:.0f}% improvement)")
            report.append(f"   AI Enhancements:")
            for enh in wf.ai_enhancements[:3]:
                report.append(f"      • {enh}")
        
        report.append("")
        report.append("💰 ROI SUMMARY")
        report.append("-"*80)
        report.append(f"Total Time Saved (per run): {total_time_saved} minutes")
        report.append(f"Monthly Savings (20 runs): {total_time_saved * 20 / 60:.1f} hours")
        report.append(f"Annual Value (@$100/hr): ${(total_time_saved * 20 * 12 / 60) * 100:,.0f}")
        report.append("")
        
        return "\n".join(report)
    
    def save_workflows(self, output_dir: str = "workflows"):
        """Save all workflows to files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        for workflow in self.workflows:
            # Generate code
            code = self.generate_workflow_code(workflow)
            
            # Save to file
            safe_name = workflow.name.lower().replace(' ', '_').replace('-', '_')
            filepath = output_path / f"{safe_name}.py"
            
            with open(filepath, 'w') as f:
                f.write(code)
            
            print(f"   💾 Saved: {filepath}")
        
        # Save JSON summary
        summary = {
            "generated": str(datetime.now()),
            "total_workflows": len(self.workflows),
            "workflows": [
                {
                    "name": wf.name,
                    "description": wf.description,
                    "scripts_count": len(wf.scripts),
                    "time_manual": wf.estimated_time_manual,
                    "time_auto": wf.estimated_time_auto,
                    "roi_score": wf.roi_score
                }
                for wf in self.workflows
            ]
        }
        
        with open(output_path / "workflows_summary.json", 'w') as f:
            json.dump(summary, f, indent=2)


def main():
    """Main execution"""
    from datetime import datetime
    
    print("🔮 INTELLIGENT WORKFLOW BUILDER")
    print("="*70)
    print()
    
    # Initialize
    builder = IntelligentWorkflowBuilder()
    
    # Analyze codebase
    builder.analyze_codebase()
    
    # Identify workflows
    workflows = builder.identify_workflow_patterns()
    
    # Generate report
    report = builder.generate_report()
    print("\n" + report)
    
    # Save workflows
    print("\n💾 GENERATING WORKFLOW CODE...")
    builder.save_workflows()
    
    print("\n✅ Complete! Workflows saved to: ./workflows/")


if __name__ == "__main__":
    main()

