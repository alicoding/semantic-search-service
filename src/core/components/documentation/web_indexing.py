#!/usr/bin/env python3
"""
Web Indexing Component - Documentation Domain Micro-Component
Single Responsibility: Index web content using Spider crawler and various sources
Pattern: 60-80 LOC focused component with proper DI
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from ...resources import get_intelligence_resource, IntelligenceResourceManager
from ...resources.cache_manager import get_cache_manager, CacheResourceManager


class WebIndexingComponent:
    """
    Web indexing using Spider crawler and various sources
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

    def index_web_docs(self, framework: str, docs_url: str, spider_key: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Index from web using Spider crawler"""
        try:
            from llama_index.readers.web import SpiderWebReader
            
            spider = SpiderWebReader(
                api_key=spider_key,
                mode="crawl",
                params={"depth": config.get('crawl_depth', 3)}
            )
            
            docs = spider.load_data(url=docs_url)
            if not docs:
                return {"error": "No documents retrieved from URL"}
            
            # Create index using shared client
            collection_name = f"docs_{framework}"
            client = self.intelligence.intelligence.client
            
            index = VectorStoreIndex.from_documents(
                docs,
                storage_context=StorageContext.from_defaults(
                    vector_store=QdrantVectorStore(
                        client=client,
                        collection_name=collection_name,
                        enable_hybrid=True
                    )
                ),
                show_progress=True
            )
            
            # Save index for offline use
            index.storage_context.persist(f"indexes/{framework}")
            
            return {
                "indexed": len(docs),
                "framework": framework, 
                "collection": collection_name,
                "source": "web"
            }
            
        except ImportError:
            return {"error": "SpiderWebReader not installed. Run: pip install llama-index-readers-web"}
        except Exception as e:
            return {"error": f"Failed to crawl documentation: {str(e)}"}

    def index_temp_docs(self, framework: str) -> Dict[str, Any]:
        """Fallback to temp_docs if available"""
        temp_docs_path = Path("temp_docs") / framework
        if temp_docs_path.exists():
            result = self.intelligence.intelligence.index_project(str(temp_docs_path), f"docs_{framework}")
            return result
        
        return {
            "error": "No documentation source available. Provide URL with Spider API key or local docs"
        }


# Component factory for easy instantiation
def create_web_indexing() -> WebIndexingComponent:
    """Create web indexing component with shared resources (proper DI)"""
    return WebIndexingComponent()