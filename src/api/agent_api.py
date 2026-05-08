"""
Agent API - REST API for AI Agent System
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import logging

from src.chat.chat_engine import ChatEngine
from src.config import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# ============================================================================
# Pydantic Models
# ============================================================================

class MessageRequest(BaseModel):
    """Message request model"""
    message: str
    agent: Optional[str] = None

class MessageResponse(BaseModel):
    """Message response model"""
    success: bool
    response: Optional[str] = None
    agent: str
    error: Optional[str] = None

class AgentSwitchRequest(BaseModel):
    """Agent switch request"""
    agent: str

class AgentInfo(BaseModel):
    """Agent information"""
    name: str
    description: str
    personality: str

# ============================================================================
# FastAPI Application Setup
# ============================================================================

app = FastAPI(
    title="AI Agent System API",
    description="JARVIS-like Personal AI Assistant",
    version="1.0.0",
)

# Configure CORS
if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Initialize chat engine
chat_engine = ChatEngine()

# ============================================================================
# Health & Info Routes
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/info")
async def info():
    """Get system information"""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "llm_provider": settings.primary_llm_provider,
        "features": {
            "voice": settings.feature_voice,
            "chat": settings.feature_chat,
            "multimodal": settings.feature_multimodal,
        },
    }

# ============================================================================
# Chat Routes
# ============================================================================

@app.post("/chat", response_model=MessageResponse)
async def chat(request: MessageRequest):
    """
    Send message to chat
    
    Args:
        request: Message request with message text
    
    Returns:
        Message response
    """
    try:
        # Switch agent if specified
        if request.agent:
            chat_engine.switch_agent(request.agent)
        
        # Process message
        result = chat_engine.process_message(request.message)
        
        if result["success"]:
            return MessageResponse(
                success=True,
                response=result["response"],
                agent=result["agent"],
            )
        else:
            return MessageResponse(
                success=False,
                agent=chat_engine.orchestrator.current_agent_name,
                error=result.get("error"),
            )
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/history")
async def get_history(limit: Optional[int] = 50):
    """
    Get conversation history
    
    Args:
        limit: Maximum number of messages
    
    Returns:
        Conversation history
    """
    try:
        history = chat_engine.get_conversation_history(limit=limit)
        return {"success": True, "history": history, "count": len(history)}
    except Exception as e:
        logger.error(f"History endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/chat/history")
async def clear_history():
    """
    Clear conversation history
    
    Returns:
        Status
    """
    try:
        result = chat_engine.clear_history()
        return result
    except Exception as e:
        logger.error(f"Clear history error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/session")
async def get_session():
    """
    Get session information
    
    Returns:
        Session info
    """
    try:
        session_info = chat_engine.get_session_info()
        return {"success": True, "session": session_info}
    except Exception as e:
        logger.error(f"Session endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Agent Routes
# ============================================================================

@app.get("/agents")
async def list_agents():
    """
    List all available agents
    
    Returns:
        List of agents
    """
    try:
        agents = chat_engine.list_agents()
        return {"success": True, "agents": agents}
    except Exception as e:
        logger.error(f"List agents error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/current")
async def get_current_agent():
    """
    Get current agent information
    
    Returns:
        Current agent info
    """
    try:
        agent_info = chat_engine.orchestrator.get_current_agent_info()
        return {"success": True, "agent": agent_info}
    except Exception as e:
        logger.error(f"Get current agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agents/switch")
async def switch_agent(request: AgentSwitchRequest):
    """
    Switch to different agent
    
    Args:
        request: Agent switch request
    
    Returns:
        Status
    """
    try:
        result = chat_engine.switch_agent(request.agent)
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=404, detail=result["error"])
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Switch agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/{agent_name}")
async def get_agent_info(agent_name: str):
    """
    Get specific agent information
    
    Args:
        agent_name: Agent name
    
    Returns:
        Agent info
    """
    try:
        agents = chat_engine.list_agents()
        agent_name = agent_name.lower()
        
        if agent_name in agents:
            return {"success": True, "agent": agents[agent_name]}
        else:
            raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get agent info error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# WebSocket Routes (Optional)
# ============================================================================

if settings.websocket_enabled:
    @app.websocket("/ws/chat")
    async def websocket_chat(websocket: WebSocket):
        """
        WebSocket endpoint for real-time chat
        
        Args:
            websocket: WebSocket connection
        """
        await websocket.accept()
        try:
            while True:
                # Receive message
                data = await websocket.receive_json()
                message = data.get("message")
                agent = data.get("agent")
                
                if not message:
                    await websocket.send_json({
                        "error": "No message provided"
                    })
                    continue
                
                # Process message
                if agent:
                    chat_engine.switch_agent(agent)
                
                result = chat_engine.process_message(message)
                
                # Send response
                await websocket.send_json({
                    "success": result["success"],
                    "response": result.get("response"),
                    "agent": result.get("agent"),
                    "error": result.get("error"),
                })
        except WebSocketDisconnect:
            logger.info("WebSocket disconnected")
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            try:
                await websocket.send_json({"error": str(e)})
            except:
                pass

# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
        },
    )

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers,
        reload=settings.api_reload,
    )
