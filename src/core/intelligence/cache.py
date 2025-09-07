#!/usr/bin/env python3
"""
Cache Strategy Implementation
Single Responsibility: Handle caching operations only
"""

from typing import Optional
from .base import CacheStrategy


class RedisCacheStrategy(CacheStrategy):
    """Redis-based caching strategy"""
    
    def get(self, key: str, namespace: str) -> Optional[str]:
        """Get from Redis cache"""
        from ..resources.cache_manager import get_cache_manager
        query_cache = get_cache_manager().get_query_cache()
        return query_cache.get(key, namespace)
    
    def set(self, key: str, namespace: str, value: str, ttl: int = 3600) -> None:
        """Set in Redis cache"""
        from ..resources.cache_manager import get_cache_manager
        query_cache = get_cache_manager().get_query_cache()
        query_cache.set(key, namespace, value, ttl)