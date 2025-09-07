#!/usr/bin/env python3
"""
Graph Index Strategy Implementation  
Single Responsibility: Handle PropertyGraphIndex operations only
"""

from typing import List
from llama_index.core import StorageContext, Document
from llama_index.core.indices.property_graph import PropertyGraphIndex
from llama_index.core.indices.property_graph import ImplicitPathExtractor
from llama_index.core.graph_stores import SimplePropertyGraphStore
from llama_index.vector_stores.qdrant import QdrantVectorStore

from .base import IndexStrategy
from ..config import get_qdrant_client, CONFIG


class GraphIndexStrategy(IndexStrategy):
    """Strategy for creating PropertyGraphIndex"""
    
    def __init__(self, client=None):
        self.client = client or get_qdrant_client()
        self._graph_stores = {}
    
    def create_index(self, documents: List[Document], collection_name: str) -> PropertyGraphIndex:
        """Create PropertyGraphIndex with schema extraction"""
        if collection_name not in self._graph_stores:
            self._graph_stores[collection_name] = SimplePropertyGraphStore()
        
        storage_context = StorageContext.from_defaults(
            vector_store=QdrantVectorStore(
                client=self.client,
                collection_name=collection_name
            ),
            property_graph_store=self._graph_stores[collection_name]
        )
        
        return PropertyGraphIndex.from_documents(
            documents=documents,
            storage_context=storage_context,
            kg_extractors=[ImplicitPathExtractor()],
            show_progress=True
        )
    
    def get_index(self, collection_name: str) -> PropertyGraphIndex:
        """Get existing PropertyGraphIndex"""
        if collection_name not in self._graph_stores:
            self._graph_stores[collection_name] = SimplePropertyGraphStore()
        
        storage_context = StorageContext.from_defaults(
            vector_store=QdrantVectorStore(client=self.client, collection_name=collection_name),
            property_graph_store=self._graph_stores[collection_name]
        )
        
        return PropertyGraphIndex(nodes=[], storage_context=storage_context)