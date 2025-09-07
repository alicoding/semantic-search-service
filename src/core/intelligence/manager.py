#!/usr/bin/env python3
"""
Intelligence Manager - Main Coordinator  
Single Responsibility: Coordinate all intelligence operations
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

from .types import IndexMode, CodebaseIntelligenceError
from .base import DocumentLoader, CacheStrategy
from .loader import DefaultDocumentLoader
from .cache import RedisCacheStrategy
from .vector_strategy import VectorIndexStrategy
from .graph_strategy import GraphIndexStrategy


class CodebaseIntelligence:
    """Main intelligence coordinator - uses strategy pattern for all operations"""
    
    def __init__(self, document_loader: DocumentLoader = None, cache_strategy: CacheStrategy = None):
        self.document_loader = document_loader or DefaultDocumentLoader()
        self.cache_strategy = cache_strategy or RedisCacheStrategy()
        
        from ..config import get_qdrant_client
        self.client = get_qdrant_client()
        
        self._vector_strategy = None
        self._graph_strategy = None
        self._index_cache = {}
    
    def _get_strategy(self, mode: IndexMode):
        """Get appropriate strategy (Factory pattern)"""
        if mode == IndexMode.VECTOR:
            if self._vector_strategy is None:
                self._vector_strategy = VectorIndexStrategy(self.client)
            return self._vector_strategy
        else:  # GRAPH or HYBRID
            if self._graph_strategy is None:
                self._graph_strategy = GraphIndexStrategy(self.client)
            return self._graph_strategy
    
    def project_exists(self, project_name: str) -> bool:
        """Check if project is indexed"""
        return self.client.collection_exists(project_name)
    
    def get_index(self, project_name: str, mode: IndexMode = IndexMode.VECTOR):
        """Get index for project"""
        if project_name in self._index_cache:
            return self._index_cache[project_name]["index"]
        
        strategy = self._get_strategy(mode)
        index = strategy.get_index(project_name)
        
        self._index_cache[project_name] = {"index": index, "mode": mode}
        return index
    
    def search_semantic(self, query: str, project_name: str, limit: int = 5) -> str:
        """Semantic search with caching"""
        cache_key = f"{query}:{limit}"
        cached = self.cache_strategy.get(cache_key, project_name)
        if cached:
            return cached
        
        index = self.get_index(project_name)
        result = str(index.as_query_engine(similarity_top_k=limit).query(query))
        
        self.cache_strategy.set(cache_key, project_name, result)
        return result
    
    def index_project(self, path: str, project_name: str, mode: IndexMode = IndexMode.VECTOR) -> Dict[str, Any]:
        """Index project from directory using native LlamaIndex methods"""
        try:
            documents = self.document_loader.load_documents(path)
            if not documents:
                return {"status": "error", "error": "No documents found", "project": project_name}
            
            strategy = self._get_strategy(mode)
            index = strategy.create_index(documents, project_name)
            
            # Cache the index
            self._index_cache[project_name] = {"index": index, "mode": mode}
            
            return {
                "status": "success",
                "project": project_name,
                "documents_indexed": len(documents),
                "mode": mode.value
            }
        except Exception as e:
            return {"status": "error", "error": str(e), "project": project_name}
    
    def list_projects(self) -> List[str]:
        """List all indexed projects using native Qdrant client"""
        collections = self.client.get_collections()
        return [c.name for c in collections.collections]
    
    def clear_project(self, project_name: str) -> bool:
        """Delete project collection using native Qdrant client"""
        try:
            self.client.delete_collection(project_name)
            # Remove from cache
            if project_name in self._index_cache:
                del self._index_cache[project_name]
            return True
        except Exception:
            return False
    
    def get_project_info(self, project_name: str) -> Dict[str, Any]:
        """Get project information using native Qdrant client"""
        if not self.project_exists(project_name):
            return {"indexed": False, "project": project_name}
        
        try:
            collection = self.client.get_collection(project_name)
            return {
                "indexed": True,
                "project": project_name,
                "documents": collection.points_count,
                "vector_size": collection.config.params.vectors.size if hasattr(collection.config.params, 'vectors') else None
            }
        except Exception as e:
            return {"indexed": True, "project": project_name, "error": str(e)}
    
    def refresh_project(self, path: str, project_name: str) -> Dict[str, Any]:
        """Refresh project with new documents using native LlamaIndex methods"""
        try:
            if not self.project_exists(project_name):
                return self.index_project(path, project_name)
            
            # Load new documents
            new_documents = self.document_loader.load_documents(path)
            if not new_documents:
                return {"status": "no_changes", "project": project_name}
            
            # Get existing index and add new documents
            index = self.get_index(project_name)
            from llama_index.core.node_parser import SimpleNodeParser
            parser = SimpleNodeParser()
            new_nodes = parser.get_nodes_from_documents(new_documents)
            
            # Use native add_nodes method
            index.insert_nodes(new_nodes)
            
            return {
                "status": "success", 
                "project": project_name,
                "documents_added": len(new_documents)
            }
        except Exception as e:
            return {"status": "error", "error": str(e), "project": project_name}
    
    def check_component_exists(self, component: str, project_name: str) -> Dict[str, Any]:
        """Check if component exists using semantic search"""
        if not self.project_exists(project_name):
            return {"exists": False, "error": f"Project '{project_name}' not indexed"}
        
        try:
            # Use semantic search to find component
            result = self.search_semantic(f"class {component} function {component} {component}", project_name, limit=1)
            
            # Simple heuristic: if result contains the component name, it likely exists
            exists = component.lower() in result.lower()
            
            return {
                "exists": exists,
                "project": project_name,
                "context": result[:200] + "..." if len(result) > 200 else result
            }
        except Exception as e:
            return {"exists": False, "error": str(e), "project": project_name}