#!/usr/bin/env python3
"""
Script to create mobile-optimized versions of HTML files
Based on the same techniques used in the nocTurneMeLoDieS project
"""

from pathlib import Path

from bs4 import BeautifulSoup


def create_mobile_version(html_content, file_path):
    """Create a mobile-optimized version of an HTML file"""
    try:
        soup = BeautifulSoup(html_content, "html.parser")

        # Create a new soup object for the mobile version
        mobile_soup = BeautifulSoup(features="html.parser")

        # Create the basic HTML structure
        html_tag = mobile_soup.new_tag("html", lang="en")
        mobile_soup.insert(0, html_tag)

        head_tag = mobile_soup.new_tag("head")
        html_tag.insert(0, head_tag)

        # Add meta tags for mobile responsiveness
        meta_charset = mobile_soup.new_tag("meta", charset="utf-8")
        head_tag.insert(0, meta_charset)

        meta_viewport = mobile_soup.new_tag(
            "meta",
            attrs={
                "name": "viewport",
                "content": "width=device-width, initial-scale=1.0",
            },
        )
        head_tag.insert(1, meta_viewport)

        # Copy title from original if it exists
        original_title = soup.find("title")
        if original_title:
            title_tag = mobile_soup.new_tag("title")
            title_tag.string = original_title.get_text()
            head_tag.insert(2, title_tag)
        else:
            title_tag = mobile_soup.new_tag("title")
            title_tag.string = f"Mobile: {Path(file_path).name}"
            head_tag.insert(2, title_tag)

        # Add mobile-friendly CSS
        css_content = """
        /* Reset and Base Styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
            padding: 0;
            margin: 0;
        }

        /* Container */
        .container {
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 15px;
        }

        /* Header Styles */
        header {
            background-color: #2c3e50;
            color: white;
            padding: 1rem;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 1.5rem;
            font-weight: bold;
        }

        /* Navigation Styles */
        nav {
            background-color: #34495e;
        }

        .nav-menu {
            display: flex;
            list-style: none;
            justify-content: center;
        }

        .nav-item {
            margin: 0 1rem;
        }

        .nav-link {
            color: white;
            text-decoration: none;
            padding: 0.75rem 1rem;
            display: block;
            transition: background-color 0.3s ease;
        }

        .nav-link:hover {
            background-color: #2c3e50;
            border-radius: 4px;
        }

        /* Mobile Navigation Toggle */
        .nav-toggle {
            display: none;
            background: none;
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
        }

        /* Main Content */
        main {
            padding: 1.5rem 0;
        }

        /* Card Styles */
        .card {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 1.5rem;
            overflow: hidden;
        }

        .card-header {
            padding: 1rem 1.5rem;
            background-color: #f8f9fa;
            border-bottom: 1px solid #eee;
        }

        .card-body {
            padding: 1.5rem;
        }

        .card-title {
            margin: 0 0 0.75rem;
            font-size: 1.25rem;
            color: #2c3e50;
        }

        /* Media Elements */
        audio, video {
            width: 100%;
            margin: 1rem 0;
        }

        /* Button Styles */
        .btn {
            display: inline-block;
            padding: 0.5rem 1rem;
            background-color: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            border: none;
            cursor: pointer;
            font-size: 1rem;
            transition: background-color 0.3s ease;
        }

        .btn:hover {
            background-color: #2980b9;
        }

        .btn-secondary {
            background-color: #95a5a6;
        }

        .btn-secondary:hover {
            background-color: #7f8c8d;
        }

        /* Utility Classes */
        .text-center {
            text-align: center;
        }

        .margin-bottom {
            margin-bottom: 1rem;
        }

        .hidden {
            display: none;
        }

        /* Footer Styles */
        footer {
            background-color: #2c3e50;
            color: white;
            text-align: center;
            padding: 1.5rem;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                text-align: center;
            }

            .nav-menu {
                flex-direction: column;
                display: none;
            }

            .nav-item {
                margin: 0.25rem 0;
            }

            .nav-toggle {
                display: block;
                position: absolute;
                top: 1rem;
                right: 1rem;
            }

            .container {
                padding: 0 10px;
            }

            .card-body {
                padding: 1rem;
            }
        }

        @media (max-width: 480px) {
            .header-content {
                padding: 0.5rem;
            }

            .card {
                margin-bottom: 1rem;
            }

            .card-body {
                padding: 0.75rem;
            }
        }

        /* Dark Mode Support */
        @media (prefers-color-scheme: dark) {
            body {
                background-color: #1a1a1a;
                color: #e0e0e0;
            }

            .card {
                background-color: #1e1e1e;
                color: #e0e0e0;
            }

            .card-header {
                background-color: #2a2a2a;
                border-bottom: 1px solid #444;
            }
        }
        """

        style_tag = mobile_soup.new_tag("style")
        style_tag.string = css_content
        head_tag.append(style_tag)

        # Create body tag
        body_tag = mobile_soup.new_tag("body")
        html_tag.append(body_tag)

        # Add mobile-friendly header
        header_tag = mobile_soup.new_tag("header")
        body_tag.append(header_tag)

        container_header = mobile_soup.new_tag("div", **{"class": "container"})
        header_tag.append(container_header)

        header_content = mobile_soup.new_tag("div", **{"class": "header-content"})
        container_header.append(header_content)

        logo = mobile_soup.new_tag("div", **{"class": "logo"})
        logo.string = "Mobile Version"
        header_content.append(logo)

        nav_toggle = mobile_soup.new_tag("button", **{"class": "nav-toggle", "id": "navToggle"})
        nav_toggle.string = "☰"
        header_content.append(nav_toggle)

        # Add navigation
        nav_tag = mobile_soup.new_tag("nav", **{"id": "mainNav"})
        body_tag.append(nav_tag)

        container_nav = mobile_soup.new_tag("div", **{"class": "container"})
        nav_tag.append(container_nav)

        nav_menu = mobile_soup.new_tag("ul", **{"class": "nav-menu"})
        container_nav.append(nav_menu)

        nav_items = [
            {"text": "Home", "href": "#"},
            {"text": "Music", "href": "#"},
            {"text": "Lyrics", "href": "#"},
            {"text": "Analysis", "href": "#"},
            {"text": "Docs", "href": "#"},
        ]

        for item in nav_items:
            nav_item = mobile_soup.new_tag("li", **{"class": "nav-item"})
            nav_link = mobile_soup.new_tag("a", **{"class": "nav-link", "href": item["href"]})
            nav_link.string = item["text"]
            nav_item.append(nav_link)
            nav_menu.append(nav_item)

        # Add main content
        main_tag = mobile_soup.new_tag("main")
        body_tag.append(main_tag)

        container_main = mobile_soup.new_tag("div", **{"class": "container"})
        main_tag.append(container_main)

        # Create a card for the content
        card = mobile_soup.new_tag("article", **{"class": "card"})
        container_main.append(card)

        card_header = mobile_soup.new_tag("div", **{"class": "card-header"})
        card.append(card_header)

        card_title = mobile_soup.new_tag("h1", **{"class": "card-title"})
        if original_title:
            card_title.string = original_title.get_text()
        else:
            card_title.string = f"Mobile Version: {Path(file_path).name}"
        card_header.append(card_title)

        card_body = mobile_soup.new_tag("div", **{"class": "card-body"})
        card.append(card_body)

        # Add the original content to the card body
        # Try to extract main content from original HTML
        main_content = soup.find("main") or soup.find("body")
        if main_content:
            # Clone the content to avoid modifying the original
            content_clone = BeautifulSoup(str(main_content), "html.parser")
            card_body.extend(content_clone.contents)
        else:
            # If no main content found, add the entire body
            body_content = soup.find("body")
            if body_content:
                content_clone = BeautifulSoup(str(body_content), "html.parser")
                card_body.extend(content_clone.contents)
            else:
                # If no body, add the whole HTML body content
                for tag in soup.find_all():
                    if tag.name not in [
                        "html",
                        "head",
                        "title",
                        "meta",
                        "link",
                        "script",
                    ]:
                        content_clone = BeautifulSoup(str(tag), "html.parser")
                        card_body.extend(content_clone.contents)
                        break

        # Add footer
        footer_tag = mobile_soup.new_tag("footer")
        body_tag.append(footer_tag)

        container_footer = mobile_soup.new_tag("div", **{"class": "container"})
        footer_tag.append(container_footer)

        footer_text = mobile_soup.new_tag("p")
        footer_text.string = f"© 2026 Mobile-Optimized Version. Original file: {Path(file_path).name}"
        container_footer.append(footer_text)

        # Add mobile navigation script
        script_content = """
        // Mobile navigation toggle
        document.addEventListener('DOMContentLoaded', function() {
            const navToggle = document.getElementById('navToggle');
            const navMenu = document.querySelector('.nav-menu');

            if (navToggle && navMenu) {
                navToggle.addEventListener('click', function() {
                    navMenu.classList.toggle('hidden');
                });
            }

            // Close mobile menu when clicking a link
            const navLinks = document.querySelectorAll('.nav-link');
            navLinks.forEach(link => {
                link.addEventListener('click', () => {
                    if (window.innerWidth <= 768) {
                        navMenu.classList.add('hidden');
                    }
                });
            });
        });
        """

        script_tag = mobile_soup.new_tag("script")
        script_tag.string = script_content
        body_tag.append(script_tag)

        return str(mobile_soup.prettify())
    except Exception as e:
        print(f"Error creating mobile version of {file_path}: {str(e)}")
        # Return original content if processing fails
        return html_content


def process_html_files():
    """Process all HTML files in the consolidated web directory"""
    html_dir = Path("/Users/steven/Music/nocTurneMeLoDieS/CONSOLIDATED_CONTENT/web/html/")
    mobile_dir = Path("/Users/steven/Music/nocTurneMeLoDieS/CONSOLIDATED_CONTENT/web/mobile-optimized/")

    # Create mobile-optimized directory if it doesn't exist
    mobile_dir.mkdir(parents=True, exist_ok=True)

    html_files = list(html_dir.glob("*.html"))
    print(f"Found {len(html_files)} HTML files to process")

    for i, html_file in enumerate(html_files):
        try:
            # Read the original HTML file
            with open(html_file, encoding="utf-8", errors="ignore") as f:
                original_content = f.read()

            # Create mobile-optimized version
            mobile_content = create_mobile_version(original_content, html_file)

            # Write mobile-optimized version
            mobile_file_path = mobile_dir / f"mobile_{html_file.name}"
            with open(mobile_file_path, "w", encoding="utf-8") as f:
                f.write(mobile_content)

            print(f"Processed ({i + 1}/{len(html_files)}): {html_file.name}")
        except Exception as e:
            print(f"Error processing {html_file.name}: {str(e)}")

    print(f"Mobile optimization completed! Files created in {mobile_dir}")


if __name__ == "__main__":
    process_html_files()
