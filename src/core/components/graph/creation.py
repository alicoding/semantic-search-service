#!/usr/bin/env python3
"""
Graph Creation Component - Graph Domain Micro-Component
Single Responsibility: Create knowledge graphs from codebase and documents
Pattern: 50-80 LOC component with injected shared resources (no duplicate API calls)
"""

from typing import Optional
from llama_index.core import SimpleDirectoryReader, Settings
from llama_index.core.node_parser import CodeSplitter
from llama_index.readers.web import SpiderWebReader
from ...resources import get_intelligence_resource, IntelligenceResourceManager
from ...intelligence.types import IndexMode


class GraphCreationComponent:
    """
    Knowledge graph creation using shared resources
    Component Pattern: Small, focused, resource-injected
    """
    
    def __init__(self, intelligence_resource: Optional[IntelligenceResourceManager] = None):
        """
        Initialize with shared resource manager
        Uses singleton if none provided (prevents duplicate resources)
        """
        self.intelligence = intelligence_resource or get_intelligence_resource()
    
    def create_from_codebase(self, code_path: str, collection_name: str):
        """
        Create knowledge graph from codebase using shared intelligence resource
        No duplicate API calls - uses centralized resource manager
        """
        try:
            # Use shared intelligence to create PropertyGraphIndex
            graph_collection = f"kg_{collection_name}"
            result = self.intelligence.intelligence.index_project(code_path, graph_collection, IndexMode.GRAPH)
            
            if result["status"] == "success":
                return self.intelligence.get_index(graph_collection, IndexMode.GRAPH)
            else:
                raise Exception(result.get("error", "Failed to create knowledge graph"))
                
        except Exception as e:
            # Fallback to manual creation with custom CodeSplitter
            documents = SimpleDirectoryReader(
                input_dir=code_path,
                recursive=True,
                required_exts=[".py", ".js", ".ts"],
                exclude=["__pycache__", "*.pyc", ".git", "node_modules"]
            ).load_data()
            
            # Use CodeSplitter for specialized code parsing
            code_splitter = CodeSplitter(
                language="python",
                chunk_lines=40,
                chunk_lines_overlap=15,
                max_chars=1500
            )
            
            nodes = code_splitter.get_nodes_from_documents(documents)
            
            # Use shared intelligence strategy for storage context
            strategy = self.intelligence.intelligence._get_strategy(IndexMode.GRAPH)
            return strategy.create_index(nodes, f"kg_{collection_name}")
    
    def create_from_documents(self, docs_path: str, collection_name: str):
        """
        Create knowledge graph from documentation using shared intelligence resource
        Includes web crawling capability for internal wikis/confluence
        """
        graph_collection = f"kg_{collection_name}"
        
        try:
            # For simple filesystem paths, use shared intelligence directly
            if not docs_path.startswith("http"):
                result = self.intelligence.intelligence.index_project(docs_path, graph_collection, IndexMode.GRAPH)
                
                if result["status"] == "success":
                    return self.intelligence.get_index(graph_collection, IndexMode.GRAPH)
                else:
                    raise Exception(result.get("error", "Failed to create knowledge graph from documents"))
            else:
                # For web crawling, need custom handling
                spider = SpiderWebReader(max_depth=3, mode="bfs")
                documents = spider.load_data([docs_path])
                
                # Use shared intelligence strategy for storage context
                strategy = self.intelligence.intelligence._get_strategy(IndexMode.GRAPH)
                return strategy.create_index(documents, graph_collection)
                
        except Exception as e:
            raise Exception(f"Error creating graph from documents: {str(e)}")


# Component factory for easy instantiation
def create_graph_creation() -> GraphCreationComponent:
    """Create graph creation component with shared resources"""
    return GraphCreationComponent()