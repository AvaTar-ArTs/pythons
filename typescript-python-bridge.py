#!/usr/bin/env python3
"""
🌉 TypeScript-Python Content Awareness Bridge
==============================================

Bridges your TypeScript deepContentAwareness.ts system with Python AI automation

Features:
- Bi-directional communication (TS ↔ Python)
- Shared data structures (Asset, TagScore, ProcessResult)
- Semantic embedding compatibility
- Tag inference integration
- Multi-model processing
"""

# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)
from pathlib import Path as PathLib

def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
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
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")

load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass

import os
import json
import subprocess
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np
from openai import OpenAI


@dataclass
class TSAsset:
    """Python equivalent of TypeScript Asset interface"""
    id: str
    content: str
    comments: Optional[str] = None
    context_metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict:
        """Convert to dict for JSON serialization"""
        return {
            "id": self.id,
            "content": self.content,
            "comments": self.comments,
            "contextMetadata": self.context_metadata or {}
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TSAsset':
        """Create from TypeScript JSON output"""
        return cls(
            id=data['id'],
            content=data['content'],
            comments=data.get('comments'),
            context_metadata=data.get('contextMetadata')
        )


@dataclass
class TSTagScore:
    """Python equivalent of TypeScript TagScore interface"""
    tag: str
    score: float
    
    def to_dict(self) -> Dict:
        return {"tag": self.tag, "score": self.score}
    
    @classmethod
    from_dict(cls, data: Dict) -> 'TSTagScore':
        return cls(tag=data['tag'], score=data['score'])


@dataclass
class TSProcessResult:
    """Python equivalent of TypeScript ProcessResult interface"""
    asset_id: str
    tags: List[str]
    tag_scores: List[TSTagScore]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        return {
            "assetId": self.asset_id,
            "tags": self.tags,
            "tagScores": [ts.to_dict() for ts in self.tag_scores],
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TSProcessResult':
        return cls(
            asset_id=data['assetId'],
            tags=data['tags'],
            tag_scores=[TSTagScore.from_dict(ts) for ts in data['tagScores']],
            metadata=data['metadata']
        )


class TypeScriptBridge:
    """
    Bridge between TypeScript content awareness and Python AI systems
    """
    
    def __init__(self, ts_script_path: str = "deepContentAwareness.ts"):
        self.ts_script_path = Path(ts_script_path)
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Temp directory for TS-Python communication
        self.comm_dir = Path("/tmp/ts_python_bridge")
        self.comm_dir.mkdir(exist_ok=True)
    
    def call_typescript_analysis(self, asset: TSAsset) -> TSProcessResult:
        """
        Call TypeScript deepContentAwareness system
        
        Writes asset to JSON, calls TS script, reads result
        """
        # Write input
        input_file = self.comm_dir / "asset_input.json"
        with open(input_file, 'w') as f:
            json.dump(asset.to_dict(), f, indent=2)
        
        # Call TypeScript (would need to compile first)
        # For now, we'll simulate the TS functionality in Python
        result = self._simulate_ts_processing(asset)
        
        return result
    
    def _simulate_ts_processing(self, asset: TSAsset) -> TSProcessResult:
        """
        Simulate TypeScript processing in Python
        (until TS integration is fully set up)
        """
        # 1. Semantic embedding
        embedding = self._generate_embedding(asset)
        
        # 2. Tag inference
        tags, tag_scores = self._infer_tags(asset, embedding)
        
        # 3. Context enrichment
        metadata = self._enrich_metadata(asset)
        
        return TSProcessResult(
            asset_id=asset.id,
            tags=tags,
            tag_scores=tag_scores,
            metadata=metadata
        )
    
    def _generate_embedding(self, asset: TSAsset) -> np.ndarray:
        """Generate semantic embedding (matches TS SemanticEmbedder)"""
        text = f"{asset.content} {asset.comments or ''}"
        
        response = self.openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        
        return np.array(response.data[0].embedding)
    
    def _infer_tags(self, asset: TSAsset, embedding: np.ndarray) -> Tuple[List[str], List[TSTagScore]]:
        """Infer tags (matches TS TagInference)"""
        # Use GPT-4 for tag inference
        prompt = f"""Analyze this content and suggest relevant tags with confidence scores:

Content: {asset.content[:500]}

Provide 10 tags with scores 0.0-1.0.
Output as JSON: {{"tags": [{{"tag": "example", "score": 0.95}}]}}"""
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            tag_data = result.get('tags', [])
            
            tags = [t['tag'] for t in tag_data]
            tag_scores = [TSTagScore(tag=t['tag'], score=t['score']) for t in tag_data]
            
            return tags, tag_scores
        except:
            return [], []
    
    def _enrich_metadata(self, asset: TSAsset) -> Dict[str, Any]:
        """Enrich with metadata (matches TS ContextualAnalyzer)"""
        return {
            "processed_at": str(Path.cwd()),
            "content_length": len(asset.content),
            "has_comments": asset.comments is not None,
            "python_processed": True
        }
    
    def batch_process_assets(self, assets: List[TSAsset], threshold: float = 0.65) -> List[TSProcessResult]:
        """
        Batch process multiple assets
        """
        results = []
        
        for asset in assets:
            result = self.call_typescript_analysis(asset)
            
            # Filter tags by threshold
            filtered_scores = [ts for ts in result.tag_scores if ts.score >= threshold]
            result.tag_scores = filtered_scores
            result.tags = [ts.tag for ts in filtered_scores]
            
            results.append(result)
        
        return results
    
    def export_for_typescript(self, assets: List[TSAsset], filepath: str):
        """Export assets in TypeScript-compatible format"""
        ts_data = {
            "assets": [asset.to_dict() for asset in assets],
            "count": len(assets),
            "generated_by": "Python Bridge",
            "timestamp": str(Path.ctime(Path.cwd()))
        }
        
        with open(filepath, 'w') as f:
            json.dump(ts_data, f, indent=2)
        
        print(f"✅ Exported {len(assets)} assets to: {filepath}")
    
    def import_from_typescript(self, filepath: str) -> List[TSAsset]:
        """Import assets from TypeScript output"""
        with open(filepath) as f:
            data = json.load(f)
        
        assets = [TSAsset.from_dict(asset_data) for asset_data in data.get('assets', [])]
        
        print(f"✅ Imported {len(assets)} assets from: {filepath}")
        return assets


# ==================== Integration Examples ====================

def example_python_to_typescript():
    """Example: Process in Python, export for TypeScript"""
    bridge = TypeScriptBridge()
    
    # Create sample assets
    assets = [
        TSAsset(
            id="doc_001",
            content="This is a comprehensive guide to AI automation...",
            comments="Target: developers"
        ),
        TSAsset(
            id="doc_002",
            content="Building YouTube content with Make.com and GPT-4...",
            comments="Focus on practical examples"
        )
    ]
    
    # Process with Python AI
    results = bridge.batch_process_assets(assets)
    
    # Export for TypeScript
    bridge.export_for_typescript(assets, "assets_for_ts.json")
    
    return results


def example_typescript_to_python():
    """Example: Import TypeScript results, enhance with Python"""
    bridge = TypeScriptBridge()
    
    # Import from TypeScript
    assets = bridge.import_from_typescript("ts_output.json")
    
    # Further processing with Python AI
    for asset in assets:
        # Add Python-specific enhancements
        asset.context_metadata = asset.context_metadata or {}
        asset.context_metadata['python_enhanced'] = True
    
    return assets


if __name__ == "__main__":
    print("🌉 TypeScript-Python Content Awareness Bridge")
    print("="*70)
    print()
    
    # Demo
    results = example_python_to_typescript()
    
    print(f"\n✅ Processed {len(results)} assets")
    for result in results:
        print(f"\n📄 Asset: {result.asset_id}")
        print(f"   Tags: {', '.join(result.tags[:5])}")
        print(f"   Top score: {result.tag_scores[0].tag if result.tag_scores else 'N/A'}")

