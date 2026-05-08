# 🚀 AI Agent System - Complete Setup & Deployment Guide

## 📊 System Overview

Your AI Agent System is now **fully built and ready to use**! Here's what you have:

### ✅ What's Included

```
✅ 5 Agent Personalities (JARVIS, FRIDAY, EDITH, KAREN, VERONICA)
✅ Multi-LLM Support (DeepSeek, Nemotron, GLM, Gemma, GPT-OSS)
✅ Voice I/O (Whisper STT + gTTS TTS)
✅ REST API (FastAPI + WebSocket)
✅ Memory System (Short & Long-term)
✅ NLP Pipeline (Intent + Entity extraction)
✅ 3 Interface Modes (Chat, Voice, API)
✅ Docker Ready
✅ Complete Tests
✅ Full Documentation
```

---

## 📝 Step-by-Step: Getting Started

### **STEP 1: Clone & Setup (5 minutes)**

```bash
# Clone the repository
git clone https://github.com/N1nja-hunt3r/ai-agent-system.git
cd ai-agent-system

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt

# Verify installation
python -c "from src.agents import JarvisAgent; print('✅ Ready!')"
```

### **STEP 2: Configure API Keys (5 minutes)**

```bash
# Create .env file
cp .env.example .env

# Edit with your API keys (NO QUOTES!)
nano .env
```

**Add your API keys:**

```bash
# Choose ONE or MORE providers

# DeepSeek (Recommended - fast & powerful)
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
PRIMARY_LLM_PROVIDER=deepseek

# NVIDIA Nemotron (Multimodal)
NEMOTRON_API_KEY=nvapi-xxxxxxxxxxxxxxxx

# GLM/Zhipu (Agentic)
GLM_API_KEY=xxxxxxxxxxxxxxxx

# Gemma (Google)
GEMMA_API_KEY=xxxxxxxxxxxxxxxx

# GPT-OSS (Efficient)
GPT_OSS_API_KEY=xxxxxxxxxxxxxxxx

# Default agent
DEFAULT_AGENT=friday
```

### **STEP 3: Quick Test (2 minutes)**

```bash
# Test in chat mode
python -m src.main --mode chat

# Type: Hello
# You should see a response from FRIDAY agent

# Type: /agents to list all agents
# Type: /quit to exit
```

✅ **Success!** System is working!

---

## 🎯 Usage Modes

### **Mode 1: Chat Mode (Text-based)**

Best for: Testing, development, quick interactions

```bash
python -m src.main --mode chat
```

**Commands:**
```
/agent jarvis    → Switch to JARVIS (formal, technical)
/agent friday    → Switch to FRIDAY (casual, fun)
/agent edith     → Switch to EDITH (analytical)
/agent karen     → Switch to KAREN (educational)
/agent veronica  → Switch to VERONICA (exploratory)
/agents          → List all agents
/clear           → Clear history
/quit            → Exit
```

**Example Session:**
```
============================================================
AI Agent System - Chat Mode
Current Agent: FRIDAY
============================================================
You: Hello!
FRIDAY: Hey there! 👋 What can I help you with?

You: /agent jarvis
Switched to: JARVIS

You: Explain machine learning
JARVIS: Machine learning is a subset of artificial intelligence...
```

---

### **Mode 2: Voice Mode (Speech I/O)**

Best for: Hands-free interaction, natural conversation

**Prerequisites:**
- Microphone + speaker
- FFmpeg installed

**Install FFmpeg:**

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
choco install ffmpeg
```

**Run voice mode:**

```bash
python -m src.main --mode voice
```

**Example:**
```
============================================================
Listening for voice input...
Press Ctrl+C to exit

Listening... Processing...
You: What's the weather today?
FRIDAY: I can't check the weather, but I can help with...
Speaking... Done
```

---

### **Mode 3: API Mode (REST Server)**

Best for: Integration, web apps, production deployment

```bash
python -m src.main --mode api
```

**Access:**
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- API: http://localhost:8000

**Quick Test:**

```bash
# Health check
curl http://localhost:8000/health

# Send message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "agent": "friday"}'

# List agents
curl http://localhost:8000/agents
```

---

## 🔧 Common Tasks

### **Task 1: Change Default Agent**

```bash
# Edit .env
DEFAULT_AGENT=jarvis  # or friday, edith, karen, veronica

# Restart system
python -m src.main --mode chat
```

### **Task 2: Switch LLM Provider**

```bash
# Edit .env
PRIMARY_LLM_PROVIDER=nemotron

# Fallback order
FALLBACK_LLM_PROVIDERS=glm,gemma,gpt-oss,deepseek
```

### **Task 3: Enable Multiple Providers**

All providers configured in .env with automatic fallback:
- Primary provider tried first
- If fails, tries fallback providers in order
- Ensures reliability

```bash
PRIMARY_LLM_PROVIDER=deepseek
FALLBACK_LLM_PROVIDERS=nemotron,glm,gemma,gpt-oss
```

### **Task 4: Use in Python Code**

```python
from src.chat import ChatEngine

# Initialize
chat = ChatEngine()

# Send message
result = chat.process_message("What is AI?")
print(result["response"])

# Switch agent
chat.switch_agent("jarvis")

# Get history
history = chat.get_conversation_history(limit=10)
for msg in history:
    print(f"{msg['role']}: {msg['content']}")
```

### **Task 5: Integrate with Flask/Django**

```python
from fastapi import FastAPI
from src.chat import ChatEngine

app = FastAPI()
chat_engine = ChatEngine()

@app.post("/my-chat")
async def my_chat(message: str):
    result = chat_engine.process_message(message)
    return {"response": result["response"]}
```

---

## 🐳 Docker Deployment

### **Quick Docker Deployment**

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

# Check logs
docker logs -f ai-agent

# Test API
curl http://localhost:8000/health
```

### **Docker Compose (Easiest)**

```bash
# Copy and edit docker-compose.yml
cp docker-compose.yml docker-compose.local.yml
nano docker-compose.local.yml

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 📊 Agent Personalities Guide

### 🎩 **JARVIS** - Formal & Technical
- **Best for:** Technical questions, detailed explanations, professional needs
- **Personality:** Precise, analytical, respectful
- **Temperature:** 0.3 (consistent)
- **Use:** `python -m src.main --mode chat --agent jarvis`

### 😊 **FRIDAY** - Casual & Fun
- **Best for:** Casual conversation, creative tasks, everyday help
- **Personality:** Warm, engaging, fun
- **Temperature:** 0.8 (creative)
- **Use:** `python -m src.main --mode chat --agent friday`

### 📊 **EDITH** - Analytical & Data-Focused
- **Best for:** Data analysis, pattern recognition, insights
- **Personality:** Logical, systematic, insightful
- **Temperature:** 0.5 (balanced)
- **Use:** `python -m src.main --mode chat --agent edith`

### 🎓 **KAREN** - Patient & Educational
- **Best for:** Learning, step-by-step guidance, teaching
- **Personality:** Patient, encouraging, supportive
- **Temperature:** 0.6 (balanced, educational)
- **Use:** `python -m src.main --mode chat --agent karen`

### 🔬 **VERONICA** - Curious & Exploratory
- **Best for:** Deep dives, technical exploration, experimentation
- **Personality:** Inquisitive, adventurous, creative
- **Temperature:** 0.85 (creative)
- **Use:** `python -m src.main --mode chat --agent veronica`

---

## 🧪 Testing

### **Run All Tests**

```bash
pytest
```

### **Run Specific Tests**

```bash
# Test agents
pytest tests/test_agents.py -v

# Test agent system
pytest tests/test_agents.py::TestAgents -v

# Test with coverage
pytest --cov=src
```

### **Test Output**

```
tests/test_agents.py::TestAgents::test_jarvis_initialization PASSED
tests/test_agents.py::TestAgents::test_friday_initialization PASSED
tests/test_agents.py::TestAgentOrchestrator::test_orchestrator_initialization PASSED
...
======================== 23 passed in 0.45s ==========================
```

---

## 📁 Project Structure

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
│   └── test_agents.py
├── data/                    # Data storage
├── logs/                    # Application logs
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker config
├── docker-compose.yml       # Docker Compose
├── README.md                # Overview
├── SETUP_GUIDE.md          # Setup instructions
├── CHANGELOG.md            # Version history
└── .gitignore              # Git ignore rules
```

---

## 🔑 Key Features Explained

### **Multi-Agent System**
- Switch between 5 different personalities
- Each with unique personality and response style
- Runtime agent switching

### **Multi-LLM Support**
- Support for 5+ LLM providers
- Automatic fallback if primary fails
- Easy provider switching

### **Voice I/O**
- Speech recognition (Whisper)
- Text-to-speech (gTTS)
- Real-time audio processing

### **Memory System**
- Short-term memory (conversation history)
- Long-term memory (persistent storage)
- Automatic memory management

### **REST API**
- Full REST endpoints
- WebSocket support for real-time chat
- Swagger UI documentation

---

## 🚀 Advanced Usage

### **Programmatic Integration**

```python
from src.agents import JarvisAgent
from src.chat import ChatEngine

# Use specific agent
jarvis = JarvisAgent()
response = jarvis.process_user_input("What is quantum computing?")
print(response)

# Use chat engine
chat = ChatEngine()
chat.switch_agent("veronica")
result = chat.process_message("Explore quantum computing")
print(result["response"])
```

### **Custom Agent Creation**

```python
from src.agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="CUSTOM",
            description="My custom agent",
            personality="custom"
        )
    
    def get_system_prompt(self):
        return "You are a custom AI assistant..."
    
    def process_user_input(self, user_input):
        return self.generate_response(user_input)
```

### **API Client in Other Languages**

**Node.js:**
```javascript
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: 'Hello', agent: 'friday' })
});
const data = await response.json();
console.log(data.response);
```

**Go:**
```go
response, _ := http.Post(
    "http://localhost:8000/chat",
    "application/json",
    bytes.NewBuffer([]byte(`{"message":"Hello"}`)),
)
```

---

## 🔒 Security Best Practices

```bash
# 1. Never commit .env with real keys
git add .gitignore
git add .env.example  # Template only

# 2. Use environment variables in production
export DEEPSEEK_API_KEY="sk-xxx"

# 3. Enable API key authentication (optional)
API_KEY_ENABLED=true
API_KEY=your_secret_key

# 4. Enable CORS only for trusted origins
CORS_ORIGINS=["http://localhost:3000"]

# 5. Use HTTPS in production
# (Set up reverse proxy like Nginx)
```

---

## 📈 Performance Optimization

### **For Speed:**
```bash
WHISPER_MODEL=tiny
PRIMARY_LLM_PROVIDER=gpt-oss
MAX_CONTEXT_TOKENS=4096
```

### **For Quality:**
```bash
WHISPER_MODEL=large
PRIMARY_LLM_PROVIDER=deepseek
DEEPSEEK_REASONING_MODEL=deepseek-v4-pro
MAX_CONTEXT_TOKENS=128000
```

### **For Memory Efficiency:**
```bash
USE_QUANTIZATION=true
WHISPER_MODEL=tiny
AGENT_MEMORY_SIZE=50
```

---

## 🆘 Common Issues & Solutions

### **Issue: "API key not recognized"**
```bash
# Solution: Check format (no quotes)
echo "Check your .env file"
DEEPSEEK_API_KEY=sk-xxx  # ✅ Correct
DEEPSEEK_API_KEY="sk-xxx"  # ❌ Wrong
```

### **Issue: "Microphone not found"**
```bash
# Solution: List devices
python -c "from src.voice_engine import MicrophoneInput; m = MicrophoneInput(); print(m.list_devices())"
```

### **Issue: "Port 8000 already in use"**
```bash
# Solution: Use different port
python -m src.main --mode api --port 8080
```

### **Issue: "Out of memory with large models"**
```bash
# Solution: Use smaller models
WHISPER_MODEL=tiny
USE_QUANTIZATION=true
```

---

## 📚 Next Learning Steps

1. **Explore Agent System**
   - Try each agent personality
   - Notice different response styles

2. **Test API Endpoints**
   - Use Swagger UI at http://localhost:8000/docs
   - Try different agents and messages

3. **Integrate into Your Project**
   - Use as Python library
   - Call REST API from your app

4. **Customize Agents**
   - Modify system prompts
   - Create custom agents
   - Fine-tune personalities

5. **Deploy to Production**
   - Use Docker
   - Set up reverse proxy (Nginx)
   - Enable monitoring

---

## 📞 Support & Resources

- **GitHub:** https://github.com/N1nja-hunt3r/ai-agent-system
- **Issues:** Report bugs and request features
- **Documentation:** See README.md and SETUP_GUIDE.md
- **Logs:** Check `logs/agent.log` for debugging

---

## ✨ What Makes This System Special

✅ **5 Unique Agent Personalities** - Each with distinct behavior  
✅ **Multi-LLM Support** - Use multiple AI providers  
✅ **Voice I/O** - Complete voice conversation capability  
✅ **Memory System** - Remembers context and history  
✅ **Production Ready** - Docker, tests, documentation  
✅ **Easy Integration** - REST API + Python library  
✅ **Highly Customizable** - Modify everything via config  
✅ **Well Documented** - Complete setup and API docs  

---

## 🎉 You're All Set!

Your AI Agent System is **fully functional and ready to use**!

**Next:** Pick a mode and start using it:

```bash
# Quick test
python -m src.main --mode chat

# Or deploy with Docker
docker-compose up -d

# Or start API server
python -m src.main --mode api
```

---

**Happy coding! 🚀**

*Made with ❤️ by N1nja-hunt3r*
