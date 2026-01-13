# 🤖 xAI (Grok) Setup Guide

## Getting Your xAI API Key

### Step 1: Sign up for xAI
1. Visit [https://console.x.ai/](https://console.x.ai/)
2. Sign up with your email: `me@avatararts.org`
3. Verify your email address

### Step 2: Get API Key
1. Log into the xAI console
2. Navigate to API Keys section
3. Create a new API key
4. Copy the key (it will look like `xai-...`)

### Step 3: Add to Environment
1. Open your `~/.env` file
2. Find the line: `XAI_API_KEY=your_xai_api_key_here`
3. Replace `your_xai_api_key_here` with your actual API key
4. Save the file

## Available xAI Models

### Grok-2 (Latest & Recommended)
- **`grok-beta`** - Latest Grok-2 model (default)
- **`grok-2-1212`** - Specific Grok-2 version
- **`grok-2-1212-preview`** - Grok-2 preview version

### Grok-1.5
- **`grok-1.5`** - Improved Grok-1.5 model

### Grok-1 (Original)
- **`grok-1`** - Original Grok model

## Usage Examples

### Basic Commands
```bash
# Quick chat with Grok-2
grok "Hello! Tell me a joke"

# Interactive mode
grok-i

# Streaming response
grok-s "Explain quantum computing"

# Use specific model
grok -m grok-1.5 "What's the weather like?"
```

### Unified AI Toolkit
```bash
# Use xAI through unified toolkit
xai "Your question here"
xai-i                    # Interactive mode

# Model-specific shortcuts
grok2 "Your question"    # Grok-2
grok1 "Your question"    # Grok-1
```

### Advanced Usage
```bash
# Read from file
grok -f question.txt

# List all models
grok-models

# Use with unified AI toolkit
ai -s xai "Your question"
ai -s xai -m grok-beta "Your question"
```

## Features

### xAI CLI Features
- ✅ Multiple Grok models
- ✅ Interactive mode
- ✅ Streaming responses
- ✅ File input support
- ✅ Model listing
- ✅ Error handling

### Grok Model Characteristics
- **Grok-2**: Most capable, best for complex reasoning
- **Grok-1.5**: Good balance of speed and quality
- **Grok-1**: Original model, good for basic tasks

## Troubleshooting

### Common Issues
1. **API Key Error**: Make sure your `XAI_API_KEY` is correctly set in `~/.env`
2. **Rate Limits**: xAI has usage limits, wait before retrying
3. **Model Not Found**: Check available models with `grok-models`

### Getting Help
```bash
# Show help
grok --help

# List models
grok-models

# Test connection
grok "Hello, are you working?"
```

## Pricing & Limits

- Check [xAI Pricing](https://console.x.ai/pricing) for current rates
- Free tier available with usage limits
- Pay-per-use model for higher usage

## Security Notes

- Keep your API key secure
- Don't commit API keys to version control
- Your `.env` file should have 600 permissions
- Consider using environment variables in production

## Next Steps

1. Get your API key from [console.x.ai](https://console.x.ai/)
2. Add it to your `~/.env` file
3. Test with: `grok "Hello, world!"`
4. Try interactive mode: `grok-i`
5. Explore different models: `grok-models`