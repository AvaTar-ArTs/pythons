#!/usr/bin/env python3
"""
Python API Documentation Generator
Automated API documentation system for discovered endpoints
"""

import os
import re
import json
import ast
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class APIDocumentationGenerator:
    """Generates comprehensive API documentation for discovered endpoints."""

    def __init__(self):
        """__init__ function."""

        self.root_path = Path(Path(str(Path.home()) + "/Documents/python")).expanduser()
        self.api_endpoints = []
        self.documentation = {}

    def discover_and_document_apis(self):
        """Discover all API endpoints and generate comprehensive documentation."""
        logger.info("🔌 DISCOVERING AND DOCUMENTING API ENDPOINTS")
        logger.info("=" * 80)

        # Discover API files
        api_files = self._discover_api_files()

        # Extract endpoints from each file
        for api_file in api_files:
            endpoints = self._extract_endpoints_from_file(api_file)
            self.api_endpoints.extend(endpoints)

        logger.info(f"   Found {len(api_files)} API files")
        logger.info(f"   Discovered {len(self.api_endpoints)} API endpoints")

        # Generate documentation for each endpoint
        for endpoint in self.api_endpoints:
            doc = self._generate_endpoint_documentation(endpoint)
            self.documentation[endpoint["path"]] = doc

        # Generate comprehensive API documentation
        self._generate_comprehensive_documentation()

        return self.api_endpoints, self.documentation

    def _discover_api_files(self):
        """Discover all API-related Python files."""
        api_files = []

        for file_path in self.root_path.rglob("*.py"):
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                content_lower = content.lower()

                # Check for API patterns
                if any(
                    term in content_lower
                    for term in [
                        "api",
                        "endpoint",
                        "route",
                        "flask",
                        "fastapi",
                        "django",
                        "app",
                    ]
                ):
                    api_files.append(
                        {
                            "path": str(file_path),
                            "name": file_path.name,
                            "content": content,
                        }
                    )

            except (IOError, OSError, UnicodeDecodeError):
                continue

        return api_files

    def _extract_endpoints_from_file(self, api_file):
        """Extract API endpoints from a file."""
        content = api_file["content"]
        endpoints = []

        # Flask patterns
        flask_routes = re.findall(r'@app\.route\(["\']([^"\']+)["\']', content)
        for route in flask_routes:
            endpoints.append(
                {
                    "path": route,
                    "method": "GET",  # Default
                    "framework": "Flask",
                    "file": api_file["path"],
                    "file_name": api_file["name"],
                }
            )

        # FastAPI patterns
        fastapi_routes = re.findall(
            r'@app\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']', content
        )
        for method, route in fastapi_routes:
            endpoints.append(
                {
                    "path": route,
                    "method": method.upper(),
                    "framework": "FastAPI",
                    "file": api_file["path"],
                    "file_name": api_file["name"],
                }
            )

        # Django patterns
        django_urls = re.findall(r'path\(["\']([^"\']+)["\']', content)
        for url in django_urls:
            endpoints.append(
                {
                    "path": url,
                    "method": "GET",  # Default
                    "framework": "Django",
                    "file": api_file["path"],
                    "file_name": api_file["name"],
                }
            )

        return endpoints

    def _generate_endpoint_documentation(self, endpoint):
        """Generate comprehensive documentation for an endpoint."""
        doc = {
            "path": endpoint["path"],
            "method": endpoint["method"],
            "framework": endpoint["framework"],
            "file": endpoint["file"],
            "file_name": endpoint["file_name"],
            "description": self._generate_description(endpoint),
            "parameters": self._extract_parameters(endpoint),
            "response": self._extract_response_info(endpoint),
            "examples": self._generate_examples(endpoint),
            "status_codes": self._extract_status_codes(endpoint),
        }

        return doc

    def _generate_description(self, endpoint):
        """Generate a description for the endpoint."""
        # Try to extract docstring or comments
        try:
            with open(endpoint["file"], "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Look for function docstrings
            pattern = rf'def\s+\w+.*?:\s*"""(.*?)"""'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                return match.group(1).strip()

            # Look for comments near the route
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if endpoint["path"] in line:
                    # Look for comments above the route
                    for j in range(max(0, i - 5), i):
                        if lines[j].strip().startswith("#"):
                            return lines[j].strip("#").strip()
                    break

        except (IOError, OSError, UnicodeDecodeError):
            pass

        # Default description
        return f"{endpoint['method']} endpoint at {endpoint['path']}"

    def _extract_parameters(self, endpoint):
        """Extract parameters from the endpoint."""
        parameters = []

        try:
            with open(endpoint["file"], "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Look for parameter patterns
            param_patterns = [
                r'request\.args\.get\(["\'](\w+)["\']',
                r'request\.form\[["\'](\w+)["\']',
                r'request\.json\[["\'](\w+)["\']',
                r'@app\.route\(["\'][^"\']*<(\w+)>[^"\']*["\']',
                r"def\s+\w+\([^)]*(\w+)[^)]*\):",
            ]

            for pattern in param_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    parameters.append(
                        {
                            "name": match,
                            "type": "string",  # Default
                            "required": True,
                            "description": f"Parameter: {match}",
                        }
                    )

        except (IOError, OSError, UnicodeDecodeError):
            pass

        return parameters

    def _extract_response_info(self, endpoint):
        """Extract response information from the endpoint."""
        response = {"type": "json", "description": "Response data", "schema": {}}

        try:
            with open(endpoint["file"], "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Look for return patterns
            if "return jsonify" in content.lower():
                response["type"] = "json"
            elif "return render_template" in content.lower():
                response["type"] = "html"
            elif "return" in content.lower():
                response["type"] = "text"

        except (IOError, OSError, UnicodeDecodeError):
            pass

        return response

    def _generate_examples(self, endpoint):
        """Generate usage examples for the endpoint."""
        examples = []

        # Generate curl example
        curl_example = f"curl -X {endpoint['method']} http://localhost:CONSTANT_5000{endpoint['path']}"
        examples.append(
            {"type": "curl", "description": "cURL example", "code": curl_example}
        )

        # Generate Python example
        python_example = f"""import requests

response = requests.{endpoint['method'].lower()}('http://localhost:CONSTANT_5000{endpoint['path']}')
logger.info(response.json())"""
        examples.append(
            {"type": "python", "description": "Python example", "code": python_example}
        )

        return examples

    def _extract_status_codes(self, endpoint):
        """Extract possible status codes from the endpoint."""
        status_codes = [
            {"code": CONSTANT_200, "description": "Success"},
            {"code": CONSTANT_400, "description": "Bad Request"},
            {"code": CONSTANT_404, "description": "Not Found"},
            {"code": CONSTANT_500, "description": "Internal Server Error"},
        ]

        return status_codes

    def _generate_comprehensive_documentation(self):
        """Generate comprehensive API documentation."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Generate OpenAPI/Swagger documentation
        openapi_doc = self._generate_openapi_documentation()

        # Save OpenAPI documentation
        openapi_file = fstr(Path.home()) + "/python_api_openapi_{timestamp}.json"
        with open(openapi_file, "w") as f:
            json.dump(openapi_doc, f, indent=2)

        # Generate HTML documentation
        html_doc = self._generate_html_documentation()

        # Save HTML documentation
        html_file = fstr(Path.home()) + "/python_api_documentation_{timestamp}.html"
        with open(html_file, "w") as f:
            f.write(html_doc)

        # Generate Markdown documentation
        markdown_doc = self._generate_markdown_documentation()

        # Save Markdown documentation
        markdown_file = fstr(Path.home()) + "/python_api_documentation_{timestamp}.md"
        with open(markdown_file, "w") as f:
            f.write(markdown_doc)

        logger.info(f"   OpenAPI documentation: {openapi_file}")
        logger.info(f"   HTML documentation: {html_file}")
        logger.info(f"   Markdown documentation: {markdown_file}")

    def _generate_openapi_documentation(self):
        """Generate OpenAPI/Swagger documentation."""
        openapi_doc = {
            "openapi": "3.0.0",
            "info": {
                "title": "Python Ecosystem API",
                "description": "Automated API documentation for discovered endpoints",
                "version": "1.0.0",
                "contact": {"name": "Python Ecosystem", "email": "steven@example.com"},
            },
            "servers": [
                {"url": "http://localhost:5000", "description": "Development server"}
            ],
            "paths": {},
        }

        for endpoint in self.api_endpoints:
            path = endpoint["path"]
            method = endpoint["method"].lower()

            if path not in openapi_doc["paths"]:
                openapi_doc["paths"][path] = {}

            openapi_doc["paths"][path][method] = {
                "summary": f"{endpoint['method']} {path}",
                "description": self.documentation[path]["description"],
                "parameters": self.documentation[path]["parameters"],
                "responses": {
                    "200": {
                        "description": "Success",
                        "content": {"application/json": {"schema": {"type": "object"}}},
                    }
                },
            }

        return openapi_doc

    def _generate_html_documentation(self):
        """Generate HTML documentation."""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Ecosystem API Documentation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .endpoint {{ border: 1px solid #ddd; margin: 20px 0; padding: 20px; border-radius: 5px; }}
        .method {{ background: #007bff; color: white; padding: 5px 10px; border-radius: 3px; display: inline-block; }}
        .path {{ font-family: monospace; font-size: 18px; margin: 10px 0; }}
        .description {{ margin: 10px 0; }}
        .parameters {{ margin: 10px 0; }}
        .examples {{ margin: 10px 0; }}
        code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>Python Ecosystem API Documentation</h1>
    <p>Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    <p>Total endpoints: {len(self.api_endpoints)}</p>
    
    <h2>Endpoints</h2>
"""

        for endpoint in self.api_endpoints:
            doc = self.documentation[endpoint["path"]]
            html += f"""
    <div class="endpoint">
        <div class="method">{endpoint['method']}</div>
        <div class="path">{endpoint['path']}</div>
        <div class="description">{doc['description']}</div>
        
        <h3>Parameters</h3>
        <div class="parameters">
"""

            for param in doc["parameters"]:
                html += f"            <p><strong>{param['name']}</strong> ({param['type']}) - {param['description']}</p>\n"

            html += "        </div>"

            html += f"""
        <h3>Examples</h3>
        <div class="examples">
"""

            for example in doc["examples"]:
                html += f"""
            <h4>{example['description']}</h4>
            <pre><code>{example['code']}</code></pre>
"""

            html += "        </div>"
            html += "    </div>"

        html += """
</body>
</html>"""

        return html

    def _generate_markdown_documentation(self):
        """Generate Markdown documentation."""
        markdown = f"""# Python Ecosystem API Documentation

Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Total endpoints: {len(self.api_endpoints)}

## Endpoints

"""

        for endpoint in self.api_endpoints:
            doc = self.documentation[endpoint["path"]]
            markdown += f"""### {endpoint['method']} {endpoint['path']}

**Description:** {doc['description']}

**Framework:** {endpoint['framework']}

**File:** {endpoint['file_name']}

#### Parameters

"""

            for param in doc["parameters"]:
                markdown += f"- **{param['name']}** ({param['type']}) - {param['description']}\n"

            markdown += "\n#### Examples\n\n"

            for example in doc["examples"]:
                markdown += f"**{example['description']}:**\n\n```{example['type']}\n{example['code']}\n```\n\n"

            markdown += "---\n\n"

        return markdown


def main():
    """Main execution function."""
    logger.info("🔌 PYTHON API DOCUMENTATION GENERATOR")
    logger.info("=" * 80)
    logger.info("Automated API documentation system for discovered endpoints")
    print()

    generator = APIDocumentationGenerator()

    # Discover and document APIs
    endpoints, documentation = generator.discover_and_document_apis()

    logger.info(f"\n✅ API DOCUMENTATION GENERATION COMPLETE!")
    logger.info("=" * 80)
    logger.info(f"📊 Documentation Summary:")
    logger.info(f"   Total endpoints documented: {len(endpoints)}")
    logger.info(f"   Documentation formats: OpenAPI, HTML, Markdown")
    logger.info(f"   Files generated: 3 documentation files")

    logger.info(f"\n🎯 Next Steps:")
    logger.info(f"   1. Review the generated documentation files")
    logger.info(f"   2. Use OpenAPI file with Swagger UI")
    logger.info(f"   3. Deploy HTML documentation to web server")
    logger.info(f"   4. Update documentation as APIs evolve")

    logger.info(f"\n📋 All API endpoints have been automatically documented!")


if __name__ == "__main__":
    main()
