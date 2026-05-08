"""
Test Suite - Agent System Tests
"""

import pytest
from src.agents.jarvis_agent import JarvisAgent
from src.agents.friday_agent import FridayAgent
from src.agents.edith_agent import EdithAgent
from src.agents.karen_agent import KarenAgent
from src.agents.veronica_agent import VeronicaAgent
from src.agents.agent_orchestrator import AgentOrchestrator
from src.chat.chat_engine import ChatEngine
from src.memory.memory_manager import MemoryManager
from src.nlp.intent_classifier import IntentClassifier
from src.nlp.entity_extractor import EntityExtractor


class TestAgents:
    """Test agent functionality"""
    
    def test_jarvis_initialization(self):
        """Test JARVIS agent initialization"""
        agent = JarvisAgent()
        assert agent.name == "JARVIS"
        assert agent.personality == "formal_technical"
        assert agent.get_system_prompt() is not None
    
    def test_friday_initialization(self):
        """Test FRIDAY agent initialization"""
        agent = FridayAgent()
        assert agent.name == "FRIDAY"
        assert agent.personality == "casual_fun"
    
    def test_edith_initialization(self):
        """Test EDITH agent initialization"""
        agent = EdithAgent()
        assert agent.name == "EDITH"
        assert agent.personality == "analytical_data"
    
    def test_karen_initialization(self):
        """Test KAREN agent initialization"""
        agent = KarenAgent()
        assert agent.name == "KAREN"
        assert agent.personality == "helpful_patient"
    
    def test_veronica_initialization(self):
        """Test VERONICA agent initialization"""
        agent = VeronicaAgent()
        assert agent.name == "VERONICA"
        assert agent.personality == "curious_explorer"
    
    def test_agent_get_info(self):
        """Test agent info retrieval"""
        agent = JarvisAgent()
        info = agent.get_info()
        assert info["name"] == "JARVIS"
        assert "personality" in info
        assert "created_at" in info


class TestAgentOrchestrator:
    """Test agent orchestrator"""
    
    def test_orchestrator_initialization(self):
        """Test orchestrator initialization"""
        orchestrator = AgentOrchestrator()
        assert orchestrator.current_agent is not None
        assert orchestrator.current_agent_name is not None
    
    def test_switch_agent(self):
        """Test agent switching"""
        orchestrator = AgentOrchestrator()
        
        # Switch to JARVIS
        success = orchestrator.switch_agent("jarvis")
        assert success
        assert orchestrator.current_agent_name == "jarvis"
        
        # Switch to FRIDAY
        success = orchestrator.switch_agent("friday")
        assert success
        assert orchestrator.current_agent_name == "friday"
    
    def test_switch_invalid_agent(self):
        """Test switching to invalid agent"""
        orchestrator = AgentOrchestrator()
        success = orchestrator.switch_agent("invalid_agent")
        assert not success
    
    def test_list_agents(self):
        """Test listing all agents"""
        orchestrator = AgentOrchestrator()
        agents = orchestrator.list_agents()
        assert len(agents) == 5
        assert "jarvis" in agents
        assert "friday" in agents
        assert "edith" in agents
        assert "karen" in agents
        assert "veronica" in agents


class TestChatEngine:
    """Test chat engine"""
    
    def test_chat_engine_initialization(self):
        """Test chat engine initialization"""
        engine = ChatEngine()
        assert engine.orchestrator is not None
        assert len(engine.conversation_history) == 0
    
    def test_get_session_info(self):
        """Test session info retrieval"""
        engine = ChatEngine()
        session = engine.get_session_info()
        assert "session_start" in session
        assert "duration_seconds" in session
        assert "messages_count" in session
        assert session["messages_count"] == 0
    
    def test_list_agents(self):
        """Test listing agents from chat engine"""
        engine = ChatEngine()
        agents = engine.list_agents()
        assert len(agents) == 5
    
    def test_clear_history(self):
        """Test clearing conversation history"""
        engine = ChatEngine()
        result = engine.clear_history()
        assert result["success"]


class TestMemoryManager:
    """Test memory management"""
    
    def test_memory_initialization(self):
        """Test memory manager initialization"""
        memory = MemoryManager()
        assert memory.short_term_memory is not None
        assert len(memory.short_term_memory) == 0
    
    def test_add_short_term_memory(self):
        """Test adding to short-term memory"""
        memory = MemoryManager()
        memory.add_short_term_memory("Test memory", "test")
        assert len(memory.short_term_memory) == 1
    
    def test_get_short_term_memory(self):
        """Test retrieving short-term memory"""
        memory = MemoryManager()
        memory.add_short_term_memory("Test 1", "test")
        memory.add_short_term_memory("Test 2", "test")
        
        memories = memory.get_short_term_memory()
        assert len(memories) == 2
    
    def test_clear_short_term_memory(self):
        """Test clearing short-term memory"""
        memory = MemoryManager()
        memory.add_short_term_memory("Test", "test")
        assert len(memory.short_term_memory) > 0
        
        memory.clear_short_term_memory()
        assert len(memory.short_term_memory) == 0


class TestIntentClassifier:
    """Test intent classification"""
    
    def test_intent_classifier_initialization(self):
        """Test intent classifier initialization"""
        classifier = IntentClassifier()
        assert classifier is not None
    
    def test_classify_greeting(self):
        """Test greeting intent classification"""
        classifier = IntentClassifier()
        result = classifier.classify("hello")
        assert result["intent"] == "greeting"
        assert result["confidence"] > 0
    
    def test_classify_farewell(self):
        """Test farewell intent classification"""
        classifier = IntentClassifier()
        result = classifier.classify("goodbye")
        assert result["intent"] == "farewell"
    
    def test_classify_help(self):
        """Test help intent classification"""
        classifier = IntentClassifier()
        result = classifier.classify("can you help me")
        assert result["intent"] == "help"
    
    def test_classify_unknown(self):
        """Test unknown intent classification"""
        classifier = IntentClassifier()
        result = classifier.classify("xyzabc qwerty")
        assert result["intent"] == "unknown"


class TestEntityExtractor:
    """Test entity extraction"""
    
    def test_entity_extractor_initialization(self):
        """Test entity extractor initialization"""
        extractor = EntityExtractor()
        assert extractor is not None
    
    def test_extract_entities(self):
        """Test entity extraction"""
        extractor = EntityExtractor()
        entities = extractor.extract("create file test.txt")
        assert isinstance(entities, list)
    
    def test_extract_numbers(self):
        """Test number extraction"""
        extractor = EntityExtractor()
        numbers = extractor.extract_numbers("I have 5 apples and 10 oranges")
        assert len(numbers) == 2
        assert numbers[0]["value"] == 5.0
        assert numbers[1]["value"] == 10.0
    
    def test_extract_dates(self):
        """Test date extraction"""
        extractor = EntityExtractor()
        dates = extractor.extract_dates("See you tomorrow")
        assert len(dates) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
