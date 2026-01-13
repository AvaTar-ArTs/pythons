#!/usr/bin/env python3
import os, re, sys
from pathlib import Path

HEADER = (Path(__file__).parent / 'templates' / 'header.html').read_text()
FOOTER = (Path(__file__).parent / 'templates' / 'footer.html').read_text()

H1 = re.compile(r'^#\s+(.+)$')
H2 = re.compile(r'^##\s+(.+)$')
H3 = re.compile(r'^###\s+(.+)$')
IMG = re.compile(r'!\[(.*?)\]\((.*?)\)')
LINK = re.compile(r'\[(.*?)\]\((.*?)\)')
OLI = re.compile(r'^\s*\d+\.\s+(.*)')
ULI = re.compile(r'^\s*[-\*]\s+(.*)')
CODE_FENCE = re.compile(r'^```')

def md_to_html(md: str) -> str:
    html_lines = []
    in_code = False
    list_open = None

    def close_list():
        nonlocal list_open
        if list_open:
            html_lines.append(f'</{list_open}>')
            list_open = None

    for raw in md.splitlines():
        line = raw.rstrip('\n')
        if CODE_FENCE.match(line):
            if not in_code:
                close_list()
                html_lines.append('<pre><code>')
                in_code = True
            else:
                html_lines.append('</code></pre>')
                in_code = False
            continue
        if in_code:
            html_lines.append(line)
            continue
        if H1.match(line):
            close_list()
            html_lines.append(f'<h1>{H1.sub(r"\\1", line)}</h1>')
            continue
        if H2.match(line):
            close_list()
            html_lines.append(f'<h2>{H2.sub(r"\\1", line)}</h2>')
            continue
        if H3.match(line):
            close_list()
            html_lines.append(f'<h3>{H3.sub(r"\\1", line)}</h3>')
            continue
        if OLI.match(line):
            if list_open != 'ol':
                close_list()
                list_open = 'ol'
                html_lines.append('<ol>')
            html_lines.append(f'<li>{OLI.sub(r"\\1", line)}</li>')
            continue
        if ULI.match(line):
            if list_open != 'ul':
                close_list()
                list_open = 'ul'
                html_lines.append('<ul>')
            html_lines.append(f'<li>{ULI.sub(r"\\1", line)}</li>')
            continue
        if line.strip() == '---':
            close_list()
            html_lines.append('<hr />')
            continue
        if line.strip() == '':
            close_list()
            html_lines.append('')
            continue
        s = IMG.sub(r'<img alt="\1" src="\2" />', line)
        s = LINK.sub(r'<a href="\2">\1</a>', s)
        html_lines.append(f'<p>{s}</p>')
    close_list()
    return '\n'.join(html_lines)


def main():
    if len(sys.argv) < 2:
        print('Usage: export_md.py path/to/file.md [--title "Title"]')
        sys.exit(1)
    md_path = Path(sys.argv[1]).expanduser().resolve()
    title = None
    if '--title' in sys.argv:
        i = sys.argv.index('--title')
        if i + 1 < len(sys.argv):
            title = sys.argv[i+1]
    if not title:
        title = md_path.stem.replace('-', ' ').title()
    md = md_path.read_text(encoding='utf-8')
    body = md_to_html(md)
    out_html = HEADER.replace('{{TITLE}}', title) + body + FOOTER
    html_path = md_path.with_suffix('.html')
    html_path.write_text(out_html, encoding='utf-8')
    print(f'✅ Exported HTML → {html_path}')

if __name__ == '__main__':
    main()
