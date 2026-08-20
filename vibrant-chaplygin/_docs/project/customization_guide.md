# Customization Guide
## Extending and Modifying the Advanced Systems

---

## 🎯 **Overview**

This guide covers how to customize, extend, and modify the Advanced Systems suite to fit your specific needs. Learn how to add new features, integrate custom APIs, modify existing functionality, and create specialized versions for different use cases.

---

## 🔧 **Core Architecture**

### **Understanding the System Structure**

```python
# Base architecture overview
class AdvancedSystem:
    def __init__(self):
        self.environment = EnvironmentLoader()
        self.clients = APIClientManager()
        self.routing = ModelRouter()
        self.pipeline = ProcessingPipeline()

    async def initialize(self):
        """Initialize all system components"""
        await self.environment.load_configs()
        await self.clients.initialize_all()
        self.routing.setup_routes()
        await self.pipeline.start_processing()
```

### **Key Extension Points**
1. **Environment Loading**: Custom configuration sources
2. **API Clients**: New service integrations
3. **Model Routing**: Custom LLM selection logic
4. **Processing Pipeline**: Custom workflows and stages
5. **Output Processing**: Custom formatters and handlers

---

## 🛠️ **Adding Custom API Integrations**

### **Step 1: Create API Client Class**

```python
# custom_api_client.py
from typing import Dict, Any, Optional
import aiohttp
import logging

logger = logging.getLogger(__name__)

class CustomAPIClient:
    """Custom API client implementation"""

    def __init__(self, api_key: str, base_url: str = None):
        self.api_key = api_key
        self.base_url = base_url or "https://api.custom-service.com/v1"
        self.session = None

    async def initialize(self):
        """Initialize the client"""
        self.session = aiohttp.ClientSession(
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
        )
        logger.info("Custom API client initialized")

    async def close(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()

    async def make_request(self, endpoint: str, method: str = 'GET',
                          data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make authenticated API request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            async with self.session.request(method, url, json=data) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logger.error(f"API request failed: {e}")
            raise

    async def custom_method(self, param1: str, param2: int) -> Dict[str, Any]:
        """Custom API method"""
        data = {
            'parameter1': param1,
            'parameter2': param2
        }
        return await self.make_request('custom-endpoint', 'POST', data)
```

### **Step 2: Register with System**

```python
# In your main system file
from custom_api_client import CustomAPIClient

class ExtendedContentPipeline(AdvancedContentPipeline):
    def __init__(self):
        super().__init__()
        self.custom_clients = {}

    def load_environment(self):
        """Extended environment loading"""
        super().load_environment()

        # Load custom API keys
        custom_env_paths = [
            Path.home() / ".env.d" / "custom-apis.env"
        ]

        for env_path in custom_env_paths:
            if env_path.exists():
                load_dotenv(env_path)

    def initialize_clients(self):
        """Extended client initialization"""
        super().initialize_clients()

        # Initialize custom clients
        if os.getenv('CUSTOM_API_KEY'):
            self.custom_clients['custom_service'] = CustomAPIClient(
                api_key=os.getenv('CUSTOM_API_KEY'),
                base_url=os.getenv('CUSTOM_BASE_URL')
            )

    async def custom_content_generation(self, prompt: str) -> str:
        """Use custom API for content generation"""
        if 'custom_service' not in self.custom_clients:
            raise ValueError("Custom service not configured")

        client = self.custom_clients['custom_service']
        result = await client.custom_method(prompt, 42)
        return result.get('generated_content', '')
```

### **Step 3: Add to Environment Configuration**

```bash
# ~/.env.d/custom-apis.env
CUSTOM_API_KEY=your-custom-api-key
CUSTOM_BASE_URL=https://api.custom-service.com/v1
```

---

## 🎨 **Customizing Content Types**

### **Adding New Content Types**

```python
# custom_content_types.py
from typing import Dict, Any

class CustomContentTypes:
    """Custom content type definitions"""

    @staticmethod
    def get_custom_types() -> Dict[str, Dict[str, Any]]:
        return {
            'product_description': {
                'llm_preference': ['anthropic', 'openai'],
                'tone': 'professional',
                'max_length': 500,
                'features': ['seo_optimization', 'call_to_action'],
                'template': """
                Product: {product_name}
                Key Features: {features}
                Target Audience: {audience}
                Generate compelling product description.
                """
            },

            'technical_tutorial': {
                'llm_preference': ['openai', 'anthropic'],
                'tone': 'educational',
                'max_length': 2000,
                'features': ['code_examples', 'step_by_step', 'prerequisites'],
                'template': """
                Topic: {topic}
                Skill Level: {level}
                Duration: {duration} minutes
                Create comprehensive tutorial with examples.
                """
            },

            'marketing_email': {
                'llm_preference': ['gemini', 'anthropic'],
                'tone': 'persuasive',
                'max_length': 800,
                'features': ['personalization', 'cta_optimization', 'mobile_friendly'],
                'template': """
                Campaign: {campaign_name}
                Audience: {audience_segment}
                Goal: {campaign_goal}
                Subject Line: {subject_line}
                Generate high-converting email content.
                """
            }
        }

    @staticmethod
    def validate_custom_type(content_type: str, config: Dict[str, Any]) -> bool:
        """Validate custom content type configuration"""
        required_fields = ['llm_preference', 'tone', 'max_length', 'features']

        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required field: {field}")

        if not isinstance(config['llm_preference'], list):
            raise ValueError("llm_preference must be a list")

        if config['max_length'] <= 0:
            raise ValueError("max_length must be positive")

        return True
```

### **Integrating Custom Content Types**

```python
# In your content pipeline
from custom_content_types import CustomContentTypes

class ExtendedContentPipeline(AdvancedContentPipeline):
    def __init__(self):
        super().__init__()
        self.custom_content_types = CustomContentTypes.get_custom_types()

    def setup_models(self):
        """Extended model setup with custom types"""
        super().setup_models()

        # Add custom content type routing
        for content_type, config in self.custom_content_types.items():
            self.content_types[content_type] = config['llm_preference'][0]
            self.model_routing[config['llm_preference'][0]] = config['llm_preference']

    async def generate_custom_content(self, content_type: str, **kwargs) -> Dict[str, Any]:
        """Generate content using custom type configuration"""
        if content_type not in self.custom_content_types:
            raise ValueError(f"Unknown content type: {content_type}")

        config = self.custom_content_types[content_type]
        template = config.get('template', '').format(**kwargs)

        # Apply custom features
        features = config.get('features', [])
        enhanced_prompt = self.apply_custom_features(template, features, kwargs)

        # Generate content
        result = await self.generate_content(
            prompt=enhanced_prompt,
            content_type=content_type,
            **kwargs
        )

        # Apply post-processing based on features
        result['content'] = self.post_process_content(result['content'], features)

        return result

    def apply_custom_features(self, prompt: str, features: list, kwargs: dict) -> str:
        """Apply custom features to prompt"""
        enhanced_prompt = prompt

        if 'seo_optimization' in features:
            enhanced_prompt += "\n\nOptimize for SEO with relevant keywords and meta descriptions."

        if 'code_examples' in features:
            enhanced_prompt += "\n\nInclude practical code examples with explanations."

        if 'personalization' in features:
            audience = kwargs.get('audience', 'general')
            enhanced_prompt += f"\n\nTailor content for {audience} audience."

        return enhanced_prompt

    def post_process_content(self, content: str, features: list) -> str:
        """Post-process generated content"""
        processed = content

        if 'cta_optimization' in features:
            processed += "\n\nCall to Action: Contact us today to learn more!"

        if 'mobile_friendly' in features:
            # Add mobile-specific formatting
            processed = processed.replace('\n\n', '\n')

        return processed
```

---

## 🔄 **Customizing Model Routing**

### **Advanced Routing Logic**

```python
# custom_routing.py
from typing import Dict, List, Any
import time

class CustomModelRouter:
    """Advanced model routing with custom logic"""

    def __init__(self):
        self.performance_history = {}
        self.cost_tracker = {}
        self.quality_scores = {}

    def setup_custom_routing(self):
        """Set up custom routing rules"""
        self.routing_rules = {
            'cost_optimization': self.route_by_cost,
            'quality_priority': self.route_by_quality,
            'performance_focus': self.route_by_performance,
            'balanced': self.route_balanced
        }

    def route_by_cost(self, content_type: str, requirements: Dict[str, Any]) -> str:
        """Route to cheapest available model"""
        cost_rankings = {
            'gemini': 1,      # Cheapest
            'anthropic-haiku': 2,
            'openai-gpt-3.5': 3,
            'anthropic': 4,
            'openai-gpt-4': 5  # Most expensive
        }

        available_models = self.get_available_models(content_type)
        return min(available_models, key=lambda x: cost_rankings.get(x, 999))

    def route_by_quality(self, content_type: str, requirements: Dict[str, Any]) -> str:
        """Route to highest quality model"""
        quality_rankings = {
            'openai-gpt-4': 1,      # Highest quality
            'anthropic': 2,
            'openai-gpt-3.5': 3,
            'anthropic-haiku': 4,
            'gemini': 5              # Lowest quality
        }

        available_models = self.get_available_models(content_type)
        return min(available_models, key=lambda x: quality_rankings.get(x, 999))

    def route_by_performance(self, content_type: str, requirements: Dict[str, Any]) -> str:
        """Route based on historical performance"""
        available_models = self.get_available_models(content_type)

        # Use performance history to select best model
        best_model = max(available_models,
                        key=lambda x: self.performance_history.get(x, 0.5))

        return best_model

    def route_balanced(self, content_type: str, requirements: Dict[str, Any]) -> str:
        """Balanced routing considering cost, quality, and performance"""
        available_models = self.get_available_models(content_type)

        scores = {}
        for model in available_models:
            cost_score = self.get_cost_score(model)
            quality_score = self.get_quality_score(model)
            performance_score = self.get_performance_score(model)

            # Weighted combination
            total_score = (quality_score * 0.4 +
                         performance_score * 0.4 +
                         (1 - cost_score) * 0.2)  # Lower cost is better

            scores[model] = total_score

        return max(scores, key=scores.get)

    def get_available_models(self, content_type: str) -> List[str]:
        """Get models available for content type"""
        # Implementation to check which models are configured and available
        return ['openai', 'anthropic', 'gemini']  # Example

    def get_cost_score(self, model: str) -> float:
        """Get normalized cost score (0-1, lower is cheaper)"""
        cost_scores = {
            'gemini': 0.1,
            'anthropic-haiku': 0.3,
            'openai-gpt-3.5': 0.5,
            'anthropic': 0.7,
            'openai-gpt-4': 1.0
        }
        return cost_scores.get(model, 0.5)

    def get_quality_score(self, model: str) -> float:
        """Get quality score (0-1, higher is better)"""
        quality_scores = {
            'openai-gpt-4': 0.95,
            'anthropic': 0.90,
            'openai-gpt-3.5': 0.75,
            'anthropic-haiku': 0.70,
            'gemini': 0.65
        }
        return quality_scores.get(model, 0.5)

    def get_performance_score(self, model: str) -> float:
        """Get performance score based on history"""
        return self.performance_history.get(model, 0.5)

    def update_performance_history(self, model: str, score: float):
        """Update performance tracking"""
        if model not in self.performance_history:
            self.performance_history[model] = score
        else:
            # Exponential moving average
            alpha = 0.1
            self.performance_history[model] = (
                alpha * score +
                (1 - alpha) * self.performance_history[model]
            )
```

### **Integrating Custom Routing**

```python
# In your content pipeline
from custom_routing import CustomModelRouter

class ExtendedContentPipeline(AdvancedContentPipeline):
    def __init__(self):
        super().__init__()
        self.custom_router = CustomModelRouter()
        self.custom_router.setup_custom_routing()

    def _select_optimal_model(self, model_type: str, requirements: Dict) -> str:
        """Override default routing with custom logic"""
        routing_strategy = requirements.get('routing_strategy', 'balanced')

        if routing_strategy in self.custom_router.routing_rules:
            return self.custom_router.routing_rules[routing_strategy](
                model_type, requirements
            )
        else:
            # Fall back to default routing
            return super()._select_optimal_model(model_type, requirements)
```

---

## 🎵 **Adding Custom Output Formats**

### **Creating Output Processors**

```python
# custom_outputs.py
from typing import Dict, Any, List
import json
import markdown
import pdfkit
from jinja2 import Template

class CustomOutputProcessor:
    """Custom output format processors"""

    @staticmethod
    def process_html(content: str, **kwargs) -> str:
        """Convert content to HTML format"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>{{ title }}</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                h1 { color: #2563eb; }
                h2 { color: #374151; }
                p { line-height: 1.6; }
                .highlight { background-color: #fef3c7; padding: 2px 4px; }
            </style>
        </head>
        <body>
            <h1>{{ title }}</h1>
            {{ content }}
        </body>
        </html>
        """

        template = Template(html_template)
        return template.render(
            title=kwargs.get('title', 'Generated Content'),
            content=markdown.markdown(content)
        )

    @staticmethod
    def process_pdf(content: str, **kwargs) -> bytes:
        """Convert content to PDF"""
        html_content = CustomOutputProcessor.process_html(content, **kwargs)

        # Configure pdfkit options
        options = {
            'page-size': 'A4',
            'margin-top': '1.0in',
            'margin-right': '1.0in',
            'margin-bottom': '1.0in',
            'margin-left': '1.0in',
            'encoding': 'UTF-8',
            'no-outline': None,
            'enable-local-file-access': None
        }

        return pdfkit.from_string(html_content, False, options=options)

    @staticmethod
    def process_structured(content: str, **kwargs) -> Dict[str, Any]:
        """Create structured JSON output"""
        lines = content.split('\n')
        sections = []

        current_section = None
        current_content = []

        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                # Save previous section
                if current_section:
                    sections.append({
                        'title': current_section,
                        'content': '\n'.join(current_content)
                    })

                # Start new section
                current_section = line.lstrip('#').strip()
                current_content = []
            elif line:
                current_content.append(line)

        # Add final section
        if current_section:
            sections.append({
                'title': current_section,
                'content': '\n'.join(current_content)
            })

        return {
            'title': kwargs.get('title', 'Structured Content'),
            'sections': sections,
            'metadata': {
                'word_count': len(content.split()),
                'section_count': len(sections),
                'generated_at': kwargs.get('timestamp')
            }
        }

    @staticmethod
    def process_slides(content: str, **kwargs) -> List[Dict[str, Any]]:
        """Convert content to presentation slides"""
        sections = content.split('\n## ')

        slides = []
        for i, section in enumerate(sections):
            lines = section.split('\n')
            title = lines[0].replace('#', '').strip()

            content_lines = []
            for line in lines[1:]:
                if line.strip():
                    content_lines.append(line)

            slides.append({
                'slide_number': i + 1,
                'title': title,
                'content': '\n'.join(content_lines),
                'notes': f"Slide {i + 1}: {title}"
            })

        return slides

    @staticmethod
    def process_api_format(content: str, **kwargs) -> Dict[str, Any]:
        """Format content for API responses"""
        return {
            'status': 'success',
            'data': {
                'content': content,
                'format': 'text',
                'length': len(content),
                'timestamp': kwargs.get('timestamp')
            },
            'metadata': {
                'model_used': kwargs.get('model_used'),
                'processing_time': kwargs.get('processing_time'),
                'content_type': kwargs.get('content_type')
            }
        }
```

### **Registering Custom Processors**

```python
# In your content pipeline
from custom_outputs import CustomOutputProcessor

class ExtendedContentPipeline(AdvancedContentPipeline):
    def __init__(self):
        super().__init__()
        self.register_output_processors()

    def register_output_processors(self):
        """Register custom output processors"""
        self.output_processors = {
            'html': CustomOutputProcessor.process_html,
            'pdf': CustomOutputProcessor.process_pdf,
            'structured': CustomOutputProcessor.process_structured,
            'slides': CustomOutputProcessor.process_slides,
            'api': CustomOutputProcessor.process_api_format
        }

    async def generate_content(self, prompt: str, content_type: str = 'blog_post',
                             output_format: str = 'text', **kwargs) -> Dict[str, Any]:
        """Extended content generation with custom outputs"""
        # Generate base content
        result = await super().generate_content(prompt, content_type, 'text', **kwargs)

        # Apply custom output processing
        if output_format in self.output_processors:
            processor = self.output_processors[output_format]
            result['formatted_content'] = processor(result['text_content'], **kwargs)
            result['output_format'] = output_format

        return result
```

---

## 🔍 **Custom Analysis Modules**

### **Creating Custom Code Analyzers**

```python
# custom_analyzers.py
from typing import Dict, List, Any
import ast
import re

class CustomCodeAnalyzer:
    """Custom code analysis modules"""

    @staticmethod
    def analyze_async_patterns(content: str) -> Dict[str, Any]:
        """Analyze async/await usage patterns"""
        tree = ast.parse(content)

        async_functions = []
        await_calls = []
        async_contexts = []

        for node in ast.walk(tree):
            if isinstance(node, ast.AsyncFunctionDef):
                async_functions.append(node.name)

            if isinstance(node, ast.Await):
                await_calls.append(f"await at line {node.lineno}")

            if isinstance(node, ast.AsyncWith) or isinstance(node, ast.AsyncFor):
                async_contexts.append(f"async context at line {node.lineno}")

        return {
            'async_functions': async_functions,
            'await_calls': await_calls,
            'async_contexts': async_contexts,
            'async_score': len(async_functions) / max(1, len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])),
            'recommendations': []
        }

    @staticmethod
    def analyze_error_handling(content: str) -> Dict[str, Any]:
        """Analyze error handling patterns"""
        tree = ast.parse(content)

        try_blocks = []
        except_blocks = []
        finally_blocks = []
        bare_excepts = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                try_blocks.append(f"try at line {node.lineno}")

                for handler in node.handlers:
                    if handler.type is None:
                        bare_excepts.append(f"bare except at line {handler.lineno}")
                    except_blocks.append(f"except at line {handler.lineno}")

                if node.finalbody:
                    finally_blocks.append(f"finally at line {node.lineno}")

        return {
            'try_blocks': try_blocks,
            'except_blocks': except_blocks,
            'finally_blocks': finally_blocks,
            'bare_excepts': bare_excepts,
            'error_handling_score': len(except_blocks) / max(1, len(try_blocks)),
            'issues': len(bare_excepts),
            'recommendations': [
                "Replace bare except clauses with specific exception types" for _ in bare_excepts
            ]
        }

    @staticmethod
    def analyze_code_complexity(content: str) -> Dict[str, Any]:
        """Analyze code complexity metrics"""
        tree = ast.parse(content)

        functions = []
        classes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = CustomCodeAnalyzer._calculate_cyclomatic_complexity(node)
                functions.append({
                    'name': node.name,
                    'line': node.lineno,
                    'complexity': complexity,
                    'is_complex': complexity > 10
                })

            if isinstance(node, ast.ClassDef):
                classes.append({
                    'name': node.name,
                    'line': node.lineno,
                    'methods': len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                })

        total_complexity = sum(f['complexity'] for f in functions)
        avg_complexity = total_complexity / max(1, len(functions))

        complex_functions = [f for f in functions if f['is_complex']]

        return {
            'functions': functions,
            'classes': classes,
            'total_complexity': total_complexity,
            'average_complexity': avg_complexity,
            'complex_functions': complex_functions,
            'maintainability_index': max(0, 100 - avg_complexity * 2),
            'recommendations': [
                f"Refactor {f['name']} (complexity: {f['complexity']})" for f in complex_functions
            ]
        }

    @staticmethod
    def _calculate_cyclomatic_complexity(node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity for a function"""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Assert)):
                complexity += 1
            elif isinstance(child, ast.BoolOp) and len(child.values) > 1:
                complexity += len(child.values) - 1
            elif isinstance(child, ast.Try):
                complexity += len(child.handlers)
            elif isinstance(child, (ast.And, ast.Or)):
                # Additional complexity for boolean operations
                complexity += 1

        return complexity

    @staticmethod
    def analyze_security_vulnerabilities(content: str) -> Dict[str, Any]:
        """Analyze potential security vulnerabilities"""
        vulnerabilities = []

        # Check for dangerous patterns
        dangerous_patterns = [
            (r'eval\(', 'Use of eval() - potential code injection'),
            (r'exec\(', 'Use of exec() - potential code injection'),
            (r'subprocess\..*shell.*=.*True', 'Shell execution with shell=True'),
            (r'pickle\.loads?\(', 'Use of pickle - potential deserialization attack'),
            (r'os\.system\(', 'Use of os.system - command injection risk'),
            (r'input\(', 'Use of input() in Python 2 - security risk'),
        ]

        for pattern, description in dangerous_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                vulnerabilities.append({
                    'type': 'security_vulnerability',
                    'pattern': match,
                    'description': description,
                    'severity': 'high'
                })

        # Check for SQL injection patterns
        sql_patterns = [
            r'.*SELECT.*\+.*',
            r'.*INSERT.*\+.*',
            r'.*UPDATE.*\+.*',
            r'cursor\.execute\(.*\+.*\)'
        ]

        for pattern in sql_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                vulnerabilities.append({
                    'type': 'sql_injection_risk',
                    'pattern': pattern,
                    'description': 'Potential SQL injection vulnerability',
                    'severity': 'high'
                })

        return {
            'vulnerabilities': vulnerabilities,
            'total_vulnerabilities': len(vulnerabilities),
            'high_severity': len([v for v in vulnerabilities if v['severity'] == 'high']),
            'medium_severity': len([v for v in vulnerabilities if v['severity'] == 'medium']),
            'low_severity': len([v for v in vulnerabilities if v['severity'] == 'low']),
            'security_score': max(0, 100 - len(vulnerabilities) * 10),
            'recommendations': [
                f"Fix {v['description']} - {v['pattern']}" for v in vulnerabilities[:5]
            ]
        }
```

### **Integrating Custom Analyzers**

```python
# In your code orchestrator
from custom_analyzers import CustomCodeAnalyzer

class ExtendedCodeOrchestrator(IntelligentCodeOrchestrator):
    def __init__(self):
        super().__init__()
        self.custom_analyzers = {
            'async_patterns': CustomCodeAnalyzer.analyze_async_patterns,
            'error_handling': CustomCodeAnalyzer.analyze_error_handling,
            'code_complexity': CustomCodeAnalyzer.analyze_code_complexity,
            'security_audit': CustomCodeAnalyzer.analyze_security_vulnerabilities
        }

    async def analyze_codebase(self, focus_areas: List[str] = None) -> Dict[str, Any]:
        """Extended analysis with custom analyzers"""
        if focus_areas is None:
            focus_areas = ['bug_detection', 'performance_optimization',
                         'code_quality', 'async_patterns', 'error_handling']

        result = await super().analyze_codebase(focus_areas)

        # Add custom analysis results
        for area in focus_areas:
            if area in self.custom_analyzers:
                # Run custom analysis on all files
                custom_results = []
                for file_path in self._discover_python_files()[:50]:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        analysis = self.custom_analyzers[area](content)
                        custom_results.append({
                            'file': str(file_path),
                            'analysis': analysis
                        })
                    except Exception as e:
                        logger.error(f"Custom analysis failed for {file_path}: {e}")

                result['custom_analyses'][area] = custom_results

        return result
```

---

## 🚀 **Creating Specialized Systems**

### **Example: Marketing Content Generator**

```python
# marketing_specialist.py
from advanced_content_pipeline import AdvancedContentPipeline
from custom_content_types import CustomContentTypes

class MarketingContentGenerator(AdvancedContentPipeline):
    """Specialized system for marketing content"""

    def __init__(self):
        super().__init__()
        self.marketing_types = {
            'social_ad': self.generate_social_ad,
            'email_campaign': self.generate_email_campaign,
            'landing_page': self.generate_landing_page,
            'video_script': self.generate_video_script
        }

    async def generate_social_ad(self, product: str, target_audience: str,
                               platform: str = 'instagram') -> Dict[str, Any]:
        """Generate social media ad content"""
        prompt = f"""
        Create a compelling social media ad for {product} targeting {target_audience}.
        Platform: {platform}
        Include: Hook, body, call-to-action
        Style: Engaging, persuasive, platform-appropriate
        """

        return await self.generate_content(
            prompt=prompt,
            content_type='marketing_copy',
            output_format='multimodal'
        )

    async def generate_email_campaign(self, campaign_goal: str,
                                    audience_segment: str) -> Dict[str, Any]:
        """Generate email marketing campaign"""
        prompt = f"""
        Create an email marketing campaign for: {campaign_goal}
        Target audience: {audience_segment}

        Include:
        - Subject line options
        - Email body
        - Call-to-action
        - Unsubscribe footer
        """

        return await self.generate_content(
            prompt=prompt,
            content_type='marketing_email',
            output_format='html'
        )

    async def generate_landing_page(self, product: str, value_prop: str) -> Dict[str, Any]:
        """Generate landing page content"""
        prompt = f"""
        Create landing page content for {product}.
        Value proposition: {value_prop}

        Include:
        - Hero headline
        - Key benefits
        - Social proof
        - Call-to-action
        """

        result = await self.generate_content(
            prompt=prompt,
            content_type='marketing_copy',
            output_format='structured'
        )

        # Add landing page specific elements
        result['landing_page_elements'] = {
            'hero_section': self._create_hero_section(result['text_content']),
            'features_section': self._extract_features(result['text_content']),
            'cta_section': self._create_cta_section()
        }

        return result

    async def generate_video_script(self, topic: str, duration: int = 60) -> Dict[str, Any]:
        """Generate video script"""
        prompt = f"""
        Create a video script for: {topic}
        Duration: {duration} seconds

        Include:
        - Hook (first 10 seconds)
        - Main content
        - Call-to-action
        - Voiceover notes
        """

        return await self.generate_content(
            prompt=prompt,
            content_type='presentation',
            output_format='structured'
        )

    def _create_hero_section(self, content: str) -> Dict[str, Any]:
        """Create hero section for landing page"""
        lines = content.split('\n')
        headline = lines[0] if lines else "Default Headline"

        return {
            'headline': headline,
            'subheadline': ' '.join(lines[1:3]) if len(lines) > 2 else "",
            'cta_button': "Get Started Today"
        }

    def _extract_features(self, content: str) -> List[str]:
        """Extract features from content"""
        lines = content.split('\n')
        features = []

        for line in lines:
            line = line.strip()
            if line.startswith('•') or line.startswith('-') or 'feature' in line.lower():
                features.append(line.lstrip('•- ').strip())

        return features[:5]  # Limit to 5 features

    def _create_cta_section(self) -> Dict[str, Any]:
        """Create call-to-action section"""
        return {
            'headline': "Ready to Get Started?",
            'description': "Join thousands of satisfied customers",
            'primary_button': "Start Free Trial",
            'secondary_button': "Learn More"
        }
```

---

## 📊 **Performance Monitoring & Optimization**

### **Custom Metrics Collection**

```python
# custom_metrics.py
from typing import Dict, Any
import time
import psutil
from collections import defaultdict

class CustomMetricsCollector:
    """Custom performance metrics collection"""

    def __init__(self):
        self.metrics = defaultdict(list)
        self.start_time = time.time()

    def record_api_call(self, service: str, model: str, tokens: int, duration: float):
        """Record API call metrics"""
        self.metrics['api_calls'].append({
            'service': service,
            'model': model,
            'tokens': tokens,
            'duration': duration,
            'timestamp': time.time()
        })

    def record_content_generation(self, content_type: str, output_format: str,
                                processing_time: float, content_length: int):
        """Record content generation metrics"""
        self.metrics['content_generation'].append({
            'content_type': content_type,
            'output_format': output_format,
            'processing_time': processing_time,
            'content_length': content_length,
            'timestamp': time.time()
        })

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'uptime': time.time() - self.start_time
        }

    def get_performance_summary(self) -> Dict[str, Any]:
        """Generate performance summary"""
        api_calls = self.metrics['api_calls']
        content_gen = self.metrics['content_generation']

        if not api_calls:
            return {'message': 'No data available'}

        total_tokens = sum(call['tokens'] for call in api_calls)
        avg_api_duration = sum(call['duration'] for call in api_calls) / len(api_calls)
        avg_content_time = sum(cg['processing_time'] for cg in content_gen) / max(1, len(content_gen))

        return {
            'total_api_calls': len(api_calls),
            'total_tokens_used': total_tokens,
            'average_api_duration': avg_api_duration,
            'average_content_generation_time': avg_content_time,
            'content_types_generated': list(set(cg['content_type'] for cg in content_gen)),
            'system_metrics': self.get_system_metrics()
        }

    def export_metrics(self, filename: str):
        """Export metrics to JSON file"""
        export_data = {
            'metrics': dict(self.metrics),
            'summary': self.get_performance_summary(),
            'exported_at': time.time()
        }

        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
```

### **Integration with Monitoring**

```python
# In your main system
from custom_metrics import CustomMetricsCollector

class MonitoredContentPipeline(AdvancedContentPipeline):
    def __init__(self):
        super().__init__()
        self.metrics = CustomMetricsCollector()

    async def generate_content(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Monitored content generation"""
        start_time = time.time()

        result = await super().generate_content(prompt, **kwargs)

        # Record metrics
        processing_time = time.time() - start_time
        content_length = len(result.get('text_content', ''))

        self.metrics.record_content_generation(
            content_type=kwargs.get('content_type', 'unknown'),
            output_format=kwargs.get('output_format', 'text'),
            processing_time=processing_time,
            content_length=content_length
        )

        # Add performance data to result
        result['performance'] = {
            'processing_time': processing_time,
            'content_length': content_length,
            'system_metrics': self.metrics.get_system_metrics()
        }

        return result
```

---

## 🎯 **Advanced Customization Patterns**

### **Plugin Architecture**

```python
# plugin_system.py
from typing import Dict, Any, Protocol
import importlib
import pkgutil

class PluginInterface(Protocol):
    """Plugin interface definition"""
    name: str
    version: str

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize plugin with configuration"""
        ...

    def process(self, data: Any, **kwargs) -> Any:
        """Process data"""
        ...

class PluginManager:
    """Plugin management system"""

    def __init__(self):
        self.plugins = {}
        self.plugin_dir = Path(__file__).parent / "plugins"

    def discover_plugins(self):
        """Discover available plugins"""
        if not self.plugin_dir.exists():
            return

        for finder, name, ispkg in pkgutil.iter_modules([str(self.plugin_dir)]):
            try:
                module = importlib.import_module(f"plugins.{name}")
                plugin_class = getattr(module, f"{name.title()}Plugin")

                if issubclass(plugin_class, PluginInterface):
                    self.plugins[name] = plugin_class()

            except Exception as e:
                logger.error(f"Failed to load plugin {name}: {e}")

    def initialize_plugins(self, config: Dict[str, Any]):
        """Initialize all plugins"""
        for name, plugin in self.plugins.items():
            plugin_config = config.get('plugins', {}).get(name, {})
            try:
                plugin.initialize(plugin_config)
                logger.info(f"Initialized plugin: {name}")
            except Exception as e:
                logger.error(f"Failed to initialize plugin {name}: {e}")

    def execute_plugin(self, plugin_name: str, data: Any, **kwargs) -> Any:
        """Execute a specific plugin"""
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin not found: {plugin_name}")

        return self.plugins[plugin_name].process(data, **kwargs)
```

### **Configuration Management**

```python
# advanced_config.py
from typing import Dict, Any
import yaml
from pathlib import Path

class AdvancedConfigurationManager:
    """Advanced configuration management"""

    def __init__(self):
        self.config_dir = Path.home() / ".config" / "advanced-systems"
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def load_configuration(self, profile: str = "default") -> Dict[str, Any]:
        """Load configuration profile"""
        config_file = self.config_dir / f"{profile}.yaml"

        if config_file.exists():
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        else:
            return self.get_default_config()

    def save_configuration(self, config: Dict[str, Any], profile: str = "default"):
        """Save configuration profile"""
        config_file = self.config_dir / f"{profile}.yaml"

        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, indent=2)

    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'api': {
                'timeout': 60,
                'max_retries': 3,
                'rate_limits': {
                    'openai': {'requests_per_minute': 50},
                    'anthropic': {'requests_per_minute': 25}
                }
            },
            'content': {
                'default_type': 'blog_post',
                'max_length': 2000,
                'quality_checks': ['grammar', 'plagiarism']
            },
            'analysis': {
                'max_files': 100,
                'focus_areas': ['bug_detection', 'performance'],
                'parallel_processing': True
            },
            'plugins': {},
            'monitoring': {
                'enabled': True,
                'metrics_retention_days': 30
            }
        }

    def validate_configuration(self, config: Dict[str, Any]) -> List[str]:
        """Validate configuration and return issues"""
        issues = []

        # Validate API settings
        api_config = config.get('api', {})
        if api_config.get('timeout', 0) <= 0:
            issues.append("API timeout must be positive")

        # Validate content settings
        content_config = config.get('content', {})
        if content_config.get('max_length', 0) <= 0:
            issues.append("Content max_length must be positive")

        return issues

    def merge_configurations(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge configurations"""
        merged = base.copy()

        for key, value in override.items():
            if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                merged[key] = self.merge_configurations(merged[key], value)
            else:
                merged[key] = value

        return merged
```

**Ready to customize your Advanced Systems? Start with the configuration management and plugin architecture above!** 🚀

*Customization Guide v1.0 - 2025*