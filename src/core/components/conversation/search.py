#!/usr/bin/env python3
"""
Conversation Search Component - Conversation Domain Micro-Component
Single Responsibility: Search indexed conversations using shared resources
Pattern: 50-80 LOC component with injected shared resources (FIXES DIP violation)
"""

from typing import Dict, Any, List, Optional
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from ...resources import get_qdrant_resource, QdrantResourceManager


class ConversationSearchComponent:
    """
    Conversation search using shared resources - FIXES DRY/DIP violations
    Component Pattern: Small, focused, resource-injected
    """
    
    def __init__(self, qdrant_resource: Optional[QdrantResourceManager] = None):
        """
        Initialize with shared resource manager - FIXES DIP violation
        Uses singleton if none provided (prevents duplicate resources)
        """
        self.qdrant = qdrant_resource or get_qdrant_resource()
    
    def search_conversations(self, query: str, collection: str = "conversations", limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search indexed conversations using shared Qdrant resource - FIXES DRY violation
        No duplicate API calls - uses centralized resource manager
        """
        try:
            # Use shared Qdrant client - ELIMINATES DRY violation
            client = self.qdrant.client
            
            if not client.collection_exists(collection):
                return [{"error": f"Collection '{collection}' not found"}]
            
            # Use native index for search - NO duplicate vector store creation
            vector_store = QdrantVectorStore(client=client, collection_name=collection)
            index = VectorStoreIndex.from_vector_store(vector_store)
            
            # Query with native pattern
            query_engine = index.as_query_engine(similarity_top_k=limit)
            response = query_engine.query(query)
            
            # Extract source nodes for context
            results = []
            if hasattr(response, 'source_nodes'):
                for node in response.source_nodes:
                    results.append({
                        'text': node.text,
                        'score': node.score,
                        'metadata': node.metadata
                    })
            else:
                results.append({'response': str(response)})
            
            return results
            
        except Exception as e:
            return [{"error": f"Search failed: {str(e)}"}]


# Component factory
def create_conversation_search() -> ConversationSearchComponent:
    """Create conversation search component with shared resources"""
    return ConversationSearchComponent()