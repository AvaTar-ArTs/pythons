#!/usr/bin/env python3
"""
Intelligent Content-Awareness System for ~/Documents
Leverages full API ecosystem for semantic understanding

Usage:
    python intelligent_documents_analyzer.py [--analyze-all] [--search "query"] [--process-new]
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict
import hashlib

# Add .env.d to path for loader
sys.path.insert(0, str(Path.home() / '.env.d'))

# Try to load environment (may not work in all contexts)
try:
    # Import loader if available
    import subprocess
    result = subprocess.run(
        ['bash', '-c', 'source ~/.env.d/loader.sh llm-apis vector-memory && env'],
        capture_output=True,
        text=True
    )
    for line in result.stdout.split('\n'):
        if '=' in line:
            key, value = line.split('=', 1)
            os.environ[key] = value
except:
    pass

# API Clients (with fallbacks)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = bool(os.getenv('OPENAI_API_KEY'))
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = bool(os.getenv('ANTHROPIC_API_KEY'))
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False

try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False


class IntelligentDocumentsAnalyzer:
    """Main analyzer class for intelligent content awareness"""
    
    def __init__(self, documents_path: Optional[Path] = None):
        self.documents_path = documents_path or Path.home() / 'Documents'
        # Keep metadata in hidden folder, but script is visible
        self.intelligence_dir = self.documents_path / '.intelligence'
        self.intelligence_dir.mkdir(exist_ok=True)
        
        self.db_path = self.intelligence_dir / 'content_intelligence.db'
        self.metadata_path = self.intelligence_dir / 'metadata.json'
        self.processed_files = self.load_processed_files()
        
        # Initialize API clients
        self.openai = None
        self.anthropic = None
        self.qdrant = None
        self.chroma = None
        
        self.init_clients()
        
        # Content processors
        self.processors = {
            '.md': self.process_markdown,
            '.txt': self.process_text,
            '.rtf': self.process_text,
            '.py': self.process_code,
            '.sh': self.process_code,
            '.js': self.process_code,
            '.json': self.process_json,
            '.csv': self.process_data,
            '.pdf': self.process_pdf,
        }
        
        # Ignore patterns
        self.ignore_patterns = [
            '.git', '.DS_Store', '__pycache__', '.pyc',
            'node_modules', '.intelligence', '_temp'
        ]
    
    def init_clients(self):
        """Initialize API clients"""
        if OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY'):
            try:
                self.openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
                print("✅ OpenAI client initialized")
            except Exception as e:
                print(f"⚠️  OpenAI init error: {e}")
        
        if ANTHROPIC_AVAILABLE and os.getenv('ANTHROPIC_API_KEY'):
            try:
                self.anthropic = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
                print("✅ Anthropic client initialized")
            except Exception as e:
                print(f"⚠️  Anthropic init error: {e}")
        
        if QDRANT_AVAILABLE:
            try:
                self.qdrant = QdrantClient(host="localhost", port=6333)
                # Create collection if doesn't exist
                try:
                    self.qdrant.get_collection("documents")
                except:
                    self.qdrant.create_collection(
                        collection_name="documents",
                        vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
                    )
                print("✅ Qdrant client initialized")
            except Exception as e:
                print(f"⚠️  Qdrant init error: {e}")
        
        if CHROMADB_AVAILABLE:
            try:
                self.chroma = chromadb.Client()
                print("✅ ChromaDB client initialized")
            except Exception as e:
                print(f"⚠️  ChromaDB init error: {e}")
    
    def load_processed_files(self) -> Dict[str, datetime]:
        """Load list of processed files"""
        if self.metadata_path.exists():
            try:
                data = json.loads(self.metadata_path.read_text())
                return {
                    k: datetime.fromisoformat(v) 
                    for k, v in data.get('processed_files', {}).items()
                }
            except:
                return {}
        return {}
    
    def save_processed_files(self):
        """Save processed files metadata"""
        data = {
            'processed_files': {
                k: v.isoformat() 
                for k, v in self.processed_files.items()
            },
            'last_updated': datetime.now().isoformat()
        }
        self.metadata_path.write_text(json.dumps(data, indent=2))
    
    def should_process(self, file_path: Path) -> bool:
        """Check if file should be processed"""
        # Check ignore patterns
        if any(pattern in str(file_path) for pattern in self.ignore_patterns):
            return False
        
        # Check if already processed recently
        file_str = str(file_path)
        if file_str in self.processed_files:
            file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            if file_mtime <= self.processed_files[file_str]:
                return False
        
        return True
    
    def analyze_document(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze a single document"""
        if not self.should_process(file_path):
            return None
        
        try:
            ext = file_path.suffix.lower()
            processor = self.processors.get(ext, self.process_generic)
            
            print(f"  📄 Processing: {file_path.name}")
            analysis = processor(file_path)
            
            if analysis:
                analysis['file'] = str(file_path.relative_to(self.documents_path))
                analysis['full_path'] = str(file_path)
                analysis['processed_at'] = datetime.now().isoformat()
                analysis['file_size'] = file_path.stat().st_size
                analysis['file_hash'] = self.file_hash(file_path)
                
                # Store in vector DB if available
                if analysis.get('embedding') and self.qdrant:
                    self.store_in_vector_db(analysis)
                
                # Update processed files
                self.processed_files[str(file_path)] = datetime.now()
                
                return analysis
        except Exception as e:
            print(f"  ⚠️  Error processing {file_path}: {e}")
            return None
    
    def file_hash(self, file_path: Path) -> str:
        """Calculate file hash"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except:
            return ""
    
    def process_markdown(self, file_path: Path) -> Dict[str, Any]:
        """Process markdown with semantic analysis"""
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        analysis = {
            'type': 'markdown',
            'content_preview': content[:500],
            'line_count': len(content.split('\n')),
            'word_count': len(content.split()),
        }
        
        # Extract topics
        if self.anthropic and len(content) > 100:
            analysis['topics'] = self.extract_topics_claude(content[:4000])
        
        # Generate summary
        if self.openai and len(content) > 200:
            analysis['summary'] = self.generate_summary_openai(content[:4000])
        
        # Create embedding
        if self.openai:
            analysis['embedding'] = self.create_embedding(content[:8000])
        
        # Extract metadata
        analysis['metadata'] = self.extract_markdown_metadata(content)
        
        return analysis
    
    def process_text(self, file_path: Path) -> Dict[str, Any]:
        """Process text files"""
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        analysis = {
            'type': 'text',
            'content_preview': content[:500],
            'line_count': len(content.split('\n')),
            'word_count': len(content.split()),
        }
        
        if self.openai and len(content) > 200:
            analysis['summary'] = self.generate_summary_openai(content[:4000])
            analysis['embedding'] = self.create_embedding(content[:8000])
        
        return analysis
    
    def process_code(self, file_path: Path) -> Dict[str, Any]:
        """Process code files"""
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        analysis = {
            'type': 'code',
            'language': file_path.suffix[1:],
            'line_count': len(content.split('\n')),
            'content_preview': content[:500],
        }
        
        # Extract functions/classes (simple regex)
        functions = self.extract_functions(content, file_path.suffix)
        if functions:
            analysis['functions'] = functions
        
        if self.openai:
            analysis['embedding'] = self.create_embedding(content[:8000])
            analysis['code_summary'] = self.summarize_code_openai(content[:2000])
        
        return analysis
    
    def extract_functions(self, content: str, ext: str) -> List[str]:
        """Extract function/class names"""
        functions = []
        
        if ext == '.py':
            import re
            # Find function definitions
            func_pattern = r'def\s+(\w+)\s*\('
            functions.extend(re.findall(func_pattern, content))
            # Find class definitions
            class_pattern = r'class\s+(\w+)'
            functions.extend(re.findall(class_pattern, content))
        
        return functions[:10]  # Limit to 10
    
    def process_json(self, file_path: Path) -> Dict[str, Any]:
        """Process JSON files"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            data = json.loads(content)
            
            analysis = {
                'type': 'json',
                'is_valid': True,
                'structure': self.analyze_json_structure(data),
            }
            
            if self.openai:
                analysis['embedding'] = self.create_embedding(str(data)[:8000])
            
            return analysis
        except:
            return {
                'type': 'json',
                'is_valid': False,
            }
    
    def analyze_json_structure(self, data: Any, depth: int = 0) -> Dict:
        """Analyze JSON structure"""
        if depth > 3:
            return {'type': 'deep'}
        
        if isinstance(data, dict):
            return {
                'type': 'object',
                'keys': list(data.keys())[:20],
                'count': len(data)
            }
        elif isinstance(data, list):
            return {
                'type': 'array',
                'length': len(data),
                'sample_type': type(data[0]).__name__ if data else None
            }
        else:
            return {'type': type(data).__name__}
    
    def process_data(self, file_path: Path) -> Dict[str, Any]:
        """Process data files (CSV, etc.)"""
        analysis = {
            'type': 'data',
            'format': file_path.suffix[1:],
        }
        
        if file_path.suffix == '.csv':
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
                analysis['row_count'] = len([l for l in lines if l.strip()])
                analysis['headers'] = lines[0].split(',')[:10] if lines else []
            except:
                pass
        
        return analysis
    
    def process_pdf(self, file_path: Path) -> Dict[str, Any]:
        """Process PDF files (basic)"""
        return {
            'type': 'pdf',
            'note': 'PDF processing requires PDF.ai or similar service'
        }
    
    def process_generic(self, file_path: Path) -> Dict[str, Any]:
        """Process generic files"""
        return {
            'type': 'generic',
            'extension': file_path.suffix,
            'size': file_path.stat().st_size
        }
    
    def extract_markdown_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from markdown frontmatter"""
        metadata = {}
        
        # Check for YAML frontmatter
        if content.startswith('---'):
            try:
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    import yaml
                    metadata = yaml.safe_load(parts[1]) or {}
            except:
                pass
        
        # Extract headings
        import re
        headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        if headings:
            metadata['headings'] = headings[:10]
        
        return metadata
    
    def extract_topics_claude(self, content: str) -> List[str]:
        """Extract topics using Claude"""
        if not self.anthropic:
            return []
        
        try:
            prompt = f"""Analyze this document and extract the main topics.
Return a JSON array of 3-5 topic strings.

Document excerpt:
{content}

Return only the JSON array, no other text."""
            
            response = self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            
            text = response.content[0].text.strip()
            # Try to parse JSON
            if text.startswith('['):
                return json.loads(text)
            else:
                # Fallback: extract from text
                return [t.strip() for t in text.split(',')[:5]]
        except Exception as e:
            print(f"    ⚠️  Topic extraction error: {e}")
            return []
    
    def generate_summary_openai(self, content: str) -> str:
        """Generate summary using OpenAI"""
        if not self.openai:
            return ""
        
        try:
            response = self.openai.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{
                    "role": "system",
                    "content": "You are a document summarizer. Create concise 2-3 sentence summaries."
                }, {
                    "role": "user",
                    "content": f"Summarize this document:\n\n{content}"
                }],
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"    ⚠️  Summary generation error: {e}")
            return ""
    
    def summarize_code_openai(self, content: str) -> str:
        """Summarize code using OpenAI"""
        if not self.openai:
            return ""
        
        try:
            response = self.openai.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{
                    "role": "system",
                    "content": "You are a code analyzer. Summarize what this code does in one sentence."
                }, {
                    "role": "user",
                    "content": f"Summarize:\n\n{content}"
                }],
                max_tokens=100
            )
            
            return response.choices[0].message.content.strip()
        except:
            return ""
    
    def create_embedding(self, content: str) -> List[float]:
        """Create embedding vector"""
        if not self.openai:
            return []
        
        try:
            response = self.openai.embeddings.create(
                model="text-embedding-3-large",
                input=content[:8000]
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"    ⚠️  Embedding error: {e}")
            return []
    
    def store_in_vector_db(self, analysis: Dict[str, Any]):
        """Store in Qdrant"""
        if not self.qdrant or not analysis.get('embedding'):
            return
        
        try:
            file_id = hash(analysis['file'])
            
            self.qdrant.upsert(
                collection_name="documents",
                points=[PointStruct(
                    id=file_id,
                    vector=analysis['embedding'],
                    payload={
                        'file': analysis['file'],
                        'type': analysis.get('type', 'unknown'),
                        'topics': analysis.get('topics', []),
                        'summary': analysis.get('summary', ''),
                        'metadata': analysis.get('metadata', {}),
                        'processed_at': analysis.get('processed_at', ''),
                    }
                )]
            )
        except Exception as e:
            print(f"    ⚠️  Vector DB storage error: {e}")
    
    def semantic_search(self, query: str, limit: int = 10) -> List[Dict]:
        """Semantic search across documents"""
        if not self.qdrant or not self.openai:
            print("⚠️  Semantic search requires OpenAI and Qdrant")
            return []
        
        try:
            query_embedding = self.create_embedding(query)
            
            results = self.qdrant.search(
                collection_name="documents",
                query_vector=query_embedding,
                limit=limit
            )
            
            return [hit.payload for hit in results]
        except Exception as e:
            print(f"⚠️  Search error: {e}")
            return []
    
    def process_all(self, limit: Optional[int] = None):
        """Process all documents"""
        print("🧠 Starting Intelligent Content Analysis...")
        print(f"📁 Analyzing: {self.documents_path}\n")
        
        files_processed = 0
        analyses = []
        
        # Get all files
        all_files = list(self.documents_path.rglob('*'))
        total_files = len([f for f in all_files if f.is_file()])
        
        print(f"📊 Found {total_files} files to process\n")
        
        for file_path in all_files:
            if limit and files_processed >= limit:
                break
            
            if file_path.is_file():
                analysis = self.analyze_document(file_path)
                if analysis:
                    analyses.append(analysis)
                    files_processed += 1
                    
                    if files_processed % 10 == 0:
                        print(f"  ✅ Processed {files_processed} files...")
        
        # Save results
        results_path = self.intelligence_dir / f'analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        results_path.write_text(json.dumps(analyses, indent=2))
        
        # Save processed files
        self.save_processed_files()
        
        print(f"\n✅ Processed {files_processed} files")
        print(f"📄 Results saved to: {results_path}")
        
        return analyses
    
    def process_new(self):
        """Process only new/modified files"""
        print("🔄 Processing new/modified files...\n")
        return self.process_all()
    
    def generate_report(self):
        """Generate analysis report"""
        print("📊 Generating report...")
        
        # Load latest analysis
        analysis_files = sorted(self.intelligence_dir.glob('analysis_*.json'))
        if not analysis_files:
            print("⚠️  No analysis files found. Run --analyze-all first.")
            return
        
        latest = json.loads(analysis_files[-1].read_text())
        
        # Generate statistics
        stats = defaultdict(int)
        for analysis in latest:
            stats[analysis.get('type', 'unknown')] += 1
        
        print("\n📈 Content Statistics:")
        print("=" * 50)
        for file_type, count in sorted(stats.items(), key=lambda x: -x[1]):
            print(f"  {file_type:20} {count:>5} files")
        
        print(f"\n📁 Total files analyzed: {len(latest)}")


def main():
    parser = argparse.ArgumentParser(description='Intelligent Documents Analyzer')
    parser.add_argument('--analyze-all', action='store_true', help='Analyze all documents')
    parser.add_argument('--process-new', action='store_true', help='Process new/modified files')
    parser.add_argument('--search', type=str, help='Semantic search query')
    parser.add_argument('--limit', type=int, help='Limit number of files to process')
    parser.add_argument('--report', action='store_true', help='Generate report')
    
    args = parser.parse_args()
    
    analyzer = IntelligentDocumentsAnalyzer()
    
    if args.search:
        results = analyzer.semantic_search(args.search)
        print(f"\n🔍 Search results for: '{args.search}'\n")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.get('file', 'unknown')}")
            if result.get('summary'):
                print(f"   {result['summary'][:100]}...")
            print()
    elif args.analyze_all:
        analyzer.process_all(limit=args.limit)
    elif args.process_new:
        analyzer.process_new()
    elif args.report:
        analyzer.generate_report()
    else:
        print("🧠 Intelligent Documents Analyzer")
        print("\nUsage:")
        print("  --analyze-all    Analyze all documents")
        print("  --process-new    Process new/modified files")
        print("  --search QUERY   Semantic search")
        print("  --report         Generate report")
        print("  --limit N        Limit processing to N files")


if __name__ == '__main__':
    main()

