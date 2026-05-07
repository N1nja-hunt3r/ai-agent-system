"""
Memory Management System
Handles short-term and long-term memory
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import deque
import json
import sqlite3
from pathlib import Path
from src.config import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class MemoryManager:
    """Manage agent memory (short-term and long-term)"""
    
    def __init__(self, max_short_term: int = 100):
        """
        Initialize memory manager
        
        Args:
            max_short_term: Maximum short-term memory size
        """
        self.short_term_memory = deque(maxlen=max_short_term)
        self.db_path = Path(settings.data_dir) / "memory.db"
        
        # Ensure data directory exists
        Path(settings.data_dir).mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._init_database()
        
        logger.info(f"MemoryManager initialized - db: {self.db_path}")
    
    def _init_database(self) -> None:
        """Initialize SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create memories table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    metadata TEXT,
                    importance REAL DEFAULT 0.5
                )
            """)
            
            # Create indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_type ON memories(type)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)
            """)
            
            conn.commit()
            conn.close()
            logger.info("Memory database initialized")
        except Exception as e:
            logger.error(f"Failed to initialize memory database: {e}")
            raise
    
    def add_short_term_memory(
        self,
        content: str,
        memory_type: str = "interaction",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Add to short-term memory
        
        Args:
            content: Memory content
            memory_type: Type of memory
            metadata: Additional metadata
        """
        memory = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": memory_type,
            "content": content,
            "metadata": metadata or {},
        }
        self.short_term_memory.append(memory)
        logger.debug(f"Added to short-term memory: {memory_type}")
    
    def add_long_term_memory(
        self,
        content: str,
        memory_type: str = "interaction",
        importance: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Add to long-term memory (persistent)
        
        Args:
            content: Memory content
            memory_type: Type of memory
            importance: Importance score (0-1)
            metadata: Additional metadata
        
        Returns:
            True if successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO memories (type, content, metadata, importance)
                VALUES (?, ?, ?, ?)
            """, (
                memory_type,
                content,
                json.dumps(metadata or {}),
                importance,
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Added to long-term memory: {memory_type}")
            return True
        except Exception as e:
            logger.error(f"Failed to add long-term memory: {e}")
            return False
    
    def get_short_term_memory(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get short-term memory
        
        Args:
            limit: Maximum number of memories to return
        
        Returns:
            List of memories
        """
        memories = list(self.short_term_memory)
        if limit:
            memories = memories[-limit:]
        return memories
    
    def get_long_term_memory(
        self,
        memory_type: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Get long-term memory
        
        Args:
            memory_type: Filter by type
            limit: Maximum number of memories
        
        Returns:
            List of memories
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if memory_type:
                cursor.execute("""
                    SELECT id, timestamp, type, content, metadata, importance
                    FROM memories
                    WHERE type = ?
                    ORDER BY importance DESC, timestamp DESC
                    LIMIT ?
                """, (memory_type, limit))
            else:
                cursor.execute("""
                    SELECT id, timestamp, type, content, metadata, importance
                    FROM memories
                    ORDER BY importance DESC, timestamp DESC
                    LIMIT ?
                """, (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            memories = []
            for row in rows:
                memories.append({
                    "id": row[0],
                    "timestamp": row[1],
                    "type": row[2],
                    "content": row[3],
                    "metadata": json.loads(row[4]),
                    "importance": row[5],
                })
            
            return memories
        except Exception as e:
            logger.error(f"Failed to retrieve long-term memory: {e}")
            return []
    
    def search_memory(
        self,
        query: str,
        search_type: str = "both",
    ) -> List[Dict[str, Any]]:
        """
        Search memory
        
        Args:
            query: Search query
            search_type: "short", "long", or "both"
        
        Returns:
            List of matching memories
        """
        results = []
        
        # Search short-term
        if search_type in ["short", "both"]:
            for memory in self.short_term_memory:
                if query.lower() in memory["content"].lower():
                    results.append(memory)
        
        # Search long-term
        if search_type in ["long", "both"]:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, timestamp, type, content, metadata, importance
                    FROM memories
                    WHERE content LIKE ?
                    ORDER BY timestamp DESC
                """, (f"%{query}%",))
                
                rows = cursor.fetchall()
                conn.close()
                
                for row in rows:
                    results.append({
                        "id": row[0],
                        "timestamp": row[1],
                        "type": row[2],
                        "content": row[3],
                        "metadata": json.loads(row[4]),
                        "importance": row[5],
                    })
            except Exception as e:
                logger.error(f"Long-term search failed: {e}")
        
        return results
    
    def clear_short_term_memory(self) -> None:
        """Clear short-term memory"""
        self.short_term_memory.clear()
        logger.info("Short-term memory cleared")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM memories")
            total = cursor.fetchone()[0]
            
            cursor.execute("SELECT type, COUNT(*) FROM memories GROUP BY type")
            by_type = dict(cursor.fetchall())
            
            conn.close()
            
            return {
                "short_term_size": len(self.short_term_memory),
                "long_term_total": total,
                "by_type": by_type,
            }
        except Exception as e:
            logger.error(f"Failed to get memory stats: {e}")
            return {}
