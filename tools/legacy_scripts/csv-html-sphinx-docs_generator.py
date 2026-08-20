#!/usr/bin/env python3
"""
Conversations Documentation Generator
Creates Sphinx/PyDocs-style HTML documentation from CSV conversation files.
"""

import csv
import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple
import html


class ConversationDocGenerator:
    """Generate Sphinx-style documentation from conversation CSVs."""

    def __init__(self, conversations_dir: str, output_dir: str = None):
        self.conversations_dir = Path(conversations_dir)
        if output_dir is None:
            self.output_dir = self.conversations_dir / 'docs'
        else:
            self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.conversations = []
        self.topics = defaultdict(list)
        self.content_types = defaultdict(list)
        self.actions = defaultdict(list)

    def load_conversations(self):
        """Load all CSV conversation files."""
        csv_files = list(self.conversations_dir.glob('*.csv'))
        csv_files = [f for f in csv_files if '_IMPROVED' not in f.name]

        print(f"📚 Loading {len(csv_files)} conversation files...")

        for csv_file in csv_files:
            try:
                conv = self._parse_csv(csv_file)
                if conv:
                    self.conversations.append(conv)
                    # Index by topics
                    for topic in conv.get('topics', []):
                        self.topics[topic].append(conv)
                    # Index by content type
                    for ctype in conv.get('content_types', []):
                        self.content_types[ctype].append(conv)
                    # Index by actions
                    for action in conv.get('actions', []):
                        self.actions[action].append(conv)
            except Exception as e:
                print(f"  ⚠️  Error loading {csv_file.name}: {e}")

        print(f"✅ Loaded {len(self.conversations)} conversations")

    def _parse_csv(self, csv_file: Path) -> Dict:
        """Parse a single CSV file."""
        conv = {
            'filename': csv_file.name,
            'filepath': str(csv_file),
            'title': self._extract_title(csv_file.name),
            'messages': [],
            'topics': set(),
            'content_types': set(),
            'actions': set(),
            'date_range': {'first': None, 'last': None},
            'stats': {
                'total_messages': 0,
                'human_messages': 0,
                'assistant_messages': 0,
            }
        }

        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    role = row.get('Role', '')
                    content = row.get('Content', '')
                    timestamp = row.get('Timestamp', '')

                    if role:
                        conv['messages'].append({
                            'role': role,
                            'content': content,
                            'timestamp': timestamp,
                        })

                        conv['stats']['total_messages'] += 1
                        if role == 'Human':
                            conv['stats']['human_messages'] += 1
                        elif role == 'Assistant':
                            conv['stats']['assistant_messages'] += 1

                            # Extract metadata
                            topics = self._extract_topics(content)
                            conv['topics'].update(topics)

                            content_type = self._classify_content(content)
                            if content_type:
                                conv['content_types'].add(content_type)

                            actions = self._extract_actions(content)
                            conv['actions'].update(actions)

                    if timestamp:
                        try:
                            date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                            if not conv['date_range']['first'] or date < conv['date_range']['first']:
                                conv['date_range']['first'] = date
                            if not conv['date_range']['last'] or date > conv['date_range']['last']:
                                conv['date_range']['last'] = date
                        except:
                            pass

            # Convert sets to lists for JSON serialization
            conv['topics'] = sorted(list(conv['topics']))
            conv['content_types'] = sorted(list(conv['content_types']))
            conv['actions'] = sorted(list(conv['actions']))

            return conv if conv['messages'] else None
        except Exception as e:
            print(f"    Error parsing {csv_file.name}: {e}")
            return None

    def _extract_title(self, filename: str) -> str:
        """Extract a readable title from filename."""
        # Remove .csv extension
        title = filename.replace('.csv', '')
        # Remove hash suffix
        title = re.sub(r'_[a-f0-9]{6}$', '', title)
        # Replace underscores with spaces
        title = title.replace('_', ' ')
        # Title case
        title = ' '.join(word.capitalize() for word in title.split())
        return title

    def _extract_topics(self, content: str) -> List[str]:
        """Extract topics from content."""
        topics = []
        content_lower = content.lower()

        topic_keywords = {
            'python': ['python', 'script', 'code', 'programming'],
            'ai': ['ai', 'artificial intelligence', 'model', 'claude'],
            'automation': ['automation', 'workflow', 'process'],
            'design': ['design', 'ui', 'ux', 'interface', 'css'],
            'data': ['data', 'csv', 'json', 'database', 'organize'],
            'web': ['web', 'html', 'website', 'browser'],
            'creative': ['creative', 'art', 'image', 'gallery'],
            'social': ['social media', 'linkedin', 'instagram', 'twitter'],
            'business': ['business', 'strategy', 'growth', 'marketing'],
            'technical': ['technical', 'api', 'server', 'terminal'],
        }

        for topic, keywords in topic_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                topics.append(topic)

        return topics[:5]

    def _classify_content(self, content: str) -> str:
        """Classify content type."""
        content_lower = content.lower()

        if any(word in content_lower for word in ['analysis', 'analyze', 'analyzing']):
            return 'Analysis'
        elif any(word in content_lower for word in ['created', 'generated', 'built']):
            return 'Creation'
        elif any(word in content_lower for word in ['explain', 'describe', 'summary']):
            return 'Explanation'
        elif any(word in content_lower for word in ['fix', 'error', 'issue']):
            return 'Troubleshooting'
        elif any(word in content_lower for word in ['improve', 'enhance', 'optimize']):
            return 'Improvement'
        return 'Response'

    def _extract_actions(self, content: str) -> List[str]:
        """Extract actions from content."""
        actions = []
        content_lower = content.lower()

        action_patterns = {
            'created': r'created|built|generated|made',
            'organized': r'organized|sorted|structured',
            'analyzed': r'analyzed|examined|reviewed',
            'improved': r'improved|enhanced|optimized',
            'fixed': r'fixed|resolved|corrected',
            'converted': r'converted|transformed|changed',
        }

        for action, pattern in action_patterns.items():
            if re.search(pattern, content_lower):
                actions.append(action)

        return actions[:3]

    def generate_docs(self):
        """Generate all documentation files."""
        print("\n🔨 Generating documentation...")

        # Create directory structure
        (self.output_dir / 'topics').mkdir(exist_ok=True)
        (self.output_dir / 'conversations').mkdir(exist_ok=True)
        (self.output_dir / 'static').mkdir(exist_ok=True)

        # Generate CSS
        self._generate_css()

        # Generate index
        self._generate_index()

        # Generate topic pages
        self._generate_topic_pages()

        # Generate individual conversation pages
        self._generate_conversation_pages()

        # Generate search page
        self._generate_search_page()

        # Generate sitemap
        self._generate_sitemap()

        print(f"\n✅ Documentation generated in: {self.output_dir}")
        print(f"   📄 Open index.html to view")

    def _generate_css(self):
        """Generate CSS stylesheet."""
        css = """/* Sphinx-style Documentation CSS */

:root {
    --primary-color: #2980b9;
    --secondary-color: #34495e;
    --accent-color: #e74c3c;
    --bg-color: #ffffff;
    --sidebar-bg: #f8f9fa;
    --text-color: #333;
    --border-color: #e0e0e0;
    --code-bg: #f4f4f4;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background: var(--bg-color);
}

.container {
    display: flex;
    min-height: 100vh;
}

/* Sidebar */
.sidebar {
    width: 280px;
    background: var(--sidebar-bg);
    border-right: 1px solid var(--border-color);
    padding: 20px;
    position: fixed;
    height: 100vh;
    overflow-y: auto;
}

.sidebar h1 {
    font-size: 1.5em;
    margin-bottom: 20px;
    color: var(--primary-color);
    border-bottom: 2px solid var(--primary-color);
    padding-bottom: 10px;
}

.sidebar nav ul {
    list-style: none;
}

.sidebar nav ul li {
    margin: 5px 0;
}

.sidebar nav a {
    color: var(--text-color);
    text-decoration: none;
    display: block;
    padding: 8px 12px;
    border-radius: 4px;
    transition: background 0.2s;
}

.sidebar nav a:hover {
    background: var(--border-color);
}

.sidebar nav a.active {
    background: var(--primary-color);
    color: white;
}

/* Main content */
.main-content {
    margin-left: 280px;
    padding: 40px;
    max-width: 900px;
}

.main-content h1 {
    font-size: 2.5em;
    margin-bottom: 20px;
    color: var(--primary-color);
    border-bottom: 3px solid var(--primary-color);
    padding-bottom: 15px;
}

.main-content h2 {
    font-size: 2em;
    margin-top: 40px;
    margin-bottom: 20px;
    color: var(--secondary-color);
    border-bottom: 2px solid var(--border-color);
    padding-bottom: 10px;
}

.main-content h3 {
    font-size: 1.5em;
    margin-top: 30px;
    margin-bottom: 15px;
    color: var(--secondary-color);
}

/* Cards */
.conversation-card {
    background: white;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: box-shadow 0.2s;
}

.conversation-card:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.conversation-card h3 {
    margin-top: 0;
    color: var(--primary-color);
}

.conversation-card .meta {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin: 15px 0;
    font-size: 0.9em;
    color: #666;
}

.conversation-card .meta span {
    display: inline-flex;
    align-items: center;
    gap: 5px;
}

.conversation-card .tags {
    margin: 15px 0;
}

.conversation-card .tag {
    display: inline-block;
    background: var(--primary-color);
    color: white;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 0.85em;
    margin: 3px;
}

/* Messages */
.message {
    margin: 20px 0;
    padding: 15px;
    border-left: 4px solid var(--border-color);
    background: var(--sidebar-bg);
}

.message.human {
    border-left-color: var(--primary-color);
}

.message.assistant {
    border-left-color: var(--accent-color);
}

.message .role {
    font-weight: bold;
    margin-bottom: 10px;
    text-transform: uppercase;
    font-size: 0.85em;
    color: var(--secondary-color);
}

.message .content {
    white-space: pre-wrap;
    word-wrap: break-word;
}

/* Code blocks */
pre {
    background: var(--code-bg);
    border: 1px solid var(--border-color);
    border-radius: 4px;
    padding: 15px;
    overflow-x: auto;
    margin: 15px 0;
}

code {
    background: var(--code-bg);
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Monaco', 'Courier New', monospace;
    font-size: 0.9em;
}

pre code {
    background: none;
    padding: 0;
}

/* Stats */
.stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin: 30px 0;
}

.stat-card {
    background: var(--sidebar-bg);
    padding: 20px;
    border-radius: 8px;
    text-align: center;
}

.stat-card .number {
    font-size: 2.5em;
    font-weight: bold;
    color: var(--primary-color);
}

.stat-card .label {
    color: #666;
    margin-top: 5px;
}

/* Search */
.search-box {
    width: 100%;
    padding: 12px;
    border: 2px solid var(--border-color);
    border-radius: 4px;
    font-size: 1em;
    margin: 20px 0;
}

.search-box:focus {
    outline: none;
    border-color: var(--primary-color);
}

/* Responsive */
@media (max-width: 768px) {
    .sidebar {
        width: 100%;
        position: relative;
        height: auto;
    }

    .main-content {
        margin-left: 0;
        padding: 20px;
    }
}
"""

        with open(self.output_dir / 'static' / 'style.css', 'w') as f:
            f.write(css)

    def _generate_index(self):
        """Generate main index page."""
        html_content = self._get_base_html(
            title="Conversations Documentation",
            content=f"""
            <h1>📚 Conversations Documentation</h1>

            <div class="stats">
                <div class="stat-card">
                    <div class="number">{len(self.conversations)}</div>
                    <div class="label">Conversations</div>
                </div>
                <div class="stat-card">
                    <div class="number">{len(self.topics)}</div>
                    <div class="label">Topics</div>
                </div>
                <div class="stat-card">
                    <div class="number">{sum(len(msgs) for msgs in self.conversations)}</div>
                    <div class="label">Total Messages</div>
                </div>
            </div>

            <h2>📖 Browse by Topic</h2>
            <div class="conversation-card">
                <ul>
                    {''.join(f'<li><a href="topics/{topic.lower().replace(' ', '_')}.html">{topic.title()}</a> ({len(convs)} conversations)</li>' for topic, convs in sorted(self.topics.items()))}
                </ul>
            </div>

            <h2>🔍 Quick Search</h2>
            <div class="conversation-card">
                <p><a href="search.html">Search all conversations</a></p>
            </div>

            <h2>📋 Recent Conversations</h2>
            {self._generate_conversation_list(sorted(self.conversations, key=lambda x: x.get('date_range', {}).get('last') or datetime.min, reverse=True)[:10])}
            """
        )

        with open(self.output_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

    def _generate_topic_pages(self):
        """Generate pages for each topic."""
        for topic, conversations in self.topics.items():
            html_content = self._get_base_html(
                title=f"{topic.title()} Conversations",
                content=f"""
                <h1>📂 {topic.title()} Conversations</h1>
                <p>Found {len(conversations)} conversations about {topic}.</p>
                {self._generate_conversation_list(conversations)}
                """
            )

            topic_file = topic.lower().replace(' ', '_')
            with open(self.output_dir / 'topics' / f'{topic_file}.html', 'w', encoding='utf-8') as f:
                f.write(html_content)

    def _generate_conversation_pages(self):
        """Generate individual conversation pages."""
        for conv in self.conversations:
            messages_html = ''
            for msg in conv['messages']:
                role_class = msg['role'].lower()
                content = html.escape(msg['content'])
                timestamp = msg.get('timestamp', '')
                messages_html += f"""
                <div class="message {role_class}">
                    <div class="role">{msg['role']}</div>
                    {f'<div class="timestamp" style="font-size: 0.8em; color: #999; margin-bottom: 5px;">{timestamp}</div>' if timestamp else ''}
                    <div class="content">{self._format_content(content)}</div>
                </div>
                """

            tags_html = ''
            if conv['topics']:
                tags_html += '<div class="tags">'
                for topic in conv['topics']:
                    tags_html += f'<span class="tag"><a href="../topics/{topic.lower().replace(" ", "_")}.html" style="color: white; text-decoration: none;">{topic}</a></span>'
                tags_html += '</div>'

            html_content = self._get_base_html(
                title=conv['title'],
                content=f"""
                <h1>{conv['title']}</h1>

                <div class="meta">
                    <span>📅 {conv['date_range']['first'].strftime('%Y-%m-%d') if conv['date_range']['first'] else 'Unknown'}</span>
                    <span>💬 {conv['stats']['total_messages']} messages</span>
                    <span>👤 {conv['stats']['human_messages']} human</span>
                    <span>🤖 {conv['stats']['assistant_messages']} assistant</span>
                </div>

                {tags_html}

                <h2>Conversation</h2>
                {messages_html}
                """
            )

            conv_file = conv['filename'].replace('.csv', '.html')
            with open(self.output_dir / 'conversations' / conv_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

    def _generate_conversation_list(self, conversations: List[Dict]) -> str:
        """Generate HTML list of conversations."""
        html = ''
        for conv in conversations:
            date_str = conv['date_range']['last'].strftime('%Y-%m-%d') if conv['date_range'].get('last') else 'Unknown'
            conv_file = conv['filename'].replace('.csv', '.html')
            topics_str = ', '.join(conv['topics'][:3]) if conv['topics'] else 'General'

            html += f"""
            <div class="conversation-card">
                <h3><a href="conversations/{conv_file}">{conv['title']}</a></h3>
                <div class="meta">
                    <span>📅 {date_str}</span>
                    <span>💬 {conv['stats']['total_messages']} messages</span>
                </div>
                <div class="tags">
                    {''.join(f'<span class="tag">{t}</span>' for t in conv['topics'][:5])}
                </div>
            </div>
            """
        return html

    def _generate_search_page(self):
        """Generate search page."""
        # Create JSON data for client-side search
        search_data = []
        for conv in self.conversations:
            search_data.append({
                'title': conv['title'],
                'filename': conv['filename'],
                'topics': conv['topics'],
                'url': f"conversations/{conv['filename'].replace('.csv', '.html')}",
            })

        with open(self.output_dir / 'static' / 'search_data.json', 'w') as f:
            json.dump(search_data, f, indent=2)

        html_content = self._get_base_html(
            title="Search Conversations",
            content=f"""
            <h1>🔍 Search Conversations</h1>
            <input type="text" id="searchInput" class="search-box" placeholder="Search by title, topic, or keyword...">
            <div id="searchResults"></div>

            <script>
                const searchData = {json.dumps(search_data)};
                const searchInput = document.getElementById('searchInput');
                const searchResults = document.getElementById('searchResults');

                searchInput.addEventListener('input', function(e) {{
                    const query = e.target.value.toLowerCase();
                    if (query.length < 2) {{
                        searchResults.innerHTML = '';
                        return;
                    }}

                    const results = searchData.filter(item => {{
                        return item.title.toLowerCase().includes(query) ||
                               item.topics.some(t => t.toLowerCase().includes(query));
                    }});

                    if (results.length === 0) {{
                        searchResults.innerHTML = '<p>No results found.</p>';
                        return;
                    }}

                    let html = '<h2>Results (' + results.length + ')</h2>';
                    results.forEach(item => {{
                        html += `
                            <div class="conversation-card">
                                <h3><a href="${{item.url}}">${{item.title}}</a></h3>
                                <div class="tags">
                                    ${{item.topics.map(t => `<span class="tag">${{t}}</span>`).join('')}}
                                </div>
                            </div>
                        `;
                    }});
                    searchResults.innerHTML = html;
                }});
            </script>
            """
        )

        with open(self.output_dir / 'search.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

    def _generate_sitemap(self):
        """Generate sitemap."""
        sitemap = {
            'index': 'index.html',
            'search': 'search.html',
            'topics': {topic: f'topics/{topic.lower().replace(" ", "_")}.html' for topic in self.topics.keys()},
            'conversations': {conv['title']: f"conversations/{conv['filename'].replace('.csv', '.html')}" for conv in self.conversations},
        }

        with open(self.output_dir / 'sitemap.json', 'w') as f:
            json.dump(sitemap, f, indent=2)

    def _format_content(self, content: str) -> str:
        """Format content with markdown-like syntax."""
        # Convert code blocks
        content = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code>\2</code></pre>', content, flags=re.DOTALL)
        # Convert inline code
        content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)
        # Convert links
        content = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', content)
        # Convert bold
        content = re.sub(r'\*\*([^\*]+)\*\*', r'<strong>\1</strong>', content)
        # Convert italic
        content = re.sub(r'\*([^\*]+)\*', r'<em>\1</em>', content)
        # Convert line breaks
        content = content.replace('\n', '<br>')
        return content

    def _get_base_html(self, title: str, content: str) -> str:
        """Generate base HTML template."""
        nav_items = [
            ('index.html', 'Home'),
            ('search.html', 'Search'),
        ]

        # Add topic links
        for topic in sorted(self.topics.keys())[:10]:
            nav_items.append((f'topics/{topic.lower().replace(" ", "_")}.html', topic.title()))

        nav_html = '\n'.join(f'<li><a href="{url}">{label}</a></li>' for url, label in nav_items)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Conversations Docs</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <div class="container">
        <aside class="sidebar">
            <h1>📚 Docs</h1>
            <nav>
                <ul>
                    {nav_html}
                </ul>
            </nav>
        </aside>
        <main class="main-content">
            {content}
        </main>
    </div>
</body>
</html>"""


def main():
    """Main function."""
    import sys

    conversations_dir = sys.argv[1] if len(sys.argv) > 1 else '/Users/steven/claude/conversations'
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    generator = ConversationDocGenerator(conversations_dir, output_dir)
    generator.load_conversations()
    generator.generate_docs()

    print(f"\n🎉 Documentation generation complete!")
    print(f"   Open {generator.output_dir / 'index.html'} in your browser")


if __name__ == '__main__':
    main()

