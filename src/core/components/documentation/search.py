#!/usr/bin/env python3
"""
Documentation Search Component - Documentation Domain Micro-Component  
Single Responsibility: Search indexed documentation for precise patterns
Pattern: 50-80 LOC component with injected shared resources (no duplicate API calls)
"""

from typing import Dict, Any, Optional
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.vector_stores.qdrant import QdrantVectorStore
from ...resources import get_intelligence_resource, IntelligenceResourceManager
from ...resources.cache_manager import get_cache_manager, CacheResourceManager


class DocumentationSearchComponent:
    """
    Documentation search using shared resources
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
        self.query_cache = self.cache.get_query_cache()  # Available to all methods
    
    def search_pattern(self, query: str, framework: str = "llamaindex", config: Dict[str, Any] = None) -> str:
        """
        Get precise implementation pattern using shared intelligence resource
        No duplicate API calls - uses centralized resource manager
        """
        config = config or {}
        collection_name = f"docs_{framework}"
        
        # Try cache first using injected cache resource
        cached = self.query_cache.get(query, collection_name)
        if cached is not None:
            return cached
        
        # Check routing strategy
        routing = config.get('routing', {})
        route_to = routing.get(framework, routing.get('default', 'indexed'))
        
        if route_to == "context7":
            return self._use_context7(query, framework)
        elif route_to == "web":
            return self._web_search(query, framework)
        
        # Default: use indexed documentation with shared client
        return self._search_indexed(query, framework, collection_name)
    
    def query_native_docs(self, collection_name: str, query: str) -> Dict[str, Any]:
        """
        TRUE 95/5 Pattern: Native LlamaIndex cached index query (3 lines total)
        load_index_from_storage + as_query_engine + query = one-liner pattern
        """
        try:
            # NATIVE CACHED INDEX LOADING - 95/5 Principle
            persist_dir = f"./storage/docs_{collection_name}"
            storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
            index = load_index_from_storage(storage_context)
            
            # NATIVE QUERY ENGINE
            query_engine = index.as_query_engine()
            response = query_engine.query(query)
            
            return {
                "success": True,
                "collection": collection_name,
                "query": query,
                "answer": str(response),
                "ready": True
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _search_indexed(self, query: str, framework: str, collection_name: str) -> str:
        """Search indexed documentation using shared resources"""
        try:
            client = self.intelligence.intelligence.client
            
            # Check if collection exists
            if not client.collection_exists(collection_name):
                return (f"Framework '{framework}' not indexed. "
                       f"Run: semantic-search docs index {framework}")
            
            # Load index from vector store
            vector_store = QdrantVectorStore(client=client, collection_name=collection_name)
            index = VectorStoreIndex.from_vector_store(vector_store)
            
            # Create query engine with compact responses
            engine = index.as_query_engine(
                similarity_top_k=2,
                response_mode="compact",
                streaming=False
            )
            
            # Enhance query for better code pattern retrieval
            enhanced_query = f"{query} show code example implementation pattern syntax"
            response = engine.query(enhanced_query)
            
            # Limit to ~500 tokens (roughly 2000 chars)
            result = str(response.response)
            if len(result) > 2000:
                result = result[:2000] + "..."
            
            # Cache the result using injected cache resource
            self.query_cache.set(query, collection_name, result)
            
            return result
            
        except Exception as e:
            return f"Error searching {framework} docs: {str(e)}"
    
    def _use_context7(self, query: str, framework: str) -> str:
        """Fallback to Context7 using native doc_search routing"""
        from ...doc_search import search_docs
        return search_docs(query, framework)
    
    def _web_search(self, query: str, framework: str) -> str:
        """Fallback to web search"""
        return f"Web search not yet implemented. Please index {framework} locally."


# Component factory for easy instantiation
def create_documentation_search() -> DocumentationSearchComponent:
    """Create documentation search component with shared resources (proper DI)"""
    return DocumentationSearchComponent()