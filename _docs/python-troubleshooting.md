# Troubleshooting Guide
## Common Issues and Solutions for Advanced Systems

---

## 🎯 **Quick Diagnosis**

### **System Health Check**
```python
# Run this script to diagnose system issues
#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path

async def diagnose_system():
    """Comprehensive system diagnosis"""
    issues = []
    recommendations = []

    # Check Python version
    if sys.version_info < (3, 8):
        issues.append("Python 3.8+ required")
        recommendations.append("Upgrade Python to 3.8 or higher")

    # Check environment files
    env_dir = Path.home() / ".env.d"
    required_files = ['llm-apis.env', 'art-vision.env', 'audio-music.env']

    for env_file in required_files:
        if not (env_dir / env_file).exists():
            issues.append(f"Missing environment file: {env_file}")
            recommendations.append(f"Create {env_file} with required API keys")

    # Check API keys
    try:
        from advanced_content_pipeline import AdvancedContentPipeline
        pipeline = AdvancedContentPipeline()

        if not pipeline.clients:
            issues.append("No API clients initialized")
            recommendations.append("Check API keys in ~/.env.d/ files")

        available_clients = list(pipeline.clients.keys())
        recommendations.append(f"Available LLM clients: {available_clients}")

    except Exception as e:
        issues.append(f"Pipeline initialization failed: {e}")
        recommendations.append("Check API keys and network connectivity")

    # Check dependencies
    try:
        import openai
        import anthropic
        import google.generativeai
    except ImportError as e:
        issues.append(f"Missing dependency: {e}")
        recommendations.append("Run: pip install -r requirements.txt")

    # Print results
    print("🔍 System Diagnosis Results")
    print("=" * 50)

    if issues:
        print(f"❌ Found {len(issues)} issues:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
    else:
        print("✅ No issues found - system is healthy!")

    if recommendations:
        print(f"\n💡 Recommendations ({len(recommendations)}):")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")

    return len(issues) == 0

if __name__ == "__main__":
    success = asyncio.run(diagnose_system())
    sys.exit(0 if success else 1)
```

---

## 🚨 **Critical Issues**

### **API Key Authentication Failures**

#### **Symptoms**
- "Authentication failed" errors
- HTTP 401/403 responses
- "Invalid API key" messages

#### **Causes & Solutions**

**Missing API Keys:**
```bash
# Check if environment files exist
ls -la ~/.env.d/

# Verify file contents (don't show actual keys)
grep -E "^[A-Z_]+=" ~/.env.d/llm-apis.env | wc -l  # Should show multiple lines
```

**Incorrect Key Format:**
```bash
# OpenAI keys should start with 'sk-'
grep "^OPENAI_API_KEY=" ~/.env.d/llm-apis.env

# Anthropic keys should start with 'sk-ant-api03'
grep "^ANTHROPIC_API_KEY=" ~/.env.d/llm-apis.env
```

**Expired or Revoked Keys:**
```bash
# Check key age (regenerate if > 6 months old)
ls -la ~/.env.d/llm-apis.env

# Test key validity
curl -H "Authorization: Bearer YOUR_KEY" https://api.openai.com/v1/models
```

**Environment File Permissions:**
```bash
# Fix permissions
chmod 600 ~/.env.d/*.env
ls -l ~/.env.d/*.env  # Should show -rw-------
```

### **Rate Limiting Issues**

#### **Symptoms**
- "Rate limit exceeded" errors
- HTTP 429 responses
- Inconsistent API failures

#### **Solutions**

**Implement Exponential Backoff:**
```python
import asyncio
import random

async def api_call_with_retry(func, max_retries=3, base_delay=1):
    """Call API with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                print(f"Rate limited, waiting {delay:.1f}s...")
                await asyncio.sleep(delay)
            else:
                raise
    raise Exception("Max retries exceeded")
```

**Configure Rate Limits:**
```python
# In your system configuration
RATE_LIMITS = {
    'openai': {'requests_per_minute': 50, 'tokens_per_minute': 10000},
    'anthropic': {'requests_per_minute': 25},
    'stability': {'requests_per_minute': 10}
}
```

**Monitor Usage:**
```python
# Track API usage
api_usage = {'openai': 0, 'anthropic': 0}

def check_rate_limit(service):
    if api_usage[service] >= RATE_LIMITS[service]['requests_per_minute']:
        raise Exception(f"Rate limit exceeded for {service}")
    api_usage[service] += 1
```

### **Memory and Performance Issues**

#### **Symptoms**
- System slowdowns
- Out of memory errors
- High CPU usage
- Analysis timeouts

#### **Solutions**

**Optimize Analysis Scope:**
```python
# Reduce analysis scope for large codebases
orchestrator.configure_analysis({
    'max_files': 25,              # Limit files analyzed
    'focus_areas': ['bug_detection'],  # Essential checks only
    'analysis_depth': 'quick'     # Faster analysis mode
})
```

**Enable Parallel Processing:**
```python
# Configure parallel analysis
orchestrator.configure_performance({
    'parallel_analysis': True,      # Process files concurrently
    'max_concurrent_requests': 3,   # Limit concurrent API calls
    'batch_size': 10               # Process files in batches
})
```

**Memory Management:**
```python
# Clear caches periodically
orchestrator.clear_analysis_cache()

# Configure memory limits
import resource
resource.setrlimit(resource.RLIMIT_AS, (2 * 1024 * 1024 * 1024, -1))  # 2GB limit
```

---

## 🔧 **API-Specific Issues**

### **OpenAI API Issues**

#### **Model Not Found**
```
Error: The model 'gpt-5' does not exist
```
**Solution:** Update to available models
```python
# Check available models
import openai
client = openai.Client()
models = client.models.list()
print([m.id for m in models.data if 'gpt' in m.id])

# Use: 'gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo'
```

#### **Context Length Exceeded**
```
Error: maximum context length is 8192 tokens
```
**Solution:** Reduce prompt length or use larger context model
```python
# Check token count before sending
import tiktoken

def count_tokens(text, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Truncate if needed
max_tokens = 6000  # Leave room for response
if count_tokens(prompt) > max_tokens:
    prompt = prompt[:int(max_tokens * 3.5)]  # Rough character limit
```

### **Anthropic API Issues**

#### **Invalid Request Format**
```
Error: messages must contain at least one message
```
**Solution:** Ensure proper message format
```python
# Correct format for Claude
messages = [
    {"role": "user", "content": "Your prompt here"}
]

response = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=4000,
    messages=messages
)
```

#### **Rate Limit Errors**
**Solution:** Implement request throttling
```python
import time

class AnthropicRateLimiter:
    def __init__(self):
        self.last_request = 0
        self.min_interval = 60 / 25  # 25 requests per minute

    async def make_request(self, *args, **kwargs):
        elapsed = time.time() - self.last_request
        if elapsed < self.min_interval:
            await asyncio.sleep(self.min_interval - elapsed)

        self.last_request = time.time()
        return await self.client.messages.create(*args, **kwargs)
```

### **Google Gemini Issues**

#### **API Key Issues**
```
Error: API_KEY_INVALID
```
**Solution:** Verify API key and enable Vertex AI
```bash
# Check API key format
echo $GOOGLE_API_KEY | head -c 10  # Should show AIza...

# Enable required APIs in Google Cloud Console
# - Vertex AI API
# - Generative Language API
```

#### **Quota Exceeded**
**Solution:** Monitor and manage quotas
```python
# Check quota usage
import google.api_core.exceptions

try:
    response = await model.generate_content(prompt)
except google.api_core.exceptions.ResourceExhausted:
    print("Gemini quota exceeded, switching to backup model")
    # Fall back to another LLM
```

### **Image Generation Issues**

#### **Stability AI Timeout**
**Solution:** Implement retry logic and smaller requests
```python
# Reduce image size for faster generation
generation_params = {
    'width': 512,      # Smaller than default 1024
    'height': 512,
    'steps': 20        # Fewer steps for faster generation
}
```

#### **Leonardo AI Authentication**
```
Error: Invalid API key
```
**Solution:** Verify Leonardo API key format
```bash
# Leonardo keys are UUID format
grep "^LEONARDO_API_KEY=" ~/.env.d/art-vision.env
# Should show: c89f62cc-5f0d-4587-bde4-cfebb327b379
```

### **Audio Processing Issues**

#### **ElevenLabs Voice Not Found**
```
Error: Voice not found
```
**Solution:** Use available voices
```python
# List available voices first
voices = await elevenlabs.voices.get_all()
print([voice.name for voice in voices])

# Use: 'Rachel', 'Drew', 'Clyde', 'Paul', 'Domi'
```

#### **AssemblyAI Transcription Failures**
**Solution:** Check file format and size
```python
# Supported formats: mp3, mp4, wav, m4a, webm
# Max file size: 5GB
# Check file before upload
import os
file_size = os.path.getsize(audio_file)
if file_size > 5 * 1024 * 1024 * 1024:  # 5GB
    raise ValueError("File too large for AssemblyAI")
```

---

## 🐛 **Code Analysis Issues**

### **AST Parsing Errors**

#### **Syntax Errors in Code**
```
Error: invalid syntax (python code)
```
**Solution:** Skip files with syntax errors
```python
def safe_analyze_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Try to parse AST
        ast.parse(content)
        return analyze_code(content)

    except SyntaxError:
        logger.warning(f"Skipping {file_path} due to syntax errors")
        return None
    except UnicodeDecodeError:
        logger.warning(f"Skipping {file_path} due to encoding issues")
        return None
```

### **Analysis Timeout**

#### **Large Codebases**
**Solution:** Implement analysis timeouts and chunking
```python
import asyncio

async def analyze_with_timeout(file_path, timeout=30):
    try:
        return await asyncio.wait_for(
            analyze_single_file(file_path),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        logger.warning(f"Analysis timeout for {file_path}")
        return {'error': 'timeout', 'file': str(file_path)}
```

### **Memory Issues During Analysis**

#### **Large Files**
**Solution:** Process large files in chunks
```python
def analyze_large_file(file_path, chunk_size=1000):
    analyses = []

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        chunk_num = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break

            chunk_analysis = analyze_code_chunk(chunk, chunk_num)
            analyses.append(chunk_analysis)
            chunk_num += 1

    return combine_chunk_analyses(analyses)
```

---

## 🌐 **Network and Connectivity Issues**

### **SSL Certificate Errors**
```python
# Disable SSL verification (not recommended for production)
import ssl
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Use with aiohttp
async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
    # Make requests
```

### **Proxy Configuration**
```python
# Configure proxy for API calls
proxy_config = {
    'http': 'http://proxy.company.com:8080',
    'https': 'http://proxy.company.com:8080'
}

# Set environment variables
os.environ['HTTP_PROXY'] = proxy_config['http']
os.environ['HTTPS_PROXY'] = proxy_config['https']
```

### **DNS Resolution Issues**
```python
# Add DNS timeout handling
import aiohttp.resolver

resolver = aiohttp.resolver.AsyncResolver()
connector = aiohttp.TCPConnector(resolver=resolver, ttl_dns_cache=30)

async with aiohttp.ClientSession(connector=connector) as session:
    # Make requests with DNS caching
```

---

## 💾 **File System Issues**

### **Permission Errors**
```bash
# Fix file permissions
chmod 644 ~/Documents/pythons/*.py  # Readable by all
chmod 755 ~/Documents/pythons/      # Executable directory

# Check current permissions
ls -la ~/Documents/pythons/
```

### **Path Issues**
```python
# Handle different path formats
from pathlib import Path

def resolve_path(path_str):
    path = Path(path_str).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")

    if not path.is_dir():
        raise NotADirectoryError(f"Not a directory: {path}")

    return path
```

### **Large File Handling**
```python
# Process large files efficiently
def process_large_file(file_path, chunk_size=8192):
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            process_chunk(chunk)
```

---

## 📊 **Performance Monitoring**

### **System Resource Monitoring**
```python
import psutil
import GPUtil

def get_system_status():
    """Get comprehensive system status"""
    return {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory': {
            'total': psutil.virtual_memory().total,
            'available': psutil.virtual_memory().available,
            'percent': psutil.virtual_memory().percent
        },
        'disk': {
            'total': psutil.disk_usage('/').total,
            'free': psutil.disk_usage('/').free,
            'percent': psutil.disk_usage('/').percent
        },
        'gpu': GPUtil.getGPUs()[0].memoryUtil * 100 if GPUtil.getGPUs() else None,
        'network': {
            'bytes_sent': psutil.net_io_counters().bytes_sent,
            'bytes_recv': psutil.net_io_counters().bytes_recv
        }
    }
```

### **API Performance Tracking**
```python
class APIPerformanceTracker:
    def __init__(self):
        self.metrics = defaultdict(list)

    def record_call(self, service, endpoint, duration, status_code):
        self.metrics[service].append({
            'endpoint': endpoint,
            'duration': duration,
            'status_code': status_code,
            'timestamp': time.time()
        })

    def get_performance_stats(self, service):
        calls = self.metrics[service]
        if not calls:
            return {}

        durations = [c['duration'] for c in calls]
        success_rate = len([c for c in calls if c['status_code'] < 400]) / len(calls)

        return {
            'total_calls': len(calls),
            'avg_duration': sum(durations) / len(durations),
            'min_duration': min(durations),
            'max_duration': max(durations),
            'success_rate': success_rate,
            'error_rate': 1 - success_rate
        }
```

---

## 🔄 **Recovery Procedures**

### **System Restart Procedure**
```bash
# Graceful shutdown
pkill -TERM advanced_systems  # Send SIGTERM
sleep 10                      # Wait for cleanup
pkill -KILL advanced_systems  # Force kill if needed

# Restart services
cd ~/advanced-systems
source venv/bin/activate
python content_pipeline/advanced_content_pipeline.py &
python code_orchestrator/intelligent_code_orchestrator.py &
```

### **Database Recovery**
```python
# If using local database
import sqlite3
import shutil

def recover_database(db_path, backup_path):
    """Recover database from backup"""
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, db_path)
        print(f"Database recovered from {backup_path}")
    else:
        print("No backup found")

# Usage
recover_database('system.db', 'system.db.backup')
```

### **Configuration Rollback**
```python
def rollback_configuration(backup_file):
    """Rollback to previous configuration"""
    if os.path.exists(backup_file):
        shutil.copy2(backup_file, 'current_config.yaml')
        print(f"Configuration rolled back from {backup_file}")
        # Restart services with new config
        restart_services()
    else:
        print("No configuration backup found")
```

---

## 📞 **Getting Help**

### **Debug Information Collection**
```python
def collect_debug_info():
    """Collect comprehensive debug information"""
    debug_info = {
        'timestamp': datetime.now().isoformat(),
        'python_version': sys.version,
        'platform': platform.platform(),
        'environment': dict(os.environ),
        'installed_packages': {pkg.key: pkg.version for pkg in pkg_resources.working_set},
        'system_resources': get_system_status(),
        'configuration_files': {}
    }

    # Check configuration files
    env_dir = Path.home() / ".env.d"
    for env_file in env_dir.glob("*.env"):
        try:
            with open(env_file, 'r') as f:
                # Count lines without showing content
                line_count = sum(1 for _ in f)
            debug_info['configuration_files'][env_file.name] = {
                'exists': True,
                'lines': line_count
            }
        except Exception as e:
            debug_info['configuration_files'][env_file.name] = {
                'exists': True,
                'error': str(e)
            }

    # Save debug info
    with open('debug_info.json', 'w') as f:
        json.dump(debug_info, f, indent=2, default=str)

    return debug_info
```

### **Error Reporting Template**
When reporting issues, include:

1. **System Information**
   - OS and version
   - Python version
   - Installed packages (pip list)

2. **Error Details**
   - Full error message and traceback
   - When the error occurred
   - Steps to reproduce

3. **Configuration**
   - Which APIs are configured (don't include keys)
   - System resource usage
   - Recent changes

4. **Logs**
   - Application logs
   - API call logs (without sensitive data)

---

## 🚀 **Advanced Troubleshooting**

### **Distributed Processing Setup**
For very large codebases, set up distributed analysis:

```python
# distributed_orchestrator.py
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

class DistributedCodeOrchestrator(IntelligentCodeOrchestrator):
    def __init__(self, num_workers=None):
        super().__init__()
        self.num_workers = num_workers or mp.cpu_count()

    async def analyze_codebase_distributed(self, focus_areas):
        """Analyze codebase using multiple processes"""
        python_files = self._discover_python_files()
        file_chunks = self._chunk_files(python_files, self.num_workers)

        with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            futures = [
                executor.submit(self._analyze_file_chunk, chunk, focus_areas)
                for chunk in file_chunks
            ]

            results = []
            for future in futures:
                results.extend(future.result())

        return self._aggregate_distributed_results(results)

    def _chunk_files(self, files, num_chunks):
        """Split files into chunks for parallel processing"""
        chunk_size = len(files) // num_chunks
        return [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

    def _analyze_file_chunk(self, file_chunk, focus_areas):
        """Analyze a chunk of files"""
        results = []
        for file_path in file_chunk:
            try:
                result = asyncio.run(self._analyze_single_file(file_path, focus_areas))
                results.append(result)
            except Exception as e:
                results.append({'error': str(e), 'file': str(file_path)})
        return results
```

### **Custom Error Recovery**
```python
class ErrorRecoveryManager:
    def __init__(self):
        self.recovery_strategies = {
            'api_timeout': self.recover_api_timeout,
            'rate_limit': self.recover_rate_limit,
            'memory_error': self.recover_memory_error,
            'network_error': self.recover_network_error
        }

    def recover_from_error(self, error_type, context):
        """Apply appropriate recovery strategy"""
        if error_type in self.recovery_strategies:
            return self.recovery_strategies[error_type](context)
        else:
            logger.error(f"No recovery strategy for {error_type}")
            return False

    def recover_api_timeout(self, context):
        """Recover from API timeout"""
        # Increase timeout
        context['timeout'] *= 2
        if context['timeout'] > 300:  # 5 minutes max
            return False
        return True

    def recover_rate_limit(self, context):
        """Recover from rate limiting"""
        import time
        time.sleep(context.get('backoff_time', 60))
        return True

    def recover_memory_error(self, context):
        """Recover from memory issues"""
        # Reduce batch size
        if 'batch_size' in context:
            context['batch_size'] = max(1, context['batch_size'] // 2)
        # Clear caches
        self.clear_all_caches()
        return True

    def recover_network_error(self, context):
        """Recover from network issues"""
        # Try different endpoint or region
        context['endpoint'] = self.get_backup_endpoint(context.get('endpoint'))
        return True
```

---

**Still having issues? Run the system diagnosis script at the beginning of this guide and share the output for targeted assistance!** 🚀

*Troubleshooting Guide v1.0 - 2025*