# AI Agent System

> JARVIS-like Personal AI Assistant with Voice I/O, Multi-Agent System, and Advanced LLM Integration

## 🤖 Overview

AI Agent System is a sophisticated multi-agent AI assistant system that supports multiple LLM providers, voice I/O, and distinct agent personalities. Built with Python, FastAPI, and cutting-edge AI models.

### ✨ Key Features

- **Multi-Agent System**: 5 distinct agent personalities (JARVIS, FRIDAY, EDITH, KAREN, VERONICA)
- **Advanced LLM Support**: DeepSeek, Nemotron, GLM, Gemma, GPT-OSS with intelligent fallback
- **Voice I/O**: Speech-to-Text (Whisper) and Text-to-Speech (gTTS)
- **Memory Management**: Short-term and long-term persistent memory
- **Intent Recognition**: Advanced NLP with entity extraction
- **REST API**: FastAPI with WebSocket support
- **Multiple Interfaces**: Chat mode, Voice mode, and HTTP API
- **Docker Support**: Ready for containerized deployment

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- API Keys for at least one LLM provider
- Microphone and speaker (for voice mode)

### Installation

```bash
# Clone repository
git clone https://github.com/N1nja-hunt3r/ai-agent-system.git
cd ai-agent-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Running the System

#### 1. Chat Mode (Text-based)

```bash
python -m src.main --mode chat

# Commands:
# /agent <name>  - Switch agent (jarvis, friday, edith, karen, veronica)
# /agents        - List all agents
# /clear         - Clear history
# /quit          - Exit
```

#### 2. Voice Mode (Speech I/O)

```bash
python -m src.main --mode voice

# Speak your commands, system will respond with voice
# Press Ctrl+C to exit
```

#### 3. API Mode (REST/WebSocket)

```bash
python -m src.main --mode api

# API available at: http://localhost:8000
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

## 📋 Agent Personalities

### JARVIS
**Formal, Technical, Professional**
- Best for: Technical questions, detailed explanations, formal interactions
- Personality: Precise, analytical, respectful
- Temperature: 0.3 (consistent, formal)

### FRIDAY
**Casual, Fun, Friendly**
- Best for: Casual conversation, creative tasks, friendly interaction
- Personality: Warm, engaging, fun
- Temperature: 0.8 (creative, diverse)

### EDITH
**Analytical, Data-Focused, Insightful**
- Best for: Data analysis, pattern recognition, strategic insights
- Personality: Logical, systematic, insightful
- Temperature: 0.5 (balanced analytical)

### KAREN
**Helpful, Patient, Educational**
- Best for: Learning, step-by-step guidance, educational content
- Personality: Patient, encouraging, supportive
- Temperature: 0.6 (balanced, educational)

### VERONICA
**Curious, Technical Explorer, Experimental**
- Best for: Exploration, technical deep dives, experimental ideas
- Personality: Inquisitive, adventurous, creative
- Temperature: 0.85 (creative exploration)

## 🔌 API Endpoints

### Chat Endpoints

```bash
# Send message
POST /chat
Body: {"message": "Hello", "agent": "friday"}

# Get conversation history
GET /chat/history?limit=50

# Clear history
DELETE /chat/history

# Get session info
GET /chat/session
```

### Agent Endpoints

```bash
# List all agents
GET /agents

# Get current agent
GET /agents/current

# Switch agent
POST /agents/switch
Body: {"agent": "jarvis"}

# Get specific agent info
GET /agents/{agent_name}
```

### WebSocket

```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8000/ws/chat');

// Send message
ws.send(JSON.stringify({
  message: "Hello",
  agent: "friday"
}));

// Receive response
ws.onmessage = (event) => {
  const response = JSON.parse(event.data);
  console.log(response.response);
};
```

## 🐳 Docker Deployment

### Using Docker Compose

```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f ai-agent

# Stop
docker-compose down
```

### Using Docker CLI

```bash
# Build image
docker build -t ai-agent-system .

# Run container
docker run -d \
  --name ai-agent \
  -p 8000:8000 \
  -e DEEPSEEK_API_KEY=your_key \
  -e PRIMARY_LLM_PROVIDER=deepseek \
  -v ./data:/app/data \
  -v ./logs:/app/logs \
  ai-agent-system
```

## 🏗️ Project Structure

```
ai-agent-system/
├── src/
│   ├── agents/              # Agent personalities
│   │   ├── base_agent.py
│   │   ├── jarvis_agent.py
│   │   ├── friday_agent.py
│   │   ├── edith_agent.py
│   │   ├── karen_agent.py
│   │   ├── veronica_agent.py
│   │   └── agent_orchestrator.py
│   ├── api/                 # REST API
│   │   └── agent_api.py
│   ├── chat/                # Chat engine
│   │   └── chat_engine.py
│   ├── config/              # Configuration
│   │   └── settings.py
│   ├── llm/                 # LLM integration
│   │   └── llm_bridge.py
│   ├── memory/              # Memory management
│   │   └── memory_manager.py
│   ├── nlp/                 # NLP components
│   │   ├── entity_extractor.py
│   │   └── intent_classifier.py
│   ├── stt/                 # Speech-to-text
│   │   └── transcriber.py
│   ├── tts/                 # Text-to-speech
│   │   └── synthesizer.py
│   ├── voice_engine/        # Voice I/O
│   │   ├── microphone.py
│   │   └── speaker.py
│   ├── utils/               # Utilities
│   │   └── logger.py
│   └── main.py              # Entry point
├── tests/                   # Test suite
├── data/                    # Data storage
├── logs/                    # Application logs
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose config
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

Key variables in `.env`:

```bash
# LLM Configuration
PRIMARY_LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_key
NEMOTRON_API_KEY=your_key
GLM_API_KEY=your_key
GEMMA_API_KEY=your_key
GPT_OSS_API_KEY=your_key
FLUX_API_KEY=your_key

# Speech Services
STT_PROVIDER=whisper
WHISPER_MODEL=base
TTS_PROVIDER=gtts
TTS_LANGUAGE=en

# System
DEFAULT_AGENT=friday
DEBUG=false
LOG_LEVEL=INFO
API_PORT=8000
```

## 📚 API Usage Examples

### Python

```python
import requests

# Send message to chat
response = requests.post(
    'http://localhost:8000/chat',
    json={
        'message': 'What is machine learning?',
        'agent': 'karen'  # Use educational agent
    }
)

print(response.json()['response'])

# Switch agent
requests.post(
    'http://localhost:8000/agents/switch',
    json={'agent': 'veronica'}
)

# Get conversation history
history = requests.get('http://localhost:8000/chat/history')
print(history.json())
```

### JavaScript/Node.js

```javascript
// Send message
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Tell me a joke',
    agent: 'friday'
  })
});

const data = await response.json();
console.log(data.response);
```

### cURL

```bash
# Send message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "agent": "friday"}'

# Get agents
curl http://localhost:8000/agents

# Switch agent
curl -X POST http://localhost:8000/agents/switch \
  -H "Content-Type: application/json" \
  -d '{"agent": "jarvis"}'
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_agents.py

# Verbose output
pytest -v
```

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interfaces                      │
│    (Chat | Voice | API | WebSocket)                    │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────┴────────────────────────────────────────┐
│               Chat Engine                              │
│  (Message routing, history management)                │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────┴────────────────────────────────────────┐
│            Agent Orchestrator                          │
│  (Agent selection, coordination)                       │
└───┬──────────────────────────┬──���───────────────────────┘
    │                          │
┌───┴──────────────┐  ┌────────┴───────────────┐
│  Agent Instances │  │  Shared Components    │
│  (5 Personalities)│  │  • Memory Manager     │
│  • JARVIS        │  │  • NLP Pipeline       │
│  • FRIDAY        │  │  • LLM Bridge         │
│  • EDITH         │  │  • Voice I/O          │
│  • KAREN         │  │  • STT/TTS            │
│  • VERONICA      │  │                       │
└──────────────────┘  └───────────────────────┘
         │                     │
         └──────────┬──────────┘
                    │
        ┌───────────┴──────────────┐
        │   External LLM APIs      │
        │  • DeepSeek              │
        │  • Nemotron (NVIDIA)     │
        │  • GLM (Zhipu)           │
        │  • Gemma (Google)        │
        │  • GPT-OSS               │
        │  (with automatic fallback)│
        └──────────────────────────┘
```

## 🔐 Security

- API keys stored in `.env` (never commit)
- CORS configurable
- Rate limiting available
- Input validation on all endpoints
- Secure WebSocket connections

## 📝 Logging

- Console and file logging
- Configurable log level
- Logs stored in `logs/` directory
- Structured logging for easy parsing

## 🚨 Troubleshooting

### Microphone not detected
```bash
# List available audio devices
python -c "from src.voice_engine import MicrophoneInput; m = MicrophoneInput(); print(m.list_devices())"
```

### API Connection Issues
```bash
# Check if API is running
curl http://localhost:8000/health

# Check logs
tail -f logs/agent.log
```

### Memory/Performance
- Adjust `AGENT_MEMORY_SIZE` in `.env`
- Use `MAX_CONTEXT_TOKENS` to control context window
- Enable `USE_QUANTIZATION` for lower resource usage

## 📦 Dependencies

Key packages:
- **FastAPI**: Web framework
- **Pydantic**: Data validation
- **OpenAI Whisper**: Speech-to-text
- **gTTS**: Text-to-speech
- **sounddevice**: Audio I/O
- **requests**: HTTP client
- **python-dotenv**: Environment management

See `requirements.txt` for complete list.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork repository
2. Create feature branch
3. Add tests
4. Submit pull request

## 📄 License

MIT License - See LICENSE file

## 👨‍💻 Author

**N1nja-hunt3r**
- GitHub: [@N1nja-hunt3r](https://github.com/N1nja-hunt3r)

## 🙏 Acknowledgments

- DeepSeek for advanced LLM models
- NVIDIA for Nemotron models
- OpenAI for Whisper
- All open-source contributors

## 📞 Support

For issues, questions, or suggestions:
- Open GitHub Issue
- Check documentation
- Review logs in `logs/agent.log`

---

**Made with ❤️ by N1nja-hunt3r**
