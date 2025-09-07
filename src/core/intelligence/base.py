#!/usr/bin/env python3
"""
Core Interfaces and Protocols - SOLID Compliant  
Single Responsibility: Define contracts for dependency injection
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Union, Protocol

from llama_index.core import Document
from llama_index.core.indices.property_graph import PropertyGraphIndex
from llama_index.core import VectorStoreIndex


class DocumentLoader(Protocol):
    """Protocol for loading documents from various sources"""
    def load_documents(self, path: str, **kwargs) -> List[Document]:
        """Load documents from path"""
        ...


class IndexStrategy(ABC):
    """Abstract strategy for creating indexes"""
    
    @abstractmethod
    def create_index(self, documents: List[Document], collection_name: str) -> Union[VectorStoreIndex, PropertyGraphIndex]:
        """Create index from documents"""
        pass
    
    @abstractmethod
    def get_index(self, collection_name: str) -> Union[VectorStoreIndex, PropertyGraphIndex]:
        """Get existing index"""
        pass


# CacheStrategy removed - using native LlamaIndex caching (95/5 principle)