# AI Agent System - Setup & Deployment Guide

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Setup](#local-setup)
3. [Configuration](#configuration)
4. [Running the System](#running-the-system)
5. [API Usage](#api-usage)
6. [Docker Deployment](#docker-deployment)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Configuration](#advanced-configuration)

---

## 🔧 Prerequisites

### System Requirements

- **OS**: Linux, macOS, or Windows
- **Python**: 3.11 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 5GB free space
- **Audio**: Microphone and speaker (for voice mode)

### Required API Keys

You need at least ONE of these:

- **DeepSeek**: [https://api.deepseek.com](https://api.deepseek.com)
- **NVIDIA Nemotron**: [https://build.nvidia.com](https://build.nvidia.com)
- **GLM/Zhipu**: [https://open.bigmodel.cn](https://open.bigmodel.cn)
- **Gemma**: [https://ai.google.dev](https://ai.google.dev)
- **GPT-OSS**: [https://api.gpt-oss.com](https://api.gpt-oss.com)

### Optional (Already included as free)

- Speech-to-Text: Whisper (included)
- Text-to-Speech: gTTS (included)

---

## 🚀 Local Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/N1nja-hunt3r/ai-agent-system.git
cd ai-agent-system
```

### Step 2: Create Virtual Environment

**Linux/macOS:**
```bash
python3.11 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your API keys
# Use your favorite editor (nano, vim, code, etc.)
nano .env
```

### Step 5: Verify Installation

```bash
# Test Python imports
python -c "from src.agents import JarvisAgent; print('✅ Installation successful!')"
```

---

## ⚙️ Configuration

### Setting API Keys in .env

**Important**: API keys should NOT have quotes. Example:

```bash
# ✅ CORRECT
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx

# ❌ WRONG
DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxxxxx"
DEEPSEEK_API_KEY='sk-xxxxxxxxxxxxxxxx'
```

### Minimal Configuration (Required)

```bash
# Pick ONE LLM provider
PRIMARY_LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_actual_key_here

# Default agent
DEFAULT_AGENT=friday

# API server
API_PORT=8000
API_HOST=0.0.0.0
```

### Full Configuration

See `.env.example` for all available options:

- LLM Providers (DeepSeek, Nemotron, GLM, Gemma, GPT-OSS)
- Voice settings (STT/TTS, microphone, speaker)
- Chat settings (history size, context length)
- API settings (host, port, workers, CORS)
- Feature flags (voice, chat, file ops, multimodal)
- Advanced settings (quantization, context tokens, reasoning)

---

## ▶️ Running the System

### 1. Chat Mode (Text-based Interactive)

```bash
python -m src.main --mode chat
```

**Features:**
- Text-based conversation
- Agent switching with `/agent`
- Command history
- Memory persistence

**Commands:**
```
/agent jarvis   - Switch to JARVIS
/agent friday   - Switch to FRIDAY
/agents         - List all agents
/clear          - Clear conversation history
/quit           - Exit
```

**Example:**
```
==================================================
AI Agent System - Chat Mode
Current Agent: FRIDAY
==================================================
You: Hello, who are you?
FRIDAY: Hey there! I'm FRIDAY, your friendly AI assistant...

You: /agent jarvis
Switched to: JARVIS

You: What is machine learning?
JARVIS: Machine learning is a subset of artificial intelligence...
```

### 2. Voice Mode (Speech I/O)

```bash
python -m src.main --mode voice
```

**Features:**
- Real-time speech recognition
- Automatic silence detection
- Voice responses
- No text input needed

**Prerequisites:**
- Working microphone
- Working speaker
- FFmpeg installed (for audio processing)

**Install FFmpeg:**

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
```bash
choco install ffmpeg
```

**Usage:**
```
============================================================
AI Agent System - Voice Mode
Current Agent: FRIDAY
============================================================
Listening for voice input...
Press Ctrl+C to exit

Listening... Processing...
You: Hello FRIDAY
FRIDAY: Hey! What can I do for you today?
Speaking... Done
```

### 3. API Mode (REST/WebSocket Server)

```bash
python -m src.main --mode api
```

Or:

```bash
python -m src.main --mode api --port 8000
```

**Output:**
```
Starting API server on 0.0.0.0:8000
Swagg​er UI: http://localhost:8000/docs

INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Access:**
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📡 API Usage

### Testing with cURL

```bash
# Health check
curl http://localhost:8000/health

# Send message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "agent": "friday"}'

# List agents
curl http://localhost:8000/agents

# Switch agent
curl -X POST http://localhost:8000/agents/switch \
  -H "Content-Type: application/json" \
  -d '{"agent": "jarvis"}'

# Get history
curl http://localhost:8000/chat/history?limit=10
```

### Python Client

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Send message
response = requests.post(
    f"{BASE_URL}/chat",
    json={"message": "What is AI?", "agent": "karen"}
)
print(response.json()["response"])

# Get conversation history
history = requests.get(f"{BASE_URL}/chat/history?limit=5")
for msg in history.json()["history"]:
    print(f"{msg['role']}: {msg['content']}")

# List agents
agents = requests.get(f"{BASE_URL}/agents")
for name, info in agents.json()["agents"].items():
    print(f"- {name}: {info['description']}")
```

### JavaScript/Node.js Client

```javascript
const BASE_URL = 'http://localhost:8000';

// Send message
const response = await fetch(`${BASE_URL}/chat`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Explain quantum computing',
    agent: 'veronica'
  })
});

const data = await response.json();
console.log(data.response);

// WebSocket for real-time chat
const ws = new WebSocket('ws://localhost:8000/ws/chat');

ws.onopen = () => {
  ws.send(JSON.stringify({
    message: 'Hello',
    agent: 'friday'
  }));
};

ws.onmessage = (event) => {
  const response = JSON.parse(event.data);
  console.log('Response:', response.response);
};
```

---

## 🐳 Docker Deployment

### Quick Start with Docker Compose

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f ai-agent

# Stop
docker-compose down
```

### Manual Docker Build

```bash
# Build image
docker build -t ai-agent-system:latest .

# Run with environment variables
docker run -d \
  --name ai-agent \
  -p 8000:8000 \
  -e DEEPSEEK_API_KEY=your_key \
  -e PRIMARY_LLM_PROVIDER=deepseek \
  -v ./data:/app/data \
  -v ./logs:/app/logs \
  ai-agent-system:latest

# Access API
curl http://localhost:8000/health
```

### Docker Environment Variables

```bash
docker run -d \
  -e PRIMARY_LLM_PROVIDER=deepseek \
  -e DEEPSEEK_API_KEY=sk-xxx \
  -e NEMOTRON_API_KEY=nvapi-xxx \
  -e GLM_API_KEY=xxx \
  -e DEFAULT_AGENT=friday \
  -e API_PORT=8000 \
  -e LOG_LEVEL=INFO \
  -v ./data:/app/data \
  -v ./logs:/app/logs \
  ai-agent-system:latest
```

### Production Docker Compose

```yaml
version: '3.8'

services:
  ai-agent:
    image: ai-agent-system:latest
    container_name: ai-agent-prod
    ports:
      - "8000:8000"
    environment:
      - PRIMARY_LLM_PROVIDER=deepseek
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
      - DEFAULT_AGENT=friday
      - DEBUG=false
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: always
    networks:
      - prod-network

networks:
  prod-network:
    driver: bridge
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'src'"

**Solution:**
```bash
# Make sure you're in the project root directory
cd ai-agent-system

# Reinstall in development mode
pip install -e .
```

### Issue: "No API key for provider"

**Solution:**
```bash
# Check your .env file
cat .env

# Verify API key is set without quotes
echo $DEEPSEEK_API_KEY

# Reload environment
source .env
```

### Issue: "Microphone not found" (Voice mode)

**Solution:**
```bash
# List available devices
python -c "from src.voice_engine import MicrophoneInput; m = MicrophoneInput(); print(m.list_devices())"

# Check audio devices on system
arecord -l  # Linux
record -l   # macOS
```

### Issue: "API won't start on port 8000"

**Solution:**
```bash
# Use different port
python -m src.main --mode api --port 8080

# Or check what's using port 8000
lsof -i :8000  # Linux/macOS
netstat -ano | findstr :8000  # Windows
```

### Issue: "LLM API error / No response"

**Solution:**
```bash
# Check API key validity
# Verify internet connection
# Check logs for details
tail -f logs/agent.log

# Test API key directly
curl https://api.deepseek.com/models \
  -H "Authorization: Bearer YOUR_KEY"
```

### Issue: "Out of memory" (Voice mode)

**Solution:**
```bash
# Reduce model size
WHISPER_MODEL=tiny python -m src.main --mode voice

# Or in .env:
WHISPER_MODEL=base  # (tiny, base, small, medium, large)
```

---

## 🔒 Advanced Configuration

### Multi-Provider Fallback

When primary provider fails, system automatically tries fallback providers:

```bash
# .env configuration
PRIMARY_LLM_PROVIDER=deepseek
FALLBACK_LLM_PROVIDERS=nemotron,glm,gemma,gpt-oss

# Automatic order:
# 1. DeepSeek
# 2. Nemotron
# 3. GLM
# 4. Gemma
# 5. GPT-OSS
```

### Rate Limiting

```bash
# .env
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60  # per minute
```

### CORS Configuration

```bash
# .env
CORS_ORIGINS=["*"]  # Allow all
# Or specific origins:
CORS_ORIGINS=["http://localhost:3000", "https://example.com"]
```

### Logging Levels

```bash
LOG_LEVEL=DEBUG    # Verbose (development)
LOG_LEVEL=INFO     # Standard (default)
LOG_LEVEL=WARNING  # Important only
LOG_LEVEL=ERROR    # Errors only
```

### Model Selection

```bash
# For different tasks
DEEPSEEK_REASONING_MODEL=deepseek-v4-pro
DEEPSEEK_CODING_MODEL=deepseek-v4-flash
DEEPSEEK_CHAT_MODEL=deepseek-v4-flash

# Nemotron with safety checks
NEMOTRON_MULTIMODAL_MODEL=nemotron-3-nano-omni-30b-a3b-reasoning
NEMOTRON_SAFETY_CHECK_MODEL=nemotron-3-content-safety
```

### Voice Settings

```bash
# Microphone
MICROPHONE_DEVICE=default
VOICE_TIMEOUT=30  # seconds

# Speaker
SPEAKER_DEVICE=default
TTS_SPEED=1.0  # 0.5-2.0
TTS_LANGUAGE=en

# Whisper
WHISPER_MODEL=base  # tiny, base, small, medium, large
WHISPER_LANGUAGE=en
```

---

## 📊 Performance Tips

### Optimize for Speed

```bash
# Use smaller models
WHISPER_MODEL=tiny

# Use faster LLM
PRIMARY_LLM_PROVIDER=gpt-oss  # Efficient MoE

# Reduce context
MAX_CONTEXT_TOKENS=4096
```

### Optimize for Quality

```bash
# Use larger models
WHISPER_MODEL=large

# Use powerful LLM
PRIMARY_LLM_PROVIDER=deepseek
DEEPSEEK_REASONING_MODEL=deepseek-v4-pro

# Increase context
MAX_CONTEXT_TOKENS=128000
```

### Optimize for Memory

```bash
# Enable quantization
USE_QUANTIZATION=true

# Smaller whisper model
WHISPER_MODEL=tiny

# Reduce memory size
AGENT_MEMORY_SIZE=50
CHAT_HISTORY_SIZE=20
```

---

## 🆘 Getting Help

1. **Check logs:**
   ```bash
   tail -f logs/agent.log
   ```

2. **Review documentation:** See README.md

3. **Test connectivity:**
   ```bash
   curl -v http://localhost:8000/health
   ```

4. **Enable debug mode:**
   ```bash
   DEBUG=true LOG_LEVEL=DEBUG python -m src.main --mode chat
   ```

5. **Open GitHub issue:** [Create issue](https://github.com/N1nja-hunt3r/ai-agent-system/issues)

---

**Happy coding! 🚀**
