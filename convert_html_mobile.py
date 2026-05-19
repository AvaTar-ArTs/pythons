#!/usr/bin/env python3
"""
Script to convert existing HTML files to mobile-ready versions
"""

import os
from pathlib import Path

from bs4 import BeautifulSoup


def load_templates():
    """Load the mobile-responsive templates we created"""
    templates = {}

    # General website template
    with open(
        "/Users/steven/Music/nocTurneMeLoDieS/mobile_responsive_template.html",
        encoding="utf-8",
    ) as f:
        templates["general"] = f.read()

    # Album/track template
    with open(
        "/Users/steven/Music/nocTurneMeLoDieS/mobile_album_template.html",
        encoding="utf-8",
    ) as f:
        templates["album"] = f.read()

    # Chat interface template
    with open(
        "/Users/steven/Music/nocTurneMeLoDieS/mobile_chat_template.html",
        encoding="utf-8",
    ) as f:
        templates["chat"] = f.read()

    return templates


def detect_template_type(html_content):
    """Detect which template type to use based on content"""
    soup = BeautifulSoup(html_content, "html.parser")

    # Check for album-specific elements
    if soup.find("audio") and ("lyrics" in html_content.lower() or "analysis" in html_content.lower()):
        return "album"

    # Check for chat/conversation elements
    if "conversation" in html_content.lower() or "message" in html_content.lower():
        return "chat"

    # Default to general template
    return "general"


def extract_content_elements(soup):
    """Extract main content elements from the original HTML"""
    content_data = {
        "title": "",
        "headings": [],
        "paragraphs": [],
        "links": [],
        "images": [],
        "audio": [],
        "code_blocks": [],
        "lists": [],
    }

    # Extract title
    title_tag = soup.find("title")
    if title_tag:
        content_data["title"] = title_tag.get_text().strip()

    # Extract headings
    for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        content_data["headings"].append(
            {
                "level": heading.name,
                "text": heading.get_text().strip(),
                "original": str(heading),
            }
        )

    # Extract paragraphs
    for p in soup.find_all("p"):
        content_data["paragraphs"].append(p.get_text().strip())

    # Extract links
    for a in soup.find_all("a", href=True):
        content_data["links"].append({"text": a.get_text().strip(), "href": a["href"]})

    # Extract images
    for img in soup.find_all("img"):
        content_data["images"].append({"src": img.get("src", ""), "alt": img.get("alt", "")})

    # Extract audio elements
    for audio in soup.find_all("audio"):
        sources = [source.get("src") for source in audio.find_all("source") if source.get("src")]
        content_data["audio"].append({"sources": sources, "controls": "controls" in audio.attrs})

    # Extract code blocks
    for code_block in soup.find_all(["code", "pre"]):
        content_data["code_blocks"].append(code_block.get_text().strip())

    # Extract lists
    for ul in soup.find_all(["ul", "ol"]):
        items = [li.get_text().strip() for li in ul.find_all("li")]
        content_data["lists"].append(items)

    return content_data


def create_mobile_version(original_html, template_type, templates):
    """Create a mobile-optimized version of the HTML"""
    soup = BeautifulSoup(original_html, "html.parser")
    content_data = extract_content_elements(soup)

    # Select appropriate template
    template_html = templates[template_type]
    template_soup = BeautifulSoup(template_html, "html.parser")

    # Update title
    if content_data["title"]:
        title_tag = template_soup.find("title")
        if title_tag:
            title_tag.string = content_data["title"]

    # Update logo/header
    logo_elem = template_soup.find(class_="logo")
    if logo_elem and content_data["title"]:
        # Use first part of title as logo
        logo_elem.string = content_data["title"].split(" - ")[0][:50]  # Limit length

    # Insert main content based on template type
    if template_type == "album":
        # Find album container and populate with content
        album_div = template_soup.find(class_="album")
        if album_div and content_data["title"]:
            # Update album title
            h3 = album_div.find("h3")
            if h3:
                h3.string = content_data["title"]

            # Add audio if available
            if content_data["audio"]:
                audio_elem = album_div.find("audio")
                if audio_elem:
                    # Clear existing sources
                    for source in audio_elem.find_all("source"):
                        source.decompose()

                    # Add new sources
                    for audio_info in content_data["audio"]:
                        for src in audio_info["sources"]:
                            new_source = template_soup.new_tag("source")
                            new_source["src"] = src
                            new_source["type"] = "audio/mpeg"
                            audio_elem.append(new_source)

            # Add content to lyrics section if we have paragraphs
            lyrics_div = album_div.find(class_="lyrics")
            if lyrics_div and content_data["paragraphs"]:
                pre = template_soup.new_tag("pre")
                pre.string = "\\n".join(content_data["paragraphs"][:10])  # Limit to first 10 paragraphs
                lyrics_div.clear()
                lyrics_div.append(pre)

    elif template_type == "chat":
        # Find conversation container and populate with content
        conv_container = template_soup.find(class_="conversation")

        if conv_container:
            # Add conversation items based on headings and paragraphs
            for i, heading in enumerate(content_data["headings"][:3]):  # Use first 3 headings
                conv_item = template_soup.new_tag("div", **{"class": "conversation-item"})

                author_div = template_soup.new_tag("div", **{"class": "author"})
                author_div.string = "A" if i % 2 == 0 else "U"  # Alternate author

                msg_content = template_soup.new_tag("div", **{"class": "message-content"})

                # Add heading as paragraph
                p_heading = template_soup.new_tag("p")
                p_heading.string = f"{heading['text']}"
                msg_content.append(p_heading)

                # Add related paragraphs if available
                if i < len(content_data["paragraphs"]):
                    p_content = template_soup.new_tag("p")
                    p_content.string = content_data["paragraphs"][i]
                    msg_content.append(p_content)

                conv_item.append(author_div)
                conv_item.append(msg_content)
                conv_container.append(conv_item)

    else:  # general template
        # Find main content area and populate with extracted content
        main_content = template_soup.find(class_="main-content")
        if main_content:
            container = template_soup.find(class_="container")
            if container:
                article = template_soup.new_tag("article", **{"class": "card"})

                header = template_soup.new_tag("div", **{"class": "card-header"})
                h1 = template_soup.new_tag("h1", **{"class": "card-title"})
                h1.string = content_data["title"] or "Converted Content"
                header.append(h1)

                body = template_soup.new_tag("div", **{"class": "card-body"})

                # Add headings and paragraphs
                for heading in content_data["headings"][:3]:  # First 3 headings
                    h = template_soup.new_tag(heading["level"])
                    h.string = heading["text"]
                    body.append(h)

                for paragraph in content_data["paragraphs"][:5]:  # First 5 paragraphs
                    p = template_soup.new_tag("p")
                    p.string = paragraph
                    body.append(p)

                # Add links if available
                if content_data["links"]:
                    ul = template_soup.new_tag("ul")
                    for link in content_data["links"][:5]:  # First 5 links
                        li = template_soup.new_tag("li")
                        a = template_soup.new_tag("a", href=link["href"])
                        a.string = link["text"]
                        li.append(a)
                        ul.append(li)
                    body.append(ul)

                article.append(header)
                article.append(body)
                container.append(article)

    return str(template_soup.prettify())


def process_html_files(base_dir):
    """Process all HTML files in the directory structure"""
    templates = load_templates()

    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith(".html"):
                html_files.append(os.path.join(root, file))

    print(f"Found {len(html_files)} HTML files to process")

    # Process each file
    converted_count = 0
    for html_file in html_files:
        try:
            # Read original file
            with open(html_file, encoding="utf-8", errors="ignore") as f:
                original_content = f.read()

            # Skip if it's one of our template files
            if (
                "mobile_responsive_template" in html_file
                or "mobile_album_template" in html_file
                or "mobile_chat_template" in html_file
            ):
                continue

            # Detect template type
            template_type = detect_template_type(original_content)

            # Create mobile version
            mobile_content = create_mobile_version(original_content, template_type, templates)

            # Create new filename with _mobile suffix
            path_obj = Path(html_file)
            new_filename = path_obj.stem + "_mobile" + path_obj.suffix
            new_filepath = path_obj.parent / new_filename

            # Write mobile version
            with open(new_filepath, "w", encoding="utf-8") as f:
                f.write(mobile_content)

            print(f"Created mobile version: {new_filepath}")
            converted_count += 1

        except Exception as e:
            print(f"Error processing {html_file}: {str(e)}")

    print(f"\\nConversion complete! Converted {converted_count} files.")


if __name__ == "__main__":
    # Specify the base directory to process
    base_directory = "/Users/steven/Music/nocTurneMeLoDieS"
    process_html_files(base_directory)
