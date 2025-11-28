# 🔄 Workflow Consolidation Strategy
**Goal:** Replace 416 individual scripts with ~10-20 reusable, configurable workflows

---

## 📋 Problem Statement

Current State:
- 416 Python scripts with overlapping functionality
- Similar patterns repeated (image upscaling, transcription, file organization, etc.)
- Difficult to maintain, update, and version control
- No unified workflow orchestration
- Manual script execution

Desired State:
- Central workflow engine
- Reusable components/plugins
- Visual workflow management
- Scheduled/triggered execution
- Unified logging and monitoring

---

## 🏗️ Proposed Architecture: Two-Tier Approach

### **Tier 1: Workflow Orchestration (n8n)**
You already have n8n running! This is perfect for:
- **Visual workflow design** (no-code/low-code)
- **Service orchestration** (APIs, webhooks, database)
- **Scheduling and triggers**
- **Error handling & retries**
- **Webhook management**
- **Audit logging**

### **Tier 2: Python Execution Layer**
Unified Python framework that replaces 416 scripts:
- **Modular components** (not monolithic scripts)
- **Configuration-driven** (JSON/YAML workflows)
- **Plugin system** for extensibility
- **Shared utilities** library
- **Single CLI entry point**

---

## 🎯 Consolidation Strategy

### **Phase 1: Identify Core Workflow Patterns**

From your 416 scripts, consolidate into ~15-20 master workflows:

#### **GROUP 1: Media Processing Pipeline**
Currently: `transcribe.py`, `audio.py`, `mp3_batch_timestamper.py`, etc. (12 scripts)
**Consolidated into:** `WorkflowMediaProcessor`

```yaml
workflow:
  name: MediaProcessor
  inputs: [audio_file, video_file]
  steps:
    - name: detect_media_type
      component: media_detector
    - name: transcribe
      component: whisper_transcriber
      if: audio_detected
    - name: convert_format
      component: ffmpeg_converter
      params: format=mp3
    - name: extract_metadata
      component: metadata_extractor
    - name: save_output
      component: file_saver
      params: output_dir=/path/to/output
```

#### **GROUP 2: Image Processing Pipeline**
Currently: `upscale.py`, `image-resize.py`, `add_text.py`, `custom-thumbnail.py`, etc. (25 scripts)
**Consolidated into:** `WorkflowImageProcessor`

```yaml
workflow:
  name: ImageProcessor
  inputs: [image_file, action]
  steps:
    - name: load_image
      component: image_loader
    - name: detect_quality
      component: quality_analyzer
    - name: upscale
      component: upscaler
      if: action == "upscale"
      params: scale_factor=2
    - name: resize
      component: resizer
      if: action == "resize"
      params: width=1920, height=1080
    - name: add_overlay
      component: text_overlay
      if: action == "add_text"
      params: text="${text}", position=top
    - name: save_image
      component: image_saver
      params: output_dir=/path/to/output
```

#### **GROUP 3: File Organization Pipeline**
Currently: `aggressive-renamer.py`, `organize.py`, `intelligent_dedup.py`, etc. (35 scripts)
**Consolidated into:** `WorkflowFileOrganizer`

```yaml
workflow:
  name: FileOrganizer
  inputs: [source_dir, organization_strategy]
  steps:
    - name: scan_directory
      component: directory_scanner
    - name: detect_duplicates
      component: duplicate_detector
      params: method=semantic_hash
    - name: analyze_names
      component: filename_analyzer
    - name: suggest_names
      component: intelligent_renamer
      if: organization_strategy == "intelligent"
    - name: categorize_files
      component: content_categorizer
    - name: execute_moves
      component: file_mover
      params: dry_run=true
    - name: log_changes
      component: change_logger
```

#### **GROUP 4: Data Processing Pipeline**
Currently: `csvmerge.py`, `csvsort.py`, `catalog-to-csv.py`, etc. (20 scripts)
**Consolidated into:** `WorkflowDataProcessor`

```yaml
workflow:
  name: DataProcessor
  inputs: [input_file, operation, format]
  steps:
    - name: load_data
      component: data_loader
      params: format=${format}
    - name: validate_data
      component: data_validator
    - name: transform_data
      component: data_transformer
      params: operation=${operation}
    - name: enrich_with_ai
      component: ai_enricher
      if: operation == "enrich"
      params: model=gpt-4-vision
    - name: save_data
      component: data_saver
      params: output_format=${format}
```

#### **GROUP 5: Web Scraping & Download Pipeline**
Currently: `scrape.py`, `download-files.py`, `ytdl-audiodownload.py`, etc. (15 scripts)
**Consolidated into:** `WorkflowDownloader`

```yaml
workflow:
  name: Downloader
  inputs: [source_url, content_type, output_format]
  steps:
    - name: fetch_content
      component: content_fetcher
      params: url=${source_url}
    - name: parse_content
      component: content_parser
      params: type=${content_type}
    - name: process_content
      component: content_processor
      params: format=${output_format}
    - name: store_metadata
      component: metadata_storer
    - name: save_files
      component: file_saver
      params: output_dir=/downloads
```

#### **GROUP 6: Gallery Generation Pipeline**
Currently: `gallery.py`, `to-html-gallery.py`, `alphabet.py`, etc. (15 scripts)
**Consolidated into:** `WorkflowGalleryBuilder`

```yaml
workflow:
  name: GalleryBuilder
  inputs: [source_dir, template_style, output_format]
  steps:
    - name: collect_media
      component: media_collector
    - name: organize_media
      component: media_organizer
      params: sort_by=alphabetic
    - name: generate_metadata
      component: metadata_generator
    - name: render_gallery
      component: gallery_renderer
      params: template=${template_style}, format=${output_format}
    - name: optimize_output
      component: html_optimizer
    - name: deploy_gallery
      component: gallery_deployer
```

---

## 🔧 Implementation: Unified Python Framework

### **Architecture Overview**

```
unified-workflow-engine/
├── core/
│   ├── workflow_engine.py      # Orchestrates workflow execution
│   ├── component.py             # Base component class
│   └── config_loader.py         # YAML/JSON loader
├── components/
│   ├── media/                   # Media processing components
│   ├── image/                   # Image processing components
│   ├── file/                    # File management components
│   ├── data/                    # Data processing components
│   ├── web/                     # Web scraping/download components
│   └── gallery/                 # Gallery generation components
├── utilities/
│   ├── llm_integration.py       # Unified LLM access (Claude, GPT, Groq)
│   ├── file_utils.py            # File operations (rename, move, dedupe)
│   ├── media_utils.py           # Media operations (transcode, upload)
│   └── logger.py                # Unified logging
├── workflows/                   # Predefined workflow configs
│   ├── media_processor.yaml
│   ├── image_processor.yaml
│   ├── file_organizer.yaml
│   ├── data_processor.yaml
│   ├── downloader.yaml
│   └── gallery_builder.yaml
├── cli/
│   └── main.py                  # Single unified CLI
└── tests/
    └── test_components.py
```

### **Core Implementation Example**

```python
# unified-workflow-engine/core/workflow_engine.py

from typing import Dict, Any, List
import yaml
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class WorkflowEngine:
    """Unified workflow execution engine"""

    def __init__(self, workflows_dir: str = "./workflows"):
        self.workflows_dir = Path(workflows_dir)
        self.components = {}
        self.results = {}

    def load_workflow(self, workflow_name: str) -> Dict[str, Any]:
        """Load workflow from YAML config"""
        workflow_path = self.workflows_dir / f"{workflow_name}.yaml"
        with open(workflow_path) as f:
            return yaml.safe_load(f)

    def execute_workflow(self, workflow_name: str, inputs: Dict[str, Any]) -> Dict:
        """Execute a complete workflow"""
        workflow = self.load_workflow(workflow_name)
        logger.info(f"Executing workflow: {workflow_name}")
        logger.info(f"Inputs: {inputs}")

        results = {}
        context = {**inputs}  # Shared context for all steps

        for step in workflow.get('steps', []):
            # Check conditional execution
            if 'if' in step:
                if not self._evaluate_condition(step['if'], context):
                    logger.info(f"Skipping step {step['name']} (condition false)")
                    continue

            # Execute step
            try:
                logger.info(f"Executing step: {step['name']}")
                component_name = step['component']
                component = self._get_component(component_name)

                params = step.get('params', {})
                # Interpolate variables in params
                params = self._interpolate_params(params, context)

                result = component.execute(context, **params)
                results[step['name']] = result
                context[step['name']] = result  # Store for next steps

            except Exception as e:
                logger.error(f"Error in step {step['name']}: {e}")
                if step.get('on_error') == 'continue':
                    continue
                else:
                    raise

        return results

    def register_component(self, name: str, component: 'Component'):
        """Register a component for use in workflows"""
        self.components[name] = component

    def _get_component(self, name: str) -> 'Component':
        """Get registered component by name"""
        if name not in self.components:
            raise ValueError(f"Component not found: {name}")
        return self.components[name]

    def _evaluate_condition(self, condition: str, context: Dict) -> bool:
        """Evaluate conditional logic"""
        # Simple implementation - can be enhanced
        return eval(condition, {"__builtins__": {}}, context)

    def _interpolate_params(self, params: Dict, context: Dict) -> Dict:
        """Replace ${variable} placeholders with context values"""
        interpolated = {}
        for key, value in params.items():
            if isinstance(value, str) and '${' in value:
                # Extract variable name from ${var_name}
                import re
                var_name = re.search(r'\$\{(\w+)\}', value).group(1)
                interpolated[key] = context.get(var_name, value)
            else:
                interpolated[key] = value
        return interpolated


class Component:
    """Base class for all workflow components"""

    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute(self, context: Dict[str, Any], **kwargs) -> Any:
        """Execute component logic"""
        raise NotImplementedError("Subclasses must implement execute()")


# Example concrete component
class WhisperTranscriber(Component):
    """Transcribes audio using OpenAI Whisper"""

    def __init__(self):
        super().__init__("whisper_transcriber")
        import whisper
        self.model = whisper.load_model("base")

    def execute(self, context: Dict[str, Any], **kwargs) -> str:
        audio_file = kwargs.get('audio_file') or context.get('audio_file')
        self.logger.info(f"Transcribing: {audio_file}")

        result = self.model.transcribe(audio_file)
        text = result['text']

        self.logger.info(f"Transcription complete: {len(text)} characters")
        return text
```

### **CLI Usage**

```bash
# Single unified CLI replaces all 416 scripts

# Execute a workflow
unified-workflow run media_processor --input audio.mp3 --format mp3

# Execute with output format
unified-workflow run image_processor --input image.jpg --action upscale --scale 2

# Execute with config file
unified-workflow run file_organizer --config organizing_strategy.json

# List available workflows
unified-workflow list

# Show workflow details
unified-workflow info media_processor

# Schedule workflow
unified-workflow schedule media_processor --input audio.mp3 --frequency daily --time 02:00

# Run with dry-run
unified-workflow run file_organizer --dry-run
```

---

## 🔗 Integration with n8n

### **Approach 1: n8n Orchestrates Workflows**

n8n can trigger Python workflows:

```
n8n Workflow:
  [Webhook Trigger]
    ↓
  [Python Executor Node]
    ↓
  unified-workflow run media_processor --input ${webhook_body.file}
    ↓
  [Process Result]
    ↓
  [Send Notification]
    ↓
  [Store in Database]
```

### **Approach 2: Python CLI Calls n8n**

Python workflows can call n8n workflows:

```python
# In a component's execute method
import requests

def trigger_external_workflow(workflow_id: str, data: Dict):
    """Trigger an n8n workflow"""
    url = "http://localhost:5678/webhook/my-webhook"
    response = requests.post(url, json=data)
    return response.json()
```

---

## 📊 Consolidation Example: Image Processing

### **Before (5 separate scripts):**
```bash
python upscale.py input.jpg --scale 2
python add_text.py input.jpg --text "My Image"
python image-resize.py input.jpg --width 1920 --height 1080
python gallery.py ./images --template dark
python custom-thumbnail.py input.jpg
```

### **After (1 unified workflow):**
```bash
# Define workflow in YAML
unified-workflow run image_processor \
  --input input.jpg \
  --operations upscale,add_text,resize,gallery,thumbnail \
  --config image_workflow.yaml

# Or programmatically
from unified_workflow import WorkflowEngine

engine = WorkflowEngine()
results = engine.execute_workflow('image_processor', {
    'image_file': 'input.jpg',
    'operations': ['upscale', 'add_text', 'resize'],
    'scale_factor': 2,
    'text': 'My Image',
    'width': 1920,
    'height': 1080
})
```

---

## 🎯 Benefits of Consolidation

| Aspect | Before (416 Scripts) | After (Unified) |
|--------|----------------------|-----------------|
| **Maintenance** | Update 416 files | Update 1 framework + configs |
| **Learning Curve** | Learn each script | Learn 1 engine |
| **Code Reuse** | Duplicated utilities | Shared components |
| **Logging/Monitoring** | Per-script logs | Centralized dashboard |
| **Error Handling** | Individual try/catch | Unified error framework |
| **Scheduling** | Manual/separate tools | Built-in n8n scheduling |
| **Versioning** | 416 versions | 1 version + workflow configs |
| **Testing** | 416 test suites | Component-based tests |
| **Documentation** | 416 different docs | 1 unified documentation |

---

## 📈 Implementation Roadmap

### **Phase 1: Foundation (Week 1-2)**
- [ ] Create WorkflowEngine base
- [ ] Implement Component base class
- [ ] Build config loader (YAML/JSON)
- [ ] Create CLI skeleton

### **Phase 2: Core Components (Week 2-4)**
- [ ] Media components (transcribe, convert)
- [ ] Image components (upscale, resize, overlay)
- [ ] File components (organize, rename, dedupe)
- [ ] Data components (CSV, JSON, enrich)

### **Phase 3: Integration (Week 4-5)**
- [ ] Unified LLM service
- [ ] Database integration
- [ ] API service wrappers
- [ ] n8n integration

### **Phase 4: Migration (Week 5-6)**
- [ ] Create workflows for each major use case
- [ ] Test against existing scripts
- [ ] Performance benchmarking
- [ ] Create migration guide

### **Phase 5: Polish (Week 6-7)**
- [ ] Web dashboard for workflow management
- [ ] API for external tools
- [ ] Comprehensive logging
- [ ] Documentation

---

## 🚀 Quick Start: Build First Workflow

```python
# Step 1: Create a component
# components/media/transcriber.py

from core.component import Component

class WhisperTranscriber(Component):
    def execute(self, context, **kwargs):
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(kwargs['audio_file'])
        return {'text': result['text'], 'segments': result['segments']}

# Step 2: Create a workflow config
# workflows/simple_transcription.yaml

workflow:
  name: SimpleTranscription
  inputs: [audio_file]
  steps:
    - name: transcribe
      component: whisper_transcriber
      params:
        audio_file: ${audio_file}
    - name: save_output
      component: file_saver
      params:
        filename: ${audio_file}_transcript.txt
        content: ${transcribe.text}

# Step 3: Execute
# python -m unified_workflow run simple_transcription --audio_file audio.mp3
```

---

## 💡 Migration Strategy

### **Option A: Gradual Migration**
1. Keep existing scripts (don't delete)
2. Build new unified framework in parallel
3. Convert workflows one at a time
4. Test thoroughly before deprecating old scripts
5. Archive old scripts after 90 days of validation

### **Option B: Wrapper Approach**
1. Create wrapper CLI that calls new engine
2. Maintain backward compatibility
3. Route existing script calls through new engine
4. Monitor for issues
5. Gradually sunset old scripts

### **Option C: Hybrid Approach**
1. Keep specialized/unique scripts (those with <5 variants)
2. Consolidate common patterns into workflows
3. Use n8n for orchestration
4. Build Python CLI for complex operations

---

## 📝 Next Steps

1. **Clarify preference:**
   - Full replacement with unified framework?
   - n8n-focused with Python plugins?
   - Hybrid approach?

2. **Identify priority workflows:**
   - Which 3-5 workflows are used most frequently?
   - Which are most painful to maintain?

3. **Start with one major consolidation:**
   - Pick image processing or media processing
   - Build 80% of that workflow
   - Test against current scripts
   - Measure performance/usability

4. **Plan database schema:**
   - Store workflow executions?
   - Track file processing history?
   - Monitor metrics?

---

**Questions for you:**
- How often do you run these scripts? (manually vs. automated)
- What's the most critical workflow (runs most frequently)?
- Do you prefer visual (n8n) or code-based (Python) workflow definition?
- Want to keep scripts for edge cases or full consolidation?
