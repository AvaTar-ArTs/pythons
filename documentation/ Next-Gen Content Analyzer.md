# 🚀 Quick Start Guide - Next-Gen Content Analyzer

## Get Up and Running in 5 Minutes

---

## 📦 Installation

### Step 1: Install Dependencies

```bash
# Basic installation
pip install asyncio aiofiles

# Optional: For ML/NLP features
pip install sentence-transformers spacy numpy

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Step 2: Download the Analyzer

The analyzer is a single file: `next_gen_content_analyzer.py`

---

## 🎯 Basic Usage

### Example 1: Analyze Current Directory

```python
import asyncio
from pathlib import Path
from next_gen_content_analyzer import NextGenContentAnalyzer, AnalysisConfig

async def quick_analyze():
    # Create analyzer
    analyzer = NextGenContentAnalyzer()

    # Find Python files in current directory
    files = list(Path.cwd().glob('*.py'))
    print(f"Found {len(files)} Python files")

    # Analyze them
    results = await analyzer.analyze_batch(files)

    # Print results
    for result in results:
        print(f"\n📄 {result.metadata.file_name}")
        print(f"   Categories: {[c.value for c in result.semantic_categories]}")
        print(f"   Priority: {result.organization_priority.value}")
        print(f"   Description: {result.intelligent_description}")

    # Show statistics
    stats = analyzer.get_statistics()
    print(f"\n📊 Analyzed {stats['files_analyzed']} files")
    print(f"   Total time: {stats['total_time_seconds']:.2f}s")
    print(f"   Avg per file: {stats['avg_time_per_file_seconds']:.3f}s")

# Run it
asyncio.run(quick_analyze())
```

### Example 2: Analyze Specific Directory

```python
async def analyze_directory(directory_path):
    analyzer = NextGenContentAnalyzer(AnalysisConfig(
        enable_ml_analysis=True,
        enable_caching=True,
        max_file_size_mb=50
    ))

    # Find all files recursively
    files = list(Path(directory_path).rglob('*.*'))
    print(f"Found {len(files)} files")

    # Analyze in batches of 100
    all_results = []
    for i in range(0, len(files), 100):
        batch = files[i:i+100]
        results = await analyzer.analyze_batch(batch)
        all_results.extend(results)
        print(f"Progress: {len(all_results)}/{len(files)}")

    return all_results

# Run it
results = asyncio.run(analyze_directory('/path/to/your/files'))
```

---

## ⚡ Common Use Cases

### Use Case 1: Find All AI/ML Related Files

```python
from next_gen_content_analyzer import ContentCategory

async def find_ai_files():
    analyzer = NextGenContentAnalyzer()
    files = list(Path('/your/directory').rglob('*.py'))
    results = await analyzer.analyze_batch(files)

    # Filter for AI/ML files
    ai_files = [
        r for r in results
        if ContentCategory.AI_ML in r.semantic_categories
    ]

    print(f"Found {len(ai_files)} AI/ML files:")
    for r in ai_files:
        print(f"  - {r.metadata.file_name}")
        print(f"    Score: {r.category_scores.get('ai_ml', 0):.1f}")

asyncio.run(find_ai_files())
```

### Use Case 2: Find High-Priority Files

```python
from next_gen_content_analyzer import Priority

async def find_important_files():
    analyzer = NextGenContentAnalyzer()
    files = list(Path.cwd().rglob('*'))
    results = await analyzer.analyze_batch(files)

    # Filter for high priority
    important = [
        r for r in results
        if r.organization_priority in [Priority.CRITICAL, Priority.HIGH]
    ]

    # Sort by priority score
    important.sort(key=lambda r: r.priority_score, reverse=True)

    print(f"Found {len(important)} important files:")
    for r in important[:10]:  # Top 10
        print(f"  {r.metadata.file_name}")
        print(f"    Priority: {r.organization_priority.value}")
        print(f"    Score: {r.priority_score:.1f}")

asyncio.run(find_important_files())
```

### Use Case 3: Generate Organization Report

```python
import json
from collections import Counter

async def generate_report():
    analyzer = NextGenContentAnalyzer()
    files = list(Path('/your/files').rglob('*'))
    results = await analyzer.analyze_batch(files)

    # Aggregate statistics
    report = {
        'total_files': len(results),
        'total_size_mb': sum(r.metadata.file_size_mb for r in results),
        'category_distribution': Counter(),
        'priority_distribution': Counter(),
        'project_distribution': Counter(),
        'high_priority_files': [],
        'recommendations': []
    }

    for r in results:
        # Count categories
        for cat in r.semantic_categories:
            report['category_distribution'][cat.value] += 1

        # Count priorities
        report['priority_distribution'][r.organization_priority.value] += 1

        # Count projects
        report['project_distribution'][r.project_context.value] += 1

        # Collect high-priority files
        if r.organization_priority in [Priority.CRITICAL, Priority.HIGH]:
            report['high_priority_files'].append({
                'name': r.metadata.file_name,
                'priority': r.organization_priority.value,
                'score': r.priority_score,
                'description': r.intelligent_description
            })

    # Save report
    with open('organization_report.json', 'w') as f:
        json.dump(report, f, indent=2)

    print("✅ Report saved to organization_report.json")
    print(f"📊 Analyzed {report['total_files']} files")
    print(f"   Total size: {report['total_size_mb']:.1f} MB")
    print(f"   Categories: {len(report['category_distribution'])}")
    print(f"   High priority: {len(report['high_priority_files'])}")

asyncio.run(generate_report())
```

---

## 🔌 Using Plugins

### Creating a Simple Plugin

```python
from next_gen_content_analyzer import ContentAnalyzerPlugin, FileMetadata

class WordCountPlugin(ContentAnalyzerPlugin):
    """Count words in files"""

    @property
    def name(self) -> str:
        return "WordCounter"

    @property
    def version(self) -> str:
        return "1.0.0"

    async def analyze(self, content: str, metadata: FileMetadata) -> Dict[str, Any]:
        words = content.split()
        return {
            'word_count': len(words),
            'unique_words': len(set(words)),
            'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0
        }

    def is_applicable(self, metadata: FileMetadata) -> bool:
        # Apply to text files
        return metadata.file_extension in ['.txt', '.md', '.py']

# Use the plugin
analyzer = NextGenContentAnalyzer()
analyzer.register_plugin(WordCountPlugin())
```

---

## ⚙️ Configuration Options

### Minimal Configuration (Fast)

```python
config = AnalysisConfig(
    max_file_size_mb=10,        # Skip large files
    enable_ml_analysis=False,   # Disable ML for speed
    enable_embeddings=False,    # No embeddings
    enable_caching=True         # Cache for repeated runs
)
```

### Balanced Configuration (Recommended)

```python
config = AnalysisConfig(
    max_file_size_mb=50,
    enable_ml_analysis=True,
    enable_embeddings=False,    # Embeddings are slow
    enable_caching=True,
    num_workers=4               # Parallel processing
)
```

### Maximum Quality Configuration (Slow but Accurate)

```python
config = AnalysisConfig(
    max_file_size_mb=100,
    enable_ml_analysis=True,
    enable_embeddings=True,     # Full semantic analysis
    enable_caching=True,
    enable_streaming=True,
    num_workers=8               # More workers
)
```

---

## 📊 Understanding Results

### Result Object Structure

```python
result = await analyzer.analyze_file(Path('example.py'))

# Basic metadata
print(result.metadata.file_name)           # "example.py"
print(result.metadata.file_size_mb)        # 1.5
print(result.metadata.mime_type)           # "text/x-python"

# Categories
print(result.semantic_categories)          # [ContentCategory.AI_ML]
print(result.category_scores)              # {"ai_ml": 45.2, "web": 5.1}

# Project context
print(result.project_context)              # ProjectContext.GENERAL
print(result.project_confidence)           # 0.85

# Analysis
print(result.key_phrases)                  # ["machine learning", "neural network"]
print(result.organization_priority)        # Priority.HIGH
print(result.priority_score)               # 32.5

# NLP features
print(result.sentiment_score)              # 0.25 (slightly positive)
print(result.readability_score)            # 67.3 (good readability)

# Recommendations
print(result.suggested_destination)        # "~/Documents/python/AI-ML/"
print(result.intelligent_description)      # "Medium file | AI/ML | in general project"
```

---

## 🐛 Troubleshooting

### Issue 1: ModuleNotFoundError

```python
# Error: ModuleNotFoundError: No module named 'sentence_transformers'

# Solution: Install optional dependencies
pip install sentence-transformers spacy numpy
```

### Issue 2: spaCy Model Not Found

```python
# Error: Can't find model 'en_core_web_sm'

# Solution: Download the model
python -m spacy download en_core_web_sm
```

### Issue 3: Slow Performance

```python
# Problem: Analysis is too slow

# Solution: Disable expensive features
config = AnalysisConfig(
    enable_ml_analysis=False,   # Disable ML
    enable_embeddings=False,    # Disable embeddings
    enable_caching=True          # Enable caching
)
```

### Issue 4: Out of Memory

```python
# Problem: Memory error on large files

# Solution: Enable streaming and reduce batch size
config = AnalysisConfig(
    max_file_size_mb=10,        # Skip very large files
    enable_streaming=True,       # Stream large files
    max_files_per_batch=50       # Smaller batches
)
```

---

## 💡 Tips & Best Practices

### Tip 1: Use Caching for Development

```python
# First run: Slow (analyzes everything)
analyzer = NextGenContentAnalyzer(AnalysisConfig(enable_caching=True))
results1 = await analyzer.analyze_batch(files)

# Second run: Fast (uses cache)
results2 = await analyzer.analyze_batch(files)  # 100x faster!
```

### Tip 2: Process in Batches for Large Datasets

```python
async def analyze_large_dataset(all_files):
    analyzer = NextGenContentAnalyzer()
    batch_size = 100

    all_results = []
    for i in range(0, len(all_files), batch_size):
        batch = all_files[i:i+batch_size]
        results = await analyzer.analyze_batch(batch)
        all_results.extend(results)

        # Progress indicator
        print(f"Progress: {len(all_results)}/{len(all_files)} "
              f"({len(all_results)/len(all_files)*100:.1f}%)")

    return all_results
```

### Tip 3: Filter Files Before Analysis

```python
# Skip unimportant files
files_to_analyze = [
    f for f in all_files
    if f.suffix in ['.py', '.js', '.md', '.json']  # Only these types
    and f.stat().st_size < 10 * 1024 * 1024        # Less than 10MB
    and not any(part.startswith('.') for part in f.parts)  # No hidden
]
```

### Tip 4: Save Results for Later

```python
import json

# Analyze and save
results = await analyzer.analyze_batch(files)
results_dict = [r.to_dict() for r in results]

with open('analysis_results.json', 'w') as f:
    json.dump(results_dict, f, indent=2)

# Load later
with open('analysis_results.json', 'r') as f:
    saved_results = json.load(f)
```

---

## 🎓 Next Steps

### Beginner
1. ✅ Run the basic example
2. ✅ Analyze your current directory
3. ✅ Understand the results
4. ✅ Try different configurations

### Intermediate
1. 📚 Create a custom plugin
2. 📊 Generate organization reports
3. 🔍 Find similar files
4. ⚙️ Optimize performance

### Advanced
1. 🚀 Analyze entire file systems
2. 🔌 Build domain-specific analyzers
3. 📈 Implement monitoring
4. 🌐 Create a web interface

---

## 📚 Additional Resources

- **Full Documentation**: See `NEXT_GEN_ANALYZER_README.md`
- **Architecture Guide**: See `TRANSFORMATION_SUMMARY.md`
- **API Reference**: See `NEXT_GEN_ANALYZER_README.md#api-reference`
- **Plugin Examples**: See the `CodeComplexityPlugin` in the main file

---

## 🆘 Getting Help

### Common Questions

**Q: How do I analyze just Python files?**
```python
files = list(Path.cwd().rglob('*.py'))
results = await analyzer.analyze_batch(files)
```

**Q: How do I disable ML features for speed?**
```python
config = AnalysisConfig(
    enable_ml_analysis=False,
    enable_embeddings=False
)
analyzer = NextGenContentAnalyzer(config)
```

**Q: How do I find files similar to a specific file?**
```python
# See Example 3 in "Understanding Results" section
target_result = await analyzer.analyze_file(target_file)
# Compare embeddings with other files
```

**Q: Can I analyze files larger than 100MB?**
```python
config = AnalysisConfig(
    max_file_size_mb=1000,  # 1GB limit
    enable_streaming=True    # Must enable streaming
)
```

---

## ✨ You're Ready!

You now have everything you need to start analyzing content like a pro!

```python
# Your journey starts here
async def my_first_analysis():
    analyzer = NextGenContentAnalyzer()
    files = list(Path.cwd().glob('*.py'))
    results = await analyzer.analyze_batch(files)

    print(f"✅ Analyzed {len(results)} files!")
    for result in results:
        print(f"  - {result.metadata.file_name}")

asyncio.run(my_first_analysis())
```

**Happy analyzing! 🚀**

---

*Need more help? Check out the full documentation or create an issue on GitHub!*
