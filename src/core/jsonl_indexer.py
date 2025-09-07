#!/usr/bin/env python3
"""
JSONL Conversation Indexer API - Component-Based Architecture
Single Responsibility: Unified API for conversation indexing using micro-components
Pattern: 50-80 LOC API delegating to domain components (FIXES DRY/DIP violations)
"""

from typing import Dict, Any, List
from .components.conversation.parser import create_conversation_parser
from .components.conversation.indexer import create_conversation_indexer
from .components.conversation.search import create_conversation_search
from .components.conversation.stats import create_conversation_stats


def index_conversations(jsonl_path: str, collection_name: str = "conversations") -> Dict[str, Any]:
    """
    Index JSONL conversations using parser + indexer components
    FIXES DRY/DIP: No duplicate Qdrant calls, proper dependency injection
    """
    # Parse conversations using parser component
    parser = create_conversation_parser()
    parse_result = parser.parse_jsonl_file(jsonl_path)
    
    if "error" in parse_result:
        return parse_result
    
    # Index documents using indexer component with shared resources
    indexer = create_conversation_indexer()
    index_result = indexer.index_documents(parse_result["documents"], collection_name)
    
    if "error" in index_result:
        return index_result
    
    # Combine results for backward compatibility
    return {
        "indexed": True,
        "collection": collection_name,
        "conversations": parse_result["conversations"],
        "messages": parse_result["messages"],
        "documents": len(parse_result["documents"]),
        "source": jsonl_path
    }


def index_anthropic_export(export_path: str) -> Dict[str, Any]:
    """
    Index Anthropic Console export using parser + indexer components
    FIXES DRY/DIP: No duplicate Qdrant calls, proper dependency injection
    """
    # Parse Anthropic export using parser component
    parser = create_conversation_parser()
    parse_result = parser.parse_anthropic_export(export_path)
    
    if "error" in parse_result:
        return parse_result
    
    # Index documents using indexer component with shared resources
    indexer = create_conversation_indexer()
    index_result = indexer.index_documents(parse_result["documents"], "anthropic_conversations")
    
    if "error" in index_result:
        return index_result
    
    # Combine results for backward compatibility
    return {
        "indexed": True,
        "collection": "anthropic_conversations",
        "conversations": parse_result["conversations"],
        "messages": parse_result["messages"],
        "source": export_path
    }


def search_conversations(query: str, collection: str = "conversations", limit: int = 5) -> List[Dict[str, Any]]:
    """
    Search indexed conversations using search component
    FIXES DRY/DIP: No duplicate Qdrant calls, proper dependency injection
    """
    search_component = create_conversation_search()
    return search_component.search_conversations(query, collection, limit)


def get_conversation_stats(collection: str = "conversations") -> Dict[str, Any]:
    """
    Get conversation statistics using stats component
    FIXES DRY/DIP: No duplicate Qdrant calls, proper dependency injection
    """
    stats_component = create_conversation_stats()
    return stats_component.get_conversation_stats(collection)