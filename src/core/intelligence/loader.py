#!/usr/bin/env python3
"""
Document Loader Implementation  
Single Responsibility: Load documents from various sources
"""

from typing import List
from llama_index.core import Document


class DefaultDocumentLoader:
    """Default document loader using SimpleDirectoryReader"""
    
    def load_documents(self, path: str, **kwargs) -> List[Document]:
        """Load documents with configured settings"""
        from ..config import get_configured_reader
        
        reader = get_configured_reader(path, **kwargs)
        return reader.load_data()