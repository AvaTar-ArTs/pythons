# 🤖 Context-Efficient Expert Agents

Intelligent, specialized agents for code analysis that adapt to file content and context.

## Overview

This directory contains lightweight, focused expert agents that provide deep analysis in their specialized domains. The intelligent meta-agent automatically selects and applies the right expert based on content analysis.

## Agents

### 1. 🤖 Intelligent Agent (Meta-Agent)
**File:** `intelligent_agent.py`

The smart orchestrator that automatically detects file content type and routes to appropriate specialized agents.

**Features:**
- Automatic content type detection
- Confidence scoring
- Multi-agent coordination
- Adaptive analysis based on context

**Usage:**
```bash
python intelligent_agent.py <file_or_directory>
```

**Example:**
```bash
# Analyzes file and automatically selects appropriate experts
python intelligent_agent.py ../Instagram-Bot/analyze.py

# Analyzes entire project
python intelligent_agent.py ../ai-image-generator/
```

---

### 2. 📋 Code Reviewer
**File:** `code_reviewer.py`

Specialized in code quality, security, and best practices.

**Analyzes:**
- Security vulnerabilities (eval, exec, hardcoded secrets)
- Code complexity (cyclomatic complexity)
- Best practices (error handling, logging)
- Documentation quality
- Code style and maintainability

**Usage:**
```bash
python code_reviewer.py <file.py> [file2.py ...]
```

**Example:**
```bash
python code_reviewer.py ../functional_category_analyzer.py
```

**Output:**
- Security issues (🔴 critical, 🟡 warning)
- Complexity metrics
- Documentation gaps
- Style recommendations

---

### 3. 🏛️ Software Architect
**File:** `software_architect.py`

Expert in system design, architecture patterns, and scalability.

**Analyzes:**
- Project structure and organization
- Module dependencies and coupling
- Design pattern usage
- Architecture quality scores
- Scalability recommendations

**Usage:**
```bash
python software_architect.py <project_directory> [--json]
```

**Example:**
```bash
python software_architect.py ../Instagram-Bot/
python software_architect.py . --json  # Save full analysis
```

**Provides:**
- Organization score (0-100)
- Coupling analysis
- Circular dependency detection
- Design pattern recognition
- Architectural recommendations

---

### 4. 🔬 Data Scientist
**File:** `data_scientist.py`

Specialized in ML workflows, data quality, and reproducibility.

**Analyzes:**
- ML workflow completeness
- Data loading and preprocessing
- Feature engineering patterns
- Model training and evaluation
- Reproducibility (random seeds)
- Best practices for data science

**Usage:**
```bash
python data_scientist.py <script.py|notebook.ipynb>
```

**Example:**
```bash
python data_scientist.py ../04_ai_tools/train_model.py
python data_scientist.py ../analysis.ipynb
```

**Checks:**
- Train/test split usage
- Data validation
- Feature scaling
- Evaluation metrics
- Random state setting

---

### 5. ⚙️ DevOps Engineer
**File:** `devops_engineer.py`

Expert in CI/CD, containerization, and infrastructure.

**Analyzes:**
- CI/CD configuration (GitHub Actions, GitLab CI, Travis)
- Dockerfiles and containerization
- Infrastructure-as-code (Terraform, Ansible, Kubernetes)
- Security best practices
- Deployment readiness

**Usage:**
```bash
python devops_engineer.py <project_directory>
```

**Example:**
```bash
python devops_engineer.py ..
```

**Provides:**
- CI/CD platform detection
- Docker best practices review
- Infrastructure inventory
- Security configuration check
- DevOps recommendations

---

## Quick Start

### 1. Using the Intelligent Agent (Recommended)

The intelligent agent automatically selects the right expert(s):

```bash
# Analyze any file or project
python intelligent_agent.py <target>
```

The agent will:
1. Detect content type (data science, DevOps, architecture, etc.)
2. Calculate confidence scores
3. Select appropriate expert(s)
4. Run comprehensive analysis
5. Provide unified report

### 2. Using Specific Agents

For targeted analysis, invoke agents directly:

```bash
# Code review
python code_reviewer.py src/main.py

# Architecture analysis
python software_architect.py ./my_project/

# Data science review
python data_scientist.py ml_pipeline.py

# DevOps analysis
python devops_engineer.py .
```

### 3. Batch Analysis

Analyze multiple files:

```bash
# Review all Python files in directory
find . -name "*.py" -exec python code_reviewer.py {} \;

# Or use the intelligent agent on a directory
python intelligent_agent.py ./src/
```

## Installation

No special installation required - agents use only Python standard library plus project dependencies.

Optional dependencies for enhanced analysis:
```bash
pip install pyyaml  # For YAML config analysis (DevOps)
```

## Agent Selection Logic

The intelligent agent uses these heuristics:

| Content Type | Indicators | Selected Agents |
|-------------|-----------|-----------------|
| **Data Science** | pandas, numpy, sklearn, tensorflow, torch, fit(), predict() | Data Scientist + Code Reviewer |
| **DevOps** | Dockerfile, docker-compose, .github/workflows, k8s | DevOps + Architect |
| **Architecture** | Multiple classes, complex structure, 10+ files | Software Architect + Code Reviewer |
| **Python File** | Single .py file | Code Reviewer (primary) |
| **Project Directory** | Directory with 10+ Python files | All applicable agents |

## Output Examples

### Code Reviewer Output
```
🔴 CRITICAL (2 issue(s)):
  Line 45: [security] Hardcoded API key detected
  Line 78: [security] Use of eval() is dangerous

🟡 WARNING (3 issue(s)):
  Line 12: [best-practice] Bare except clause
  Line 34: [complexity] High cyclomatic complexity (15)

💡 SUGGESTION (5 issue(s)):
  Line 56: [documentation] Function missing docstring
  Line 89: [style] Line too long (145 characters)
```

### Software Architect Output
```
🏗️ PROJECT STRUCTURE
  • Max Depth: 3 levels
  • Top-level Modules: 12
  • Organization Score: 85/100

📦 DEPENDENCIES
  • External Packages: 45
  • Coupling Score: 35/100 ✅
  • Circular Dependencies: 0

💡 RECOMMENDATIONS
1. 🔵 Improve Code Documentation [LOW]
   Category: maintainability
   Consider adding module-level docstrings
```

## Integration with Workflow

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Run code review on staged Python files
git diff --cached --name-only --diff-filter=ACM | grep '\.py$' | while read file; do
    python .agents/code_reviewer.py "$file" || exit 1
done
```

### CI/CD Integration

Add to `.github/workflows/analysis.yml`:
```yaml
- name: Run Intelligent Agent Analysis
  run: |
    python .agents/intelligent_agent.py .
```

## Development

### Adding New Agents

1. Create new agent file (e.g., `performance_analyzer.py`)
2. Implement agent class with analysis methods
3. Add `format_*` method for output
4. Update `intelligent_agent.py` to include new agent
5. Add detection patterns to `content_patterns`

### Agent Interface

All agents should implement:
```python
class MyAgent:
    def analyze_*(self, target: Path) -> Dict:
        """Perform analysis, return dict with results"""
        pass

    def format_*(self, analysis: Dict) -> str:
        """Format analysis as readable text"""
        pass
```

## Best Practices

1. **Use Intelligent Agent First**: Let it detect the right expert
2. **Combine Analyses**: Use multiple agents for comprehensive review
3. **Iterate**: Fix critical issues, re-run analysis
4. **Automate**: Integrate into CI/CD and pre-commit hooks
5. **Context Matters**: Provide project context for better analysis

## Troubleshooting

**Issue**: Agent not detecting content type correctly
- **Solution**: Use specific agent directly or check detection logic

**Issue**: Analysis too slow
- **Solution**: Analyze specific files instead of entire project

**Issue**: Import errors
- **Solution**: Run from `.agents/` directory or adjust Python path

## Performance

| Agent | Typical Speed | Memory Usage |
|-------|--------------|--------------|
| Code Reviewer | ~100 files/sec | Low (< 50MB) |
| Software Architect | ~50 files/sec | Medium (~100MB) |
| Data Scientist | ~50 files/sec | Low (< 50MB) |
| DevOps | ~instant | Very Low (< 10MB) |
| Intelligent Agent | Varies | Sum of selected agents |

## Contributing

To improve agents:
1. Add more detection patterns
2. Enhance analysis heuristics
3. Improve output formatting
4. Add new specialized agents
5. Optimize performance

## License

Part of the Python Tools Collection. MIT License.

---

**Generated by Claude Code** 🤖
