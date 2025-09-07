#!/usr/bin/env python3
"""
URL Indexing Component - Documentation Domain Micro-Component
Single Responsibility: Index web content from URLs using native LlamaIndex patterns
Pattern: 40-60 LOC focused component with proper DI
"""

from typing import Dict, Any, Optional
from llama_index.core import VectorStoreIndex
from ...resources import get_intelligence_resource, IntelligenceResourceManager
from ...resources.cache_manager import get_cache_manager, CacheResourceManager


class URLIndexingComponent:
    """
    URL indexing using native LlamaIndex patterns
    Component Pattern: Small, focused, resource-injected
    """
    
    def __init__(self, 
                 intelligence_resource: Optional[IntelligenceResourceManager] = None,
                 cache_resource: Optional[CacheResourceManager] = None):
        """
        Initialize with shared resource managers (proper DI pattern)
        Uses singletons if none provided (prevents duplicate resources)
        """
        self.intelligence = intelligence_resource or get_intelligence_resource()
        self.cache = cache_resource or get_cache_manager()

    def index_url_native(self, url: str, collection_name: str) -> Dict[str, Any]:
        """
        TRUE 95/5 Pattern: Native LlamaIndex URL indexing (5 lines total)
        SimpleWebPageReader + VectorStoreIndex.from_documents = one-liner pattern
        """
        try:
            from llama_index.readers.web import SimpleWebPageReader
            
            # NATIVE LLAMAINDEX ONE-LINER (2025 pattern)
            documents = SimpleWebPageReader().load_data([url])
            index = VectorStoreIndex.from_documents(documents, show_progress=True)
            
            # NATIVE PERSISTENCE
            persist_dir = f"./storage/docs_{collection_name}"
            index.storage_context.persist(persist_dir=persist_dir)
            
            return {
                "success": True,
                "indexed": True,
                "docs_count": len(documents),
                "collection": collection_name,
                "url": url,
                "persist_dir": persist_dir,
                "ready_for_qa": True
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}


# Component factory for easy instantiation
def create_url_indexing() -> URLIndexingComponent:
    """Create URL indexing component with shared resources (proper DI)"""
    return URLIndexingComponent()