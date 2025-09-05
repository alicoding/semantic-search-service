#!/usr/bin/env python3
"""
Conversation Memory - Native LlamaIndex Memory integration  
Following TRUE 95/5 principle - LlamaIndex does everything
"""

from pathlib import Path
from typing import Optional, List
from llama_index.core import Document, VectorStoreIndex, StorageContext
from llama_index.core.memory import Memory
from llama_index.core.base.llms.types import ChatMessage
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import models

# Import claude-parser's memory export
try:
    from claude_parser.memory import MemoryExporter
except ImportError:
    raise ImportError("Please install claude-parser: pip install -e ../claude-parser")

# Settings and client configured in config.py
from llama_index.core import Settings
from .config import get_qdrant_client

def create_memory_session(session_id: str = "default") -> Memory:
    """Create native LlamaIndex Memory for conversation tracking - TRUE 95/5"""
    return Memory.from_defaults(
        session_id=session_id,
        token_limit=40000  # Configurable from config
    )

def add_conversation_to_memory(memory: Memory, user_msg: str, assistant_msg: str) -> None:
    """Add conversation pair to memory - native pattern"""
    memory.put_messages([
        ChatMessage(role="user", content=user_msg),
        ChatMessage(role="assistant", content=assistant_msg)
    ])

def search_conversation_memory(memory: Memory, query: str) -> List[ChatMessage]:
    """Search conversation memory - native retrieval"""
    # Get all messages and filter (LlamaIndex will add semantic search in future)
    all_messages = memory.get()
    # Simple text search for now - could be enhanced with semantic search
    relevant_messages = [
        msg for msg in all_messages 
        if query.lower() in msg.content.lower()
    ]
    return relevant_messages[-10:]  # Return last 10 relevant messages

def index_current_project(collection_name: Optional[str] = None) -> int:
    """Index ALL conversations in current project"""
    project_path = str(Path.cwd())
    
    if not collection_name:
        collection_name = f"{Path.cwd().name}_conversations"
    
    return index_project_conversations(project_path, collection_name)

def index_project_conversations(project_path: str, collection_name: str) -> int:
    """Index all conversations from a project folder"""
    exporter = MemoryExporter(exclude_tools=True)
    
    # Collect all documents using export_project (folder-based)
    docs = []
    for memory_dict in exporter.export_project(project_path):
        docs.append(Document(
            text=memory_dict["text"], 
            metadata=memory_dict["metadata"],
            doc_id=memory_dict["metadata"].get("user_uuid", "")
        ))
    
    # Use centralized client from config
    client = get_qdrant_client()
    
    # Create collection if needed (simple, no hybrid for now)
    if not client.collection_exists(collection_name):
        # Get embedding dimension from current model
        embed_dim = Settings.embed_model.embed_dim if hasattr(Settings.embed_model, 'embed_dim') else 1536
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=embed_dim,
                distance=models.Distance.COSINE
            )
        )
    
    # Index with storage_context (required for Qdrant to actually store)
    vector_store = QdrantVectorStore(client=client, collection_name=collection_name)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    VectorStoreIndex.from_documents(docs, storage_context=storage_context)
    
    return len(docs)

def search_conversations(query: str, collection_name: str) -> str:
    """Search indexed conversations"""
    client = get_qdrant_client()
    vector_store = QdrantVectorStore(client=client, collection_name=collection_name)
    index = VectorStoreIndex.from_vector_store(vector_store)
    return str(index.as_query_engine().query(query))

# Total: ~60 lines, much cleaner!