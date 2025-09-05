#!/usr/bin/env python3
"""
JSONL Conversation Indexer - TRUE 95/5 Pattern
Index Claude/Anthropic conversation format using native LlamaIndex
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from .config import get_qdrant_client

def index_conversations(jsonl_path: str, collection_name: str = "conversations") -> Dict[str, Any]:
    """
    Index JSONL conversations from Claude/Anthropic - TRUE 95/5 pattern
    Handles standard conversation format with role/content fields
    """
    path = Path(jsonl_path)
    if not path.exists():
        return {"error": f"File not found: {jsonl_path}"}
    
    # Parse JSONL and create documents
    documents = []
    conversation_count = 0
    message_count = 0
    
    with open(path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                msg = json.loads(line.strip())
                
                # Handle different formats
                if isinstance(msg, dict):
                    # Single message format
                    role = msg.get('role', 'unknown')
                    content = msg.get('content', '')
                    metadata = {
                        'role': role,
                        'line_number': line_num,
                        'message_id': msg.get('id', f"msg_{line_num}"),
                        'timestamp': msg.get('timestamp', ''),
                        'model': msg.get('model', ''),
                    }
                    
                    # Create document with conversation context
                    text = f"[{role}]: {content}"
                    documents.append(Document(text=text, metadata=metadata))
                    message_count += 1
                    
                elif isinstance(msg, list):
                    # Conversation format (list of messages)
                    conversation_count += 1
                    for idx, turn in enumerate(msg):
                        role = turn.get('role', 'unknown')
                        content = turn.get('content', '')
                        metadata = {
                            'role': role,
                            'conversation_id': f"conv_{line_num}",
                            'turn_number': idx,
                            'line_number': line_num
                        }
                        text = f"[{role}]: {content}"
                        documents.append(Document(text=text, metadata=metadata))
                        message_count += 1
                        
            except json.JSONDecodeError as e:
                print(f"Warning: Skipping invalid JSON at line {line_num}: {e}")
                continue
    
    if not documents:
        return {"error": "No valid messages found in JSONL file"}
    
    # Create index with native LlamaIndex
    client = get_qdrant_client()
    vector_store = QdrantVectorStore(client=client, collection_name=collection_name)
    
    # Index documents
    index = VectorStoreIndex.from_documents(
        documents,
        vector_store=vector_store,
        show_progress=True
    )
    
    return {
        "indexed": True,
        "collection": collection_name,
        "conversations": conversation_count,
        "messages": message_count,
        "documents": len(documents),
        "source": jsonl_path
    }

def index_anthropic_export(export_path: str) -> Dict[str, Any]:
    """
    Index Anthropic Console export format - TRUE 95/5 pattern
    Handles the specific export format from Anthropic Console
    """
    path = Path(export_path)
    if not path.exists():
        return {"error": f"File not found: {export_path}"}
    
    documents = []
    
    with open(path, 'r') as f:
        data = json.load(f) if path.suffix == '.json' else [json.loads(line) for line in f]
    
    # Handle Anthropic export structure
    if isinstance(data, dict) and 'conversations' in data:
        conversations = data['conversations']
    else:
        conversations = data if isinstance(data, list) else [data]
    
    for conv_idx, conversation in enumerate(conversations):
        conv_id = conversation.get('uuid', f"conv_{conv_idx}")
        messages = conversation.get('messages', [])
        
        for msg_idx, message in enumerate(messages):
            role = message.get('role', 'unknown')
            content = message.get('content', '')
            
            # Handle content that might be a list (multi-part messages)
            if isinstance(content, list):
                content = ' '.join([part.get('text', '') for part in content if 'text' in part])
            
            metadata = {
                'conversation_id': conv_id,
                'message_index': msg_idx,
                'role': role,
                'model': message.get('model', ''),
                'created_at': message.get('created_at', '')
            }
            
            text = f"[{role}]: {content}"
            documents.append(Document(text=text, metadata=metadata))
    
    if not documents:
        return {"error": "No messages found in Anthropic export"}
    
    # Index with native pattern
    client = get_qdrant_client()
    vector_store = QdrantVectorStore(client=client, collection_name="anthropic_conversations")
    
    index = VectorStoreIndex.from_documents(
        documents,
        vector_store=vector_store,
        show_progress=True
    )
    
    return {
        "indexed": True,
        "collection": "anthropic_conversations",
        "conversations": len(conversations),
        "messages": len(documents),
        "source": export_path
    }

def search_conversations(query: str, collection: str = "conversations", limit: int = 5) -> List[Dict[str, Any]]:
    """
    Search indexed conversations - TRUE 95/5 pattern
    Returns relevant conversation snippets
    """
    client = get_qdrant_client()
    if not client.collection_exists(collection):
        return [{"error": f"Collection '{collection}' not found"}]
    
    # Use native index for search
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

def get_conversation_stats(collection: str = "conversations") -> Dict[str, Any]:
    """
    Get statistics about indexed conversations - TRUE 95/5 pattern
    """
    client = get_qdrant_client()
    if not client.collection_exists(collection):
        return {"error": f"Collection '{collection}' not found"}
    
    # Get collection info
    collection_info = client.get_collection(collection)
    
    return {
        "collection": collection,
        "total_messages": collection_info.points_count,
        "vector_size": collection_info.config.params.vectors.size,
        "indexed": True
    }