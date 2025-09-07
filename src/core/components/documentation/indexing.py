#!/usr/bin/env python3
"""
Documentation Indexing Coordinator - Documentation Domain Component
Single Responsibility: Coordinate different indexing strategies using focused components
Pattern: 50-80 LOC coordinator using composition pattern with proper DI
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from ...resources import get_intelligence_resource, IntelligenceResourceManager
from ...resources.cache_manager import get_cache_manager, CacheResourceManager
from .url_indexing import create_url_indexing
from .github_indexing import create_github_indexing
from .web_indexing import create_web_indexing
from .workflow_indexing import create_workflow_indexing


class DocumentationIndexingComponent:
    """
    Documentation indexing coordinator using composition of focused components
    Component Pattern: Coordinator with proper DI, delegates to specialized components
    """
    
    def __init__(self, 
                 intelligence_resource: Optional[IntelligenceResourceManager] = None,
                 cache_resource: Optional[CacheResourceManager] = None):
        """
        Initialize with shared resource managers and specialized components
        Uses singletons if none provided (prevents duplicate resources)
        """
        self.intelligence = intelligence_resource or get_intelligence_resource()
        self.cache = cache_resource or get_cache_manager()
        
        # Composition: Use focused components for different indexing types
        self.url_indexer = create_url_indexing()
        self.github_indexer = create_github_indexing()
        self.web_indexer = create_web_indexing()
        self.workflow_indexer = create_workflow_indexing()
    
    def index_framework(self, framework: str, docs_url: Optional[str] = None, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Index framework documentation using shared intelligence resource
        No duplicate API calls - uses centralized resource manager
        """
        config = config or {}
        
        # Check if offline mode
        if config.get('offline_mode', False):
            return self._index_offline_docs(framework, config)
        
        # Web crawling with Spider
        spider_key = os.getenv("SPIDER_API_KEY") or config.get('spider_api_key')
        if spider_key and docs_url:
            return self.web_indexer.index_web_docs(framework, docs_url, spider_key, config)
        
        # Fallback to temp_docs
        return self.web_indexer.index_temp_docs(framework)
    
    def _index_offline_docs(self, framework: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Index from offline documentation"""
        offline_path = Path(config.get('offline_docs_path', './offline_docs'))
        docs_path = offline_path / framework
        
        if not docs_path.exists():
            return {"error": f"Offline docs not found at {docs_path}"}
        
        # Use shared intelligence to index
        result = self.intelligence.intelligence.index_project(str(docs_path), f"docs_{framework}")
        return result
    
    def index_url_native(self, url: str, collection_name: str) -> Dict[str, Any]:
        """Delegate URL indexing to focused component"""
        return self.url_indexer.index_url_native(url, collection_name)

    def index_github_native(self, repo: str, collection_name: str) -> Dict[str, Any]:
        """Delegate GitHub indexing to focused component"""
        return self.github_indexer.index_github_native(repo, collection_name)

    def index_with_workflow(self, source_config: Dict[str, Any]) -> Dict[str, Any]:
        """2025 Pattern: Declarative workflow-based document processing"""
        return self.workflow_indexer.create_document_pipeline(source_config)



# Component factory for easy instantiation
def create_documentation_indexing() -> DocumentationIndexingComponent:
    """Create documentation indexing component with shared resources"""
    return DocumentationIndexingComponent()