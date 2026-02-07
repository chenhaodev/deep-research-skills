import sqlite3
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
from deep_research.api.models import Paper


class CacheManager:
    """SQLite-based cache for API responses to avoid redundant calls."""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS papers (
                paper_id TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                data_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    
    def get(self, paper_id: str) -> Optional[Paper]:
        """Retrieve paper from cache by ID.
        
        Args:
            paper_id: Unique identifier for the paper
            
        Returns:
            Paper object if found, None otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT data_json FROM papers WHERE paper_id = ?", (paper_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Paper.model_validate_json(row[0])
        return None
    
    def set(self, paper_id: str, paper: Paper, source: str):
        """Store paper in cache.
        
        Args:
            paper_id: Unique identifier for the paper
            paper: Paper object to cache
            source: Source of the data (e.g., 'semantic_scholar')
        """
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT OR REPLACE INTO papers (paper_id, source, data_json) VALUES (?, ?, ?)",
            (paper_id, source, paper.model_dump_json())
        )
        conn.commit()
        conn.close()
    
    def is_expired(self, paper_id: str, ttl_days: int) -> bool:
        """Check if cached paper is expired based on TTL.
        
        Args:
            paper_id: Unique identifier for the paper
            ttl_days: Time-to-live in days
            
        Returns:
            True if expired or not found, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT created_at FROM papers WHERE paper_id = ?", (paper_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return True
        
        created = datetime.fromisoformat(row[0])
        return datetime.now() - created > timedelta(days=ttl_days)
