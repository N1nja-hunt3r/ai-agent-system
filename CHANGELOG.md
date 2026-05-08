# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-05-08

### Added
- Initial release of AI Agent System
- 5 distinct agent personalities (JARVIS, FRIDAY, EDITH, KAREN, VERONICA)
- Multi-LLM provider support (DeepSeek, Nemotron, GLM, Gemma, GPT-OSS)
- Voice input/output (Whisper STT, gTTS TTS)
- REST API with FastAPI and WebSocket support
- Memory management system (short-term and long-term)
- Intent classification and entity extraction
- Chat mode with interactive commands
- Voice mode with real-time speech I/O
- Docker and Docker Compose support
- Comprehensive test suite
- Complete documentation and setup guides

### Features
- Multi-agent orchestration
- Automatic LLM provider fallback
- Conversation history and session management
- Agent personality switching at runtime
- Memory persistence with SQLite
- Advanced NLP pipeline
- Rate limiting and CORS support
- Logging to console and file
- Configuration via environment variables

### Technical Stack
- Python 3.11+
- FastAPI for REST API
- Pydantic for data validation
- OpenAI Whisper for STT
- gTTS for TTS
- sounddevice for audio I/O
- requests for HTTP client
- SQLite for persistent storage

---

## Versioning

This project follows [Semantic Versioning](https://semver.org/):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)
