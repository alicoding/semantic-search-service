#!/usr/bin/env python3
"""
GitHub Indexing Component - Documentation Domain Micro-Component
Single Responsibility: Index GitHub repository content using native LlamaIndex patterns
Pattern: 50-70 LOC focused component with proper DI
"""

from typing import Dict, Any, Optional
from llama_index.core import VectorStoreIndex
from ...resources import get_intelligence_resource, IntelligenceResourceManager
from ...resources.cache_manager import get_cache_manager, CacheResourceManager


class GitHubIndexingComponent:
    """
    GitHub repository indexing using native LlamaIndex patterns
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

    def index_github_native(self, repo: str, collection_name: str) -> Dict[str, Any]:
        """
        TRUE 95/5 Pattern: Native GitHub repository indexing
        GitHubRepositoryReader + VectorStoreIndex.from_documents = one-liner pattern
        """
        try:
            from llama_index.readers.github import GitHubRepositoryReader
            
            # Native GitHub reader
            owner, repo_name = repo.split('/')
            reader = GitHubRepositoryReader(
                github_token=None,  # Public repos
                owner=owner,
                repo=repo_name,
                filter_directories=[["docs"], ["documentation"], ["doc"]]
            )
            
            # Try main branch first, then master
            documents = reader.load_data(branch="main")
            if not documents:
                documents = reader.load_data(branch="master")
                
            if not documents:
                return {"success": False, "error": "No documents found in repository"}
            
            # NATIVE INDEXING
            index = VectorStoreIndex.from_documents(documents, show_progress=True)
            
            # NATIVE PERSISTENCE
            persist_dir = f"./storage/docs_{collection_name}"
            index.storage_context.persist(persist_dir=persist_dir)
            
            return {
                "success": True,
                "indexed": True,
                "docs_count": len(documents),
                "collection": f"docs_{collection_name}",
                "repo": repo,
                "persist_dir": persist_dir
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}


# Component factory for easy instantiation
def create_github_indexing() -> GitHubIndexingComponent:
    """Create GitHub indexing component with shared resources (proper DI)"""
    return GitHubIndexingComponent()