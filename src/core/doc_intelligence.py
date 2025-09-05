#!/usr/bin/env python3
"""
Documentation Intelligence System
Provides precise documentation snippets to prevent AI agents from guessing
Accessible via CLI, REST API, and MCP tools
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.vector_stores.qdrant import QdrantVectorStore
from .config import get_qdrant_client, CONFIG
from .semantic_search import index_project

class DocIntelligence:
    """
    Single source of truth for documentation intelligence
    Used by CLI, API, and MCP interfaces
    """
    
    def __init__(self):
        self.client = get_qdrant_client()
        self.doc_config = CONFIG.get('documentation', {})
        self.index_config = CONFIG.get('indexing', {})
        
    def index_framework(self, framework: str, docs_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Index framework documentation
        Can use web crawler (Spider) or local files
        """
        # Check if offline mode
        if self.doc_config.get('offline_mode', False):
            # Use local documentation
            offline_path = Path(self.doc_config.get('offline_docs_path', './offline_docs'))
            docs_path = offline_path / framework
            
            if not docs_path.exists():
                return {"error": f"Offline docs not found at {docs_path}"}
            
            # Use existing index_project with config-driven settings
            return index_project(str(docs_path), f"docs_{framework}")
        
        # Check for Spider API key for web crawling
        spider_key = os.getenv("SPIDER_API_KEY") or CONFIG.get('spider_api_key')
        
        if spider_key and docs_url:
            try:
                from llama_index.readers.web import SpiderWebReader
                
                spider = SpiderWebReader(
                    api_key=spider_key,
                    mode="crawl",  # Recursive crawling
                    params={"depth": CONFIG.get('crawl_depth', 3)}
                )
                
                docs = spider.load_data(url=docs_url)
                
                if not docs:
                    return {"error": "No documents retrieved from URL"}
                
                # Create index
                collection_name = f"docs_{framework}"
                index = VectorStoreIndex.from_documents(
                    docs,
                    storage_context=StorageContext.from_defaults(
                        vector_store=QdrantVectorStore(
                            client=self.client, 
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
        
        # Fallback to temp_docs if available
        temp_docs_path = Path("temp_docs") / framework
        if temp_docs_path.exists():
            return index_project(str(temp_docs_path), f"docs_{framework}")
        
        return {
            "error": "No documentation source available. Provide URL with Spider API key or local docs"
        }
    
    def search_pattern(self, query: str, framework: str = "llamaindex") -> str:
        """
        Get precise implementation pattern (200-500 tokens)
        This is what prevents AI from guessing method names
        """
        # Import cache here to avoid circular import
        from .redis_cache import query_cache
        
        collection_name = f"docs_{framework}"
        
        # Try cache first
        cached = query_cache.get(query, collection_name)
        if cached is not None:
            return cached
        
        # Check routing strategy
        routing = self.doc_config.get('routing', {})
        route_to = routing.get(framework, routing.get('default', 'indexed'))
        
        if route_to == "context7":
            # Use Context7 (if available)
            return self._use_context7(query, framework)
        elif route_to == "web":
            # Use web search
            return self._web_search(query, framework)
        
        # Default: use indexed documentation
        try:
            # Check if collection exists
            if not self.client.collection_exists(collection_name):
                return (f"Framework '{framework}' not indexed. "
                       f"Run: semantic-search docs index {framework}")
            
            # Load index from vector store
            vector_store = QdrantVectorStore(
                client=self.client,
                collection_name=collection_name
            )
            index = VectorStoreIndex.from_vector_store(vector_store)
            
            # Create query engine with compact responses
            engine = index.as_query_engine(
                similarity_top_k=2,  # Get top 2 most relevant chunks
                response_mode="compact",  # Concise synthesis
                streaming=False
            )
            
            # Enhance query for better code pattern retrieval
            enhanced_query = f"{query} show code example implementation pattern syntax"
            
            # Get response
            response = engine.query(enhanced_query)
            
            # Limit to ~500 tokens (roughly 2000 chars)
            result = str(response.response)
            if len(result) > 2000:
                result = result[:2000] + "..."
            
            # Cache the result
            query_cache.set(query, collection_name, result)
            
            return result
            
        except Exception as e:
            return f"Error searching {framework} docs: {str(e)}"
    
    def check_exists(self, component: str, framework: str = "llamaindex") -> Dict[str, Any]:
        """
        Fast existence check for components/functions/classes
        Used by task-enforcer to know if something already exists
        """
        collection_name = f"docs_{framework}"
        
        if not self.client.collection_exists(collection_name):
            return {
                "exists": False,
                "error": f"Framework '{framework}' not indexed"
            }
        
        try:
            vector_store = QdrantVectorStore(
                client=self.client,
                collection_name=collection_name
            )
            index = VectorStoreIndex.from_vector_store(vector_store)
            
            # Use retriever for fast checking
            retriever = index.as_retriever(similarity_top_k=1)
            nodes = retriever.retrieve(component)
            
            if nodes and nodes[0].score > 0.7:  # Confidence threshold
                return {
                    "exists": True,
                    "confidence": nodes[0].score,
                    "context": nodes[0].text[:500],
                    "framework": framework
                }
            
            return {
                "exists": False,
                "framework": framework,
                "message": f"Component '{component}' not found in {framework} docs"
            }
            
        except Exception as e:
            return {
                "exists": False,
                "error": str(e)
            }
    
    def refresh_docs(self, framework: str) -> Dict[str, Any]:
        """
        Refresh documentation using native LlamaIndex patterns
        Re-indexes only changed documents
        """
        # Get framework config
        auto_index = self.doc_config.get('auto_index', {})
        framework_config = auto_index.get(framework, {})
        
        if not framework_config.get('enabled', False):
            return {"error": f"Framework '{framework}' not enabled for indexing"}
        
        docs_url = framework_config.get('url')
        if not docs_url:
            return {"error": f"No URL configured for framework '{framework}'"}
        
        # Re-index the framework
        return self.index_framework(framework, docs_url)
    
    def list_frameworks(self) -> List[str]:
        """List all indexed documentation frameworks"""
        collections = [c.name for c in self.client.get_collections().collections]
        return [c.replace('docs_', '') for c in collections if c.startswith('docs_')]
    
    def get_framework_info(self, framework: str) -> Dict[str, Any]:
        """Get information about an indexed framework"""
        collection_name = f"docs_{framework}"
        
        if not self.client.collection_exists(collection_name):
            return {
                "framework": framework,
                "indexed": False,
                "error": "Not indexed"
            }
        
        collection = self.client.get_collection(collection_name)
        return {
            "framework": framework,
            "indexed": True,
            "documents": collection.points_count,
            "collection": collection_name
        }
    
    def _use_context7(self, query: str, framework: str) -> str:
        """Fallback to Context7 using native doc_search routing"""
        from .doc_search import search_docs
        # Route through doc_search which has Context7 integration
        return search_docs(query, framework)
    
    def _web_search(self, query: str, framework: str) -> str:
        """Fallback to web search"""
        # Could use WebFetch or other web search
        return f"Web search not yet implemented. Please index {framework} locally."

# Global instance shared across all interfaces
_doc_intelligence = None

def get_doc_intelligence() -> DocIntelligence:
    """Get or create the global DocIntelligence instance"""
    global _doc_intelligence
    if _doc_intelligence is None:
        _doc_intelligence = DocIntelligence()
    return _doc_intelligence