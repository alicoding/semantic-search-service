#!/usr/bin/env python3
"""
Conversation Parser Component - Conversation Domain Micro-Component
Single Responsibility: Parse JSONL/Anthropic conversation formats into Documents
Pattern: 50-80 LOC component with no dependencies (pure parsing logic)
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from llama_index.core import Document


class ConversationParserComponent:
    """
    Conversation format parsing - pure logic, no dependencies
    Component Pattern: Small, focused, stateless
    """
    
    def parse_jsonl_file(self, jsonl_path: str) -> Dict[str, Any]:
        """Parse JSONL conversation file into documents"""
        path = Path(jsonl_path)
        if not path.exists():
            return {"error": f"File not found: {jsonl_path}"}
        
        documents = []
        conversation_count = 0
        message_count = 0
        
        with open(path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    msg = json.loads(line.strip())
                    
                    if isinstance(msg, dict):
                        # Single message format
                        doc = self._create_message_document(msg, line_num)
                        documents.append(doc)
                        message_count += 1
                        
                    elif isinstance(msg, list):
                        # Conversation format (list of messages)
                        conversation_count += 1
                        for idx, turn in enumerate(msg):
                            doc = self._create_conversation_document(turn, line_num, idx)
                            documents.append(doc)
                            message_count += 1
                            
                except json.JSONDecodeError as e:
                    print(f"Warning: Skipping invalid JSON at line {line_num}: {e}")
                    continue
        
        return {
            "documents": documents,
            "conversations": conversation_count,
            "messages": message_count,
            "source": jsonl_path
        }
    
    def parse_anthropic_export(self, export_path: str) -> Dict[str, Any]:
        """Parse Anthropic Console export format into documents"""
        path = Path(export_path)
        if not path.exists():
            return {"error": f"File not found: {export_path}"}
        
        documents = []
        
        with open(path, 'r') as f:
            data = json.load(f) if path.suffix == '.json' else [json.loads(line) for line in f]
        
        # Handle Anthropic export structure
        conversations = self._extract_conversations(data)
        
        for conv_idx, conversation in enumerate(conversations):
            conv_id = conversation.get('uuid', f"conv_{conv_idx}")
            messages = conversation.get('messages', [])
            
            for msg_idx, message in enumerate(messages):
                doc = self._create_anthropic_document(message, conv_id, msg_idx)
                documents.append(doc)
        
        return {
            "documents": documents,
            "conversations": len(conversations),
            "messages": len(documents),
            "source": export_path
        }
    
    def _create_message_document(self, msg: dict, line_num: int) -> Document:
        """Create document from single message"""
        role = msg.get('role', 'unknown')
        content = msg.get('content', '')
        metadata = {
            'role': role,
            'line_number': line_num,
            'message_id': msg.get('id', f"msg_{line_num}"),
            'timestamp': msg.get('timestamp', ''),
            'model': msg.get('model', ''),
        }
        text = f"[{role}]: {content}"
        return Document(text=text, metadata=metadata)
    
    def _create_conversation_document(self, turn: dict, line_num: int, idx: int) -> Document:
        """Create document from conversation turn"""
        role = turn.get('role', 'unknown')
        content = turn.get('content', '')
        metadata = {
            'role': role,
            'conversation_id': f"conv_{line_num}",
            'turn_number': idx,
            'line_number': line_num
        }
        text = f"[{role}]: {content}"
        return Document(text=text, metadata=metadata)
    
    def _create_anthropic_document(self, message: dict, conv_id: str, msg_idx: int) -> Document:
        """Create document from Anthropic message"""
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
        return Document(text=text, metadata=metadata)
    
    def _extract_conversations(self, data: Any) -> List[dict]:
        """Extract conversations from various data structures"""
        if isinstance(data, dict) and 'conversations' in data:
            return data['conversations']
        return data if isinstance(data, list) else [data]


# Component factory
def create_conversation_parser() -> ConversationParserComponent:
    """Create conversation parser component"""
    return ConversationParserComponent()