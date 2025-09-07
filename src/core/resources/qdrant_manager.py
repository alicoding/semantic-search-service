#!/usr/bin/env python3
"""
Qdrant Resource Manager - Centralized Resource Layer
Single Responsibility: Manage shared Qdrant client connections (prevent duplicate connections)
Pattern: Singleton resource manager for efficient Qdrant sharing across components
"""

from typing import Optional, Any
from qdrant_client import QdrantClient
from .config_manager import get_config_resource


class QdrantResourceManager:
    """
    Centralized Qdrant resource manager
    Prevents duplicate client connections by sharing single client instance
    """
    
    _instance: Optional['QdrantResourceManager'] = None
    _qdrant_client: Optional[QdrantClient] = None
    _async_qdrant_client: Optional[Any] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @property
    def client(self) -> QdrantClient:
        """Get shared Qdrant client (lazy initialization)"""
        if self._qdrant_client is None:
            config_manager = get_config_resource()
            self._qdrant_client = QdrantClient(url=config_manager.config.qdrant_url)
        return self._qdrant_client
    
    @property
    def async_client(self):
        """Get shared async Qdrant client (lazy initialization)"""
        if self._async_qdrant_client is None:
            try:
                from qdrant_client import AsyncQdrantClient
                config_manager = get_config_resource()
                self._async_qdrant_client = AsyncQdrantClient(url=config_manager.config.qdrant_url)
            except ImportError:
                # Fallback to sync client if async not available
                return self.client
        return self._async_qdrant_client
    
    def get_client(self) -> QdrantClient:
        """Get Qdrant client (backward compatibility method)"""
        return self.client
    
    def close_client(self):
        """Explicitly close Qdrant client - call on shutdown"""
        if self._qdrant_client is not None:
            try:
                self._qdrant_client.close()
            except Exception:
                pass  # Ignore errors on close
            self._qdrant_client = None
    
    def get_collection_name(self, project: str) -> str:
        """Get collection name with configured prefix using config resource"""
        config_manager = get_config_resource()
        return config_manager.get_collection_name(project)


# Global instance for component sharing
_qdrant_manager = QdrantResourceManager()

def get_qdrant_resource() -> QdrantResourceManager:
    """Get shared Qdrant resource manager"""
    return _qdrant_manager