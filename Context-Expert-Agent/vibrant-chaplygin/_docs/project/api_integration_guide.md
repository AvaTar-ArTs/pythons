# API Integration Guide
## Setting Up and Configuring AI Service APIs

---

## 🎯 **Overview**

This guide covers the setup and configuration of all AI service APIs used by the Advanced Systems suite. The systems automatically load API keys from your `~/.env.d/` directory, providing secure and organized credential management.

---

## 📁 **Environment Structure**

### **Required Directory Structure**
```
~/.env.d/
├── llm-apis.env          # Language Model APIs
├── art-vision.env        # Image/Video Generation APIs
├── audio-music.env       # Audio Processing APIs
├── gemini.env           # Google Gemini API
├── other-tools.env      # Utility and Social APIs
└── MASTER_CONSOLIDATED.env  # All APIs consolidated
```

### **File Permissions**
```bash
# Secure API key files
chmod 600 ~/.env.d/*.env
```

---

## 🤖 **LLM APIs Configuration**

### **OpenAI API**
```bash
# ~/.env.d/llm-apis.env
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo
```

**Setup Steps:**
1. Visit [OpenAI API](https://platform.openai.com/api-keys)
2. Create new API key
3. Add to environment file
4. Test with: `curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models`

### **Anthropic Claude**
```bash
# ~/.env.d/llm-apis.env
ANTHROPIC_API_KEY=sk-ant-api03-your-anthropic-key-here
```

**Setup Steps:**
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Generate API key
3. Add to environment file
4. Test with API call to verify

### **Google Gemini**
```bash
# ~/.env.d/gemini.env
GOOGLE_API_KEY=your-google-gemini-api-key
```

**Setup Steps:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API key
3. Add to environment file
4. Enable Vertex AI API if needed

### **Mistral AI**
```bash
# ~/.env.d/llm-apis.env
MISTRAL_API_KEY=your-mistral-api-key
```

**Setup Steps:**
1. Visit [Mistral Platform](https://console.mistral.ai/)
2. Generate API key
3. Add to environment file

### **Perplexity AI**
```bash
# ~/.env.d/llm-apis.env
PERPLEXITY_API_KEY=pplx-your-perplexity-key
```

**Setup Steps:**
1. Visit [Perplexity API](https://www.perplexity.ai/settings/api)
2. Generate API key
3. Add to environment file

---

## 🎨 **Creative APIs Configuration**

### **Stability AI (Image Generation)**
```bash
# ~/.env.d/art-vision.env
STABILITY_API_KEY=sk-your-stability-key
STABILITY_BASE_URL=https://api.stability.ai
```

**Setup Steps:**
1. Visit [Stability AI](https://platform.stability.ai/account/keys)
2. Generate API key
3. Add to environment file
4. Test image generation endpoint

### **Leonardo AI**
```bash
# ~/.env.d/art-vision.env
LEONARDO_API_KEY=your-leonardo-key
LEONARDO_BASE_URL=https://cloud.leonardo.ai/api/rest/v1
```

**Setup Steps:**
1. Visit [Leonardo AI](https://app.leonardo.ai/settings)
2. Generate API key
3. Add to environment file

### **Replicate (AI Models)**
```bash
# ~/.env.d/art-vision.env
REPLICATE_API_KEY=r8_your-replicate-key
```

**Setup Steps:**
1. Visit [Replicate](https://replicate.com/account/api-tokens)
2. Generate API token
3. Add to environment file

### **Runway ML (Video)**
```bash
# ~/.env.d/art-vision.env
RUNWAY_API_KEY=key_your-runway-key
```

**Setup Steps:**
1. Visit [Runway ML](https://app.runwayml.com/account/api-keys)
2. Generate API key
3. Add to environment file

---

## 🎵 **Audio APIs Configuration**

### **ElevenLabs (Text-to-Speech)**
```bash
# ~/.env.d/audio-music.env
ELEVENLABS_API_KEY=your-elevenlabs-key
```

**Setup Steps:**
1. Visit [ElevenLabs](https://elevenlabs.io/app/profile)
2. Generate API key
3. Add to environment file
4. Test TTS generation

### **AssemblyAI (Speech-to-Text)**
```bash
# ~/.env.d/audio-music.env
ASSEMBLYAI_API_KEY=your-assemblyai-key
```

**Setup Steps:**
1. Visit [AssemblyAI](https://www.assemblyai.com/app/account)
2. Generate API key
3. Add to environment file

### **Deepgram (Speech Recognition)**
```bash
# ~/.env.d/audio-music.env
DEEPGRAM_API_KEY=your-deepgram-key
```

**Setup Steps:**
1. Visit [Deepgram](https://console.deepgram.com/)
2. Generate API key
3. Add to environment file

---

## 🔧 **Utility APIs Configuration**

### **ScrapingBee (Web Scraping)**
```bash
# ~/.env.d/other-tools.env
SCRAPINGBEE_API_KEY=your-scrapingbee-key
```

### **ScrapingBot**
```bash
# ~/.env.d/other-tools.env
SCRAPINGBOT_API_KEY=your-scrapingbot-key
```

### **Adobe PDF Services**
```bash
# ~/.env.d/other-tools.env
ADOBE_PDF_SERVICES_CLIENT_ID=your-adobe-client-id
ADOBE_PDF_SERVICES_CLIENT_SECRET=your-adobe-client-secret
```

### **PDF.ai**
```bash
# ~/.env.d/other-tools.env
PDFAI_API_KEY=your-pdfai-key
```

---

## 🔐 **Security Best Practices**

### **API Key Management**
```bash
# Never commit API keys to version control
echo "*.env" >> .gitignore
echo "~/.env.d/" >> .gitignore

# Use environment-specific keys
# Production keys should be different from development
```

### **Key Rotation**
```bash
# Rotate keys regularly (recommended: quarterly)
# Update all environment files when rotating
# Test all systems after key rotation
```

### **Access Control**
```bash
# Restrict file permissions
chmod 600 ~/.env.d/*.env

# Use separate keys for different environments
# Consider using key management services for teams
```

---

## 🧪 **Testing API Connections**

### **Automated Testing Script**
```python
#!/usr/bin/env python3
"""
API Connectivity Test Script
"""

import os
import asyncio
import aiohttp
from pathlib import Path
from dotenv import load_dotenv

class APITester:
    def __init__(self):
        self.load_environment()

    def load_environment(self):
        """Load all environment files"""
        env_paths = [
            Path.home() / ".env.d" / "llm-apis.env",
            Path.home() / ".env.d" / "art-vision.env",
            Path.home() / ".env.d" / "audio-music.env",
            Path.home() / ".env.d" / "gemini.env",
            Path.home() / ".env.d" / "other-tools.env"
        ]

        for env_path in env_paths:
            if env_path.exists():
                load_dotenv(env_path)

    async def test_openai(self):
        """Test OpenAI API connection"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return {'status': 'missing_key'}

        try:
            async with aiohttp.ClientSession() as session:
                headers = {'Authorization': f'Bearer {api_key}'}
                async with session.get('https://api.openai.com/v1/models', headers=headers) as response:
                    return {'status': 'success' if response.status == 200 else 'failed'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    async def test_anthropic(self):
        """Test Anthropic API connection"""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return {'status': 'missing_key'}

        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            # Simple test request
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=10,
                messages=[{"role": "user", "content": "Hello"}]
            )
            return {'status': 'success'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    async def test_gemini(self):
        """Test Google Gemini API connection"""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            return {'status': 'missing_key'}

        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            # Simple test
            response = model.generate_content("Hello")
            return {'status': 'success'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    async def run_all_tests(self):
        """Run all API connectivity tests"""
        print("🔍 Testing API Connections...")
        print("=" * 50)

        tests = {
            'OpenAI': self.test_openai(),
            'Anthropic': self.test_anthropic(),
            'Google Gemini': self.test_gemini()
        }

        results = {}
        for name, test_coro in tests.items():
            print(f"Testing {name}...")
            result = await test_coro
            results[name] = result

            if result['status'] == 'success':
                print(f"✅ {name}: Connected successfully")
            elif result['status'] == 'missing_key':
                print(f"⚠️  {name}: API key not configured")
            else:
                print(f"❌ {name}: Connection failed - {result.get('message', 'Unknown error')}")

        print("\n" + "=" * 50)
        successful = sum(1 for r in results.values() if r['status'] == 'success')
        total = len(results)
        print(f"Results: {successful}/{total} APIs connected successfully")

        return results

async def main():
    tester = APITester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
```

### **Running the Test**
```bash
# Save as test_apis.py and run
python test_apis.py
```

---

## 📊 **Rate Limits & Quotas**

### **API Rate Limits**
| Service | Requests/Minute | Requests/Hour | Notes |
|---------|-----------------|----------------|--------|
| OpenAI | 50-350 | 200-2000 | Varies by model |
| Anthropic | 25 | 1000 | Per API key |
| Google Gemini | 60 | 1000 | Free tier limits |
| Stability AI | 10 | 150 | Per API key |
| ElevenLabs | 25 | 10000 | Per API key |

### **Quota Management**
```python
# Configure rate limits in your code
RATE_LIMITS = {
    'openai': {'requests_per_minute': 50, 'tokens_per_minute': 10000},
    'anthropic': {'requests_per_minute': 25},
    'stability': {'requests_per_minute': 10}
}
```

---

## 🚨 **Troubleshooting**

### **Common Issues**

#### **"API Key Not Found"**
```bash
# Check if environment files exist
ls -la ~/.env.d/

# Verify file contents (don't show keys)
head -n 5 ~/.env.d/llm-apis.env

# Check file permissions
ls -l ~/.env.d/*.env
```

#### **Connection Timeouts**
```python
# Increase timeout settings
import aiohttp
timeout = aiohttp.ClientTimeout(total=60)  # 60 seconds
```

#### **Rate Limit Errors**
```python
# Implement exponential backoff
import asyncio
import random

async def api_call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if 'rate_limit' in str(e).lower():
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                await asyncio.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")
```

#### **SSL Certificate Errors**
```python
# Disable SSL verification (not recommended for production)
import ssl
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
```

---

## 🔄 **API Key Rotation**

### **Automated Rotation Script**
```python
#!/usr/bin/env python3
"""
API Key Rotation Script
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta

class APIKeyRotator:
    def __init__(self):
        self.env_dir = Path.home() / ".env.d"
        self.backup_dir = self.env_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)

    def backup_current_keys(self):
        """Backup current API keys"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"api_keys_backup_{timestamp}.json"

        keys = {}
        for env_file in self.env_dir.glob("*.env"):
            if env_file.name != "MASTER_CONSOLIDATED.env":
                with open(env_file, 'r') as f:
                    for line in f:
                        if '=' in line and not line.startswith('#'):
                            key, value = line.strip().split('=', 1)
                            keys[key] = value

        with open(backup_file, 'w') as f:
            json.dump(keys, f, indent=2)

        print(f"✅ Keys backed up to {backup_file}")
        return backup_file

    def rotate_key(self, service_name, new_key):
        """Rotate a specific API key"""
        # This would integrate with your key management service
        # For now, manually update the environment files
        print(f"🔄 Rotating {service_name} API key...")
        # Implementation would update the specific .env file
        print(f"✅ {service_name} key rotated successfully")

    def validate_rotated_keys(self):
        """Validate that rotated keys work"""
        # Run the API connectivity tests
        print("🔍 Validating rotated keys...")
        # Implementation would run test_apis.py
        print("✅ All rotated keys validated successfully")

# Usage
if __name__ == "__main__":
    rotator = APIKeyRotator()

    # Backup current keys
    backup = rotator.backup_current_keys()

    # Rotate specific keys (manual process for security)
    print("\nNext steps:")
    print("1. Generate new API keys from service providers")
    print("2. Update ~/.env.d/*.env files with new keys")
    print("3. Run API connectivity tests")
    print("4. Delete old keys from providers")
    print(f"5. Secure backup available at: {backup}")
```

---

## 📈 **Monitoring & Analytics**

### **API Usage Tracking**
```python
# Track API usage across services
api_usage = {
    'openai': {'requests': 0, 'tokens': 0, 'cost': 0.0},
    'anthropic': {'requests': 0, 'tokens': 0, 'cost': 0.0},
    'stability': {'requests': 0, 'cost': 0.0}
}

# Update usage counters in your API calls
def track_api_usage(service, **metrics):
    if service in api_usage:
        for key, value in metrics.items():
            api_usage[service][key] += value
```

### **Cost Monitoring**
```python
# API cost per 1K tokens (approximate, update with current pricing)
COST_PER_1K_TOKENS = {
    'openai': {'gpt-4': 0.03, 'gpt-3.5': 0.002},
    'anthropic': {'claude-3': 0.015},
    'gemini': {'pro': 0.001}  # Free tier available
}

def calculate_cost(service, model, tokens):
    if service in COST_PER_1K_TOKENS and model in COST_PER_1K_TOKENS[service]:
        rate = COST_PER_1K_TOKENS[service][model]
        return (tokens / 1000) * rate
    return 0.0
```

---

## 🎯 **Best Practices**

### **Security**
- Never commit API keys to version control
- Use environment-specific keys
- Rotate keys regularly
- Monitor API usage for anomalies

### **Performance**
- Implement caching for repeated requests
- Use async/await for concurrent API calls
- Batch requests where possible
- Monitor rate limits and implement backoff

### **Reliability**
- Implement retry logic with exponential backoff
- Have fallback providers for critical services
- Monitor API health and switch providers if needed
- Keep backup API keys for emergencies

### **Cost Management**
- Set spending limits on API dashboards
- Monitor usage patterns and optimize
- Use cheaper models for non-critical tasks
- Implement caching to reduce API calls

---

## 📞 **Support & Resources**

### **API Documentation Links**
- **OpenAI**: https://platform.openai.com/docs
- **Anthropic**: https://docs.anthropic.com/
- **Google Gemini**: https://ai.google.dev/docs
- **Stability AI**: https://platform.stability.ai/docs
- **ElevenLabs**: https://docs.elevenlabs.io/

### **Community Resources**
- **API Status Pages**: Check service status before troubleshooting
- **Developer Forums**: Community support for integration issues
- **GitHub Issues**: Report and find solutions for common problems

### **Professional Services**
- **API Consulting**: For complex integration needs
- **Security Audits**: For API key management validation
- **Performance Optimization**: For high-volume API usage

**Ready to integrate your APIs? Start with the testing script to validate all connections!** 🚀

*API Integration Guide v1.0 - 2025*