#!/usr/bin/env python3
"""
Context7 REST API Client
Programmatic access to Context7 library documentation
Uses the REST API: https://context7.com/api/v2
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
import ssl

# Load environment from ~/.env.d/
env_dir = Path.home() / '.env.d'
if env_dir.exists():
    from dotenv import load_dotenv
    for env_file in env_dir.glob('*.env'):
        load_dotenv(env_file, override=False)

class Context7APIClient:
    """Client for Context7 REST API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('CONTEXT7_API_KEY')
        self.base_url = "https://context7.com/api/v2"
        self.mcp_url = "https://mcp.context7.com/mcp"
        
        if not self.api_key:
            raise ValueError("CONTEXT7_API_KEY not found. Add it to ~/.env.d/llm-apis.env")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # SSL context for macOS certificate handling
        self.ssl_context = ssl.create_default_context()
        try:
            self.ssl_context.check_hostname = False
            self.ssl_context.verify_mode = ssl.CERT_NONE
        except:
            pass  # Use default if can't modify
    
    def search_libraries(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for libraries in Context7
        
        Args:
            query: Search term (e.g., "next.js", "pillow", "pandas")
            limit: Maximum number of results
            
        Returns:
            List of library results
        """
        url = f"{self.base_url}/search"
        params = {"query": query}
        
        try:
            # Build URL with query params
            full_url = f"{url}?{urlencode(params)}"
            req = Request(full_url, headers=self.headers)
            
            with urlopen(req, timeout=10, context=self.ssl_context) as response:
                data = json.loads(response.read().decode())
                return data.get('results', [])[:limit]
        except (HTTPError, URLError) as e:
            print(f"❌ Error searching Context7: {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return []
    
    def get_library_docs(self, library_id: str) -> Optional[Dict[str, Any]]:
        """
        Get documentation for a specific library
        
        Args:
            library_id: Library ID (e.g., "/websites/nextjs", "/vercel/next.js")
            
        Returns:
            Library documentation data
        """
        # Note: Check Context7 API docs for exact endpoint
        # This is a placeholder based on typical REST API patterns
        url = f"{self.base_url}/libraries/{library_id}"
        
        try:
            req = Request(url, headers=self.headers)
            with urlopen(req, timeout=10, context=self.ssl_context) as response:
                return json.loads(response.read().decode())
        except (HTTPError, URLError) as e:
            print(f"❌ Error fetching library docs: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def find_library_for_codebase(self, library_name: str) -> Optional[Dict[str, Any]]:
        """
        Find the best matching library in Context7 for a library name
        
        Args:
            library_name: Name of library (e.g., "Pillow", "pandas", "requests")
            
        Returns:
            Best matching library result
        """
        results = self.search_libraries(library_name, limit=5)
        
        if not results:
            return None
        
        # Find best match (highest trust score or stars)
        best_match = max(results, key=lambda x: (
            x.get('trustScore', 0),
            x.get('stars', 0),
            x.get('benchmarkScore', 0)
        ))
        
        return best_match
    
    def get_documentation_snippet(self, library_id: str, query: str) -> Optional[str]:
        """
        Get a specific documentation snippet for a library
        
        Args:
            library_id: Library ID
            query: What you're looking for (e.g., "resize image", "dataframe merge")
            
        Returns:
            Documentation snippet text
        """
        # Note: Check Context7 API docs for exact endpoint
        # This might be part of the MCP protocol, not REST API
        url = f"{self.base_url}/libraries/{library_id}/snippets"
        params = {"query": query}
        
        try:
            full_url = f"{url}?{urlencode(params)}"
            req = Request(full_url, headers=self.headers)
            with urlopen(req, timeout=10, context=self.ssl_context) as response:
                data = json.loads(response.read().decode())
                return data.get('snippet', '')
        except (HTTPError, URLError) as e:
            print(f"❌ Error fetching snippet: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None


class Context7CodebaseIntegrator:
    """Integrate Context7 with your codebase"""
    
    def __init__(self):
        self.client = Context7APIClient()
        self.pythons_dir = Path.home() / 'pythons'
        self.context7_dir = self.pythons_dir / '.context7'
        self.context7_dir.mkdir(exist_ok=True)
    
    def analyze_and_fetch_docs(self):
        """Analyze your codebase and fetch relevant Context7 docs"""
        print("🔍 Analyzing codebase and fetching Context7 documentation...")
        print("=" * 80)
        
        # Load existing index
        index_file = self.context7_dir / 'codebase_index.json'
        if not index_file.exists():
            print("⚠️  No codebase index found. Run context7_codebase_indexer.py first.")
            return
        
        with open(index_file) as f:
            index = json.load(f)
        
        libraries = index.get('libraries', {})
        top_libraries = sorted(
            libraries.items(),
            key=lambda x: x[1].get('usage_count', 0),
            reverse=True
        )[:20]  # Top 20 libraries
        
        print(f"\n📚 Fetching Context7 docs for top {len(top_libraries)} libraries...\n")
        
        library_docs = {}
        for lib_name, lib_info in top_libraries:
            print(f"  🔍 Searching for: {lib_name}...", end=' ')
            
            result = self.client.find_library_for_codebase(lib_name)
            if result:
                library_docs[lib_name] = {
                    'context7_id': result.get('id'),
                    'title': result.get('title'),
                    'description': result.get('description'),
                    'trust_score': result.get('trustScore'),
                    'benchmark_score': result.get('benchmarkScore'),
                    'last_updated': result.get('lastUpdateDate'),
                    'versions': result.get('versions', []),
                    'total_snippets': result.get('totalSnippets', 0)
                }
                print(f"✅ Found: {result.get('title')}")
            else:
                print("❌ Not found in Context7")
        
        # Save results
        docs_file = self.context7_dir / 'context7_library_docs.json'
        with open(docs_file, 'w') as f:
            json.dump({
                'generated_at': datetime.now().isoformat(),
                'libraries': library_docs
            }, f, indent=2)
        
        print(f"\n✅ Documentation mapping saved: {docs_file}")
        
        # Generate summary
        self.generate_integration_summary(library_docs)
    
    def generate_integration_summary(self, library_docs: Dict):
        """Generate integration summary"""
        md_file = self.context7_dir / 'CONTEXT7_LIBRARY_MAPPING.md'
        
        with open(md_file, 'w') as f:
            f.write("# Context7 Library Mapping\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## 📚 Your Libraries in Context7\n\n")
            f.write("| Your Library | Context7 ID | Trust Score | Snippets |\n")
            f.write("|--------------|-------------|-------------|----------|\n")
            
            for lib_name, doc_info in sorted(library_docs.items()):
                ctx7_id = doc_info.get('context7_id', 'N/A')
                trust = doc_info.get('trust_score', 'N/A')
                snippets = doc_info.get('total_snippets', 'N/A')
                f.write(f"| `{lib_name}` | `{ctx7_id}` | {trust} | {snippets:,} |\n")
            
            f.write("\n## 💡 Usage\n\n")
            f.write("### In Cursor/Warp (MCP):\n")
            f.write("```\n")
            f.write("Create a function to resize images using Pillow. use context7\n")
            f.write("```\n\n")
            f.write("### Via REST API (Python):\n")
            f.write("```python\n")
            f.write("from context7_api_client import Context7APIClient\n")
            f.write("client = Context7APIClient()\n")
            f.write("results = client.search_libraries('pillow')\n")
            f.write("```\n")
        
        print(f"  ✅ Summary saved: {md_file}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Context7 API Client')
    parser.add_argument('--search', type=str, help='Search for a library')
    parser.add_argument('--integrate', action='store_true', help='Integrate with codebase')
    
    args = parser.parse_args()
    
    if args.integrate:
        integrator = Context7CodebaseIntegrator()
        integrator.analyze_and_fetch_docs()
    elif args.search:
        client = Context7APIClient()
        results = client.search_libraries(args.search)
        print(f"\n📚 Found {len(results)} results for '{args.search}':\n")
        for result in results:
            print(f"  • {result.get('title')} ({result.get('id')})")
            print(f"    Trust: {result.get('trustScore')}, Snippets: {result.get('totalSnippets')}")
    else:
        print("Usage:")
        print("  python context7_api_client.py --search 'pillow'")
        print("  python context7_api_client.py --integrate")


if __name__ == '__main__':
    main()
