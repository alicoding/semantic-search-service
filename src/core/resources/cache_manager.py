#!/usr/bin/env python3
"""
Cache Resource Manager - Native LlamaIndex Redis Caching
Single Responsibility: Manage all caching operations with native LlamaIndex patterns
Pattern: 50-80 LOC resource manager using verified RedisKVStore patterns
"""

from llama_index.storage.kvstore.redis import RedisKVStore
from llama_index.core.ingestion import IngestionCache
import hashlib
import json
from typing import Any, Optional
from .config_manager import get_config_resource


class CacheResourceManager:
    """
    Cache resource manager using native LlamaIndex RedisKVStore
    Resource Pattern: Centralized cache management with fallback
    """
    
    def __init__(self):
        """Initialize with config from config manager"""
        config = get_config_resource().config
        self.redis_host = config.get('redis_host', 'localhost')
        self.redis_port = config.get('redis_port', 6380)
        self.redis_ttl = config.get('cache_ttl', 3600)
        self._store = None
        self.enabled = True
    
    def get_redis_store(self) -> Optional[RedisKVStore]:
        """Get native LlamaIndex RedisKVStore - VERIFIED pattern"""
        if self._store is None:
            try:
                self._store = RedisKVStore.from_host_and_port(
                    host=self.redis_host,
                    port=self.redis_port
                )
                # Test connection
                self._store.get("__test__")
            except Exception as e:
                print(f"Redis connection failed: {e}. Caching disabled.")
                self.enabled = False
                return None
        return self._store
    
    def get_query_cache(self):
        """Get query cache instance"""
        return QueryCache(self.get_redis_store(), self.enabled)
    
    def get_ingestion_cache(self, collection: str = "ingestion_cache") -> Optional[IngestionCache]:
        """Get native IngestionCache for pipeline caching - VERIFIED pattern"""
        store = self.get_redis_store()
        if store is None:
            return None
        return IngestionCache(cache=store, collection=collection)


class QueryCache:
    """Query caching using native RedisKVStore"""
    
    def __init__(self, store: Optional[RedisKVStore], enabled: bool = True):
        self.store = store
        self.enabled = enabled and store is not None
    
    def _make_key(self, query: str) -> str:
        """Create cache key from query"""
        return hashlib.md5(query.encode()).hexdigest()
    
    def get(self, query: str, collection: str = "default") -> Optional[str]:
        """Get cached query result"""
        if not self.enabled:
            return None
        try:
            key = self._make_key(query)
            result = self.store.get(key, collection=collection)
            return json.loads(result) if result else None
        except:
            return None
    
    def set(self, query: str, collection: str, result: str, ttl: Optional[int] = None) -> bool:
        """Set cached query result"""
        if not self.enabled:
            return False
        try:
            key = self._make_key(query)
            self.store.put(key, json.dumps(result), collection=collection)
            return True
        except:
            return False


# Global cache manager instance (singleton pattern)
_cache_manager = None

def get_cache_manager() -> CacheResourceManager:
    """Get global cache resource manager (singleton)"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheResourceManager()
    return _cache_manager