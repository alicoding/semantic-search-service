#!/usr/bin/env python3
"""
Cache Resource Manager - Native LlamaIndex IngestionPipeline Caching (2025)
Single Responsibility: Provide native LlamaIndex caching following 95/5 principle
Pattern: Framework handles 95% of caching, we provide 5% configuration only
"""

from llama_index.storage.kvstore.redis import RedisKVStore
from llama_index.core.ingestion import IngestionCache
from typing import Optional
from .config_manager import get_config_resource


class CacheResourceManager:
    """
    Cache resource manager using native LlamaIndex IngestionPipeline patterns (2025)
    95/5 Pattern: LlamaIndex handles cache lifecycle, we provide configuration only
    """
    
    def __init__(self):
        """Initialize with minimal config - LlamaIndex 2025 pattern"""
        config = get_config_resource().config
        self.redis_host = config.redis_host
        self.redis_port = config.redis_port
        self.enabled = True
    
    def get_ingestion_cache(self, collection: str = "default_cache") -> Optional[IngestionCache]:
        """
        Get native LlamaIndex IngestionCache - TRUE 95/5 pattern
        Framework handles: connection, serialization, lifecycle, TTL, eviction
        We handle: configuration only (5%)
        """
        if not self.enabled:
            return None
            
        try:
            # Native LlamaIndex one-liner - framework does 95% of work
            redis_store = RedisKVStore.from_host_and_port(
                host=self.redis_host,
                port=self.redis_port
            )
            return IngestionCache(cache=redis_store, collection=collection)
        except Exception as e:
            print(f"Redis cache unavailable: {e}. Using no cache.")
            self.enabled = False
            return None


    def get_query_cache(self, collection: str = "query_cache") -> Optional[IngestionCache]:
        """
        Get query-specific cache using same native pattern
        LlamaIndex 2025: Use IngestionCache for all caching needs (95/5 principle)
        """
        return self.get_ingestion_cache(collection)


# Global cache manager instance (singleton pattern)
_cache_manager = None

def get_cache_manager() -> CacheResourceManager:
    """Get global cache resource manager (singleton)"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheResourceManager()
    return _cache_manager