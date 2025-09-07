#!/usr/bin/env python3
"""
Conversation Stats Component - Conversation Domain Micro-Component
Single Responsibility: Get statistics about indexed conversations
Pattern: 50-80 LOC component with injected shared resources (FIXES DIP violation)
"""

from typing import Dict, Any, Optional
from ...resources import get_qdrant_resource, QdrantResourceManager


class ConversationStatsComponent:
    """
    Conversation statistics using shared resources - FIXES DRY/DIP violations
    Component Pattern: Small, focused, resource-injected
    """
    
    def __init__(self, qdrant_resource: Optional[QdrantResourceManager] = None):
        """
        Initialize with shared resource manager - FIXES DIP violation
        Uses singleton if none provided (prevents duplicate resources)
        """
        self.qdrant = qdrant_resource or get_qdrant_resource()
    
    def get_conversation_stats(self, collection: str = "conversations") -> Dict[str, Any]:
        """
        Get statistics about indexed conversations using shared Qdrant resource - FIXES DRY violation
        No duplicate API calls - uses centralized resource manager
        """
        try:
            # Use shared Qdrant client - ELIMINATES DRY violation
            client = self.qdrant.client
            
            if not client.collection_exists(collection):
                return {"error": f"Collection '{collection}' not found"}
            
            # Get collection info using shared client
            collection_info = client.get_collection(collection)
            
            return {
                "collection": collection,
                "total_messages": collection_info.points_count,
                "vector_size": collection_info.config.params.vectors.size,
                "indexed": True
            }
            
        except Exception as e:
            return {"error": f"Stats failed: {str(e)}"}


# Component factory
def create_conversation_stats() -> ConversationStatsComponent:
    """Create conversation stats component with shared resources"""
    return ConversationStatsComponent()