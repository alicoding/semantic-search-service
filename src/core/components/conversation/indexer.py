#!/usr/bin/env python3
"""
Conversation Indexer Component - Conversation Domain Micro-Component
Single Responsibility: Index conversation documents using shared resources
Pattern: 50-80 LOC component with injected shared resources (FIXES DIP violation)
"""

from typing import Dict, Any, List, Optional
from llama_index.core import VectorStoreIndex, Document
from llama_index.vector_stores.qdrant import QdrantVectorStore
from ...resources import get_qdrant_resource, QdrantResourceManager


class ConversationIndexerComponent:
    """
    Conversation indexing using shared resources - FIXES DRY/DIP violations
    Component Pattern: Small, focused, resource-injected
    """
    
    def __init__(self, qdrant_resource: Optional[QdrantResourceManager] = None):
        """
        Initialize with shared resource manager - FIXES DIP violation
        Uses singleton if none provided (prevents duplicate resources)
        """
        self.qdrant = qdrant_resource or get_qdrant_resource()
    
    def index_documents(self, documents: List[Document], collection_name: str = "conversations") -> Dict[str, Any]:
        """
        Index conversation documents using shared Qdrant resource - FIXES DRY violation
        No duplicate API calls - uses centralized resource manager
        """
        if not documents:
            return {"error": "No documents provided for indexing"}
        
        try:
            # Use shared Qdrant client - ELIMINATES DRY violation
            client = self.qdrant.client
            vector_store = QdrantVectorStore(client=client, collection_name=collection_name)
            
            # Index documents with native LlamaIndex pattern
            index = VectorStoreIndex.from_documents(
                documents,
                vector_store=vector_store,
                show_progress=True
            )
            
            return {
                "indexed": True,
                "collection": collection_name,
                "documents": len(documents),
                "index_created": True
            }
            
        except Exception as e:
            return {"error": f"Indexing failed: {str(e)}"}


# Component factory
def create_conversation_indexer() -> ConversationIndexerComponent:
    """Create conversation indexer component with shared resources"""
    return ConversationIndexerComponent()