#!/usr/bin/env python3
"""
Conversation Memory Component - Conversation Domain Micro-Component
Single Responsibility: Manage conversation memory and project conversation indexing
Pattern: 50-80 LOC component using native LlamaIndex Memory and shared resources
"""

from pathlib import Path
from typing import Optional, List
from llama_index.core import Document
from llama_index.core.memory import Memory
from llama_index.core.base.llms.types import ChatMessage
from ...resources import get_intelligence_resource, IntelligenceResourceManager

# Import claude-parser's memory export
try:
    from claude_parser.memory import MemoryExporter
except ImportError:
    raise ImportError("Please install claude-parser: pip install -e ../claude-parser")


class ConversationMemoryComponent:
    """
    Conversation memory using shared resources and native LlamaIndex Memory
    Component Pattern: Small, focused, resource-injected
    """
    
    def __init__(self, intelligence_resource: Optional[IntelligenceResourceManager] = None):
        """
        Initialize with shared resource manager
        Uses singleton if none provided (prevents duplicate resources)
        """
        self.intelligence = intelligence_resource or get_intelligence_resource()
    
    def create_memory_session(self, session_id: str = "default") -> Memory:
        """Create native LlamaIndex Memory for conversation tracking - TRUE 95/5"""
        return Memory.from_defaults(session_id=session_id, token_limit=40000)
    
    def add_conversation_to_memory(self, memory: Memory, user_msg: str, assistant_msg: str) -> None:
        """Add conversation pair to memory - native pattern"""
        memory.put_messages([
            ChatMessage(role="user", content=user_msg),
            ChatMessage(role="assistant", content=assistant_msg)
        ])
    
    def search_conversation_memory(self, memory: Memory, query: str) -> List[ChatMessage]:
        """Search conversation memory - native retrieval"""
        all_messages = memory.get()
        relevant_messages = [
            msg for msg in all_messages if query.lower() in msg.content.lower()
        ]
        return relevant_messages[-10:]  # Return last 10 relevant messages
    
    def index_project_conversations(self, project_path: str, collection_name: str) -> int:
        """Index all conversations from a project folder using shared intelligence"""
        exporter = MemoryExporter(exclude_tools=True)
        docs = []
        
        for memory_dict in exporter.export_project(project_path):
            docs.append(Document(
                text=memory_dict["text"], 
                metadata=memory_dict["metadata"],
                doc_id=memory_dict["metadata"].get("user_uuid", "")
            ))
        
        if not docs:
            return 0
        
        # Use shared intelligence for indexing (eliminates redundant operations)
        from ..indexer import create_conversation_indexer
        indexer = create_conversation_indexer()
        result = indexer.index_documents(docs, collection_name)
        return result.get("documents_indexed", len(docs))
    
    def search_conversations(self, query: str, collection_name: str) -> str:
        """Search indexed conversations using shared intelligence"""
        try:
            return self.intelligence.intelligence.search_semantic(query, collection_name)
        except Exception as e:
            return f"Error searching conversations: {str(e)}"


# Component factory for easy instantiation
def create_conversation_memory() -> ConversationMemoryComponent:
    """Create conversation memory component with shared resources"""
    return ConversationMemoryComponent()