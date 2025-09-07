#!/usr/bin/env python3
"""
Vector Index Strategy Implementation
Single Responsibility: Handle VectorStoreIndex operations only
"""

from typing import List
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core import Document
from llama_index.vector_stores.qdrant import QdrantVectorStore

from .base import IndexStrategy
from ..config import get_qdrant_client, CONFIG


class VectorIndexStrategy(IndexStrategy):
    """Strategy for creating VectorStoreIndex"""
    
    def __init__(self, client=None):
        self.client = client or get_qdrant_client()
    
    def create_index(self, documents: List[Document], collection_name: str) -> VectorStoreIndex:
        """Create VectorStoreIndex with optimized settings"""
        vector_store_kwargs = {
            'client': self.client,
            'collection_name': collection_name
        }
        if CONFIG.get('enable_hybrid', False):
            vector_store_kwargs['enable_hybrid'] = True
        
        storage_context = StorageContext.from_defaults(
            vector_store=QdrantVectorStore(**vector_store_kwargs)
        )
        
        return VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            show_progress=True
        )
    
    def get_index(self, collection_name: str) -> VectorStoreIndex:
        """Get existing VectorStoreIndex"""
        vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=collection_name
        )
        return VectorStoreIndex.from_vector_store(vector_store)