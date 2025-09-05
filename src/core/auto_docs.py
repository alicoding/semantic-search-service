#!/usr/bin/env python3
"""
Auto Documentation Generator - TRUE Native LlamaIndex 2025 Patterns
Using latest verified patterns:
- PropertyGraphIndex for structured code understanding
- Native entity/relation extraction for API documentation
- LlamaIndex Workflows for persistent documentation generation
"""

from llama_index.core import SimpleDirectoryReader, PropertyGraphIndex, Document
from llama_index.core.node_parser import CodeSplitter
from llama_index.core.schema import BaseNode
from pathlib import Path
import sys
import json
from datetime import datetime
from typing import List, Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.core.config import load_config, initialize_settings

def generate_api_reference() -> Dict[str, Any]:
    """Generate comprehensive API reference using PropertyGraphIndex - TRUE 2025 pattern with persistence"""
    print("📚 Generating API reference using PropertyGraphIndex...")
    
    # Initialize configuration and settings
    config = load_config()
    initialize_settings(config)
    
    # Check if we have a persisted index
    persist_dir = Path("./storage/auto_docs")
    try:
        if persist_dir.exists():
            print("🔄 Loading existing PropertyGraphIndex from storage...")
            from llama_index.core import StorageContext, load_index_from_storage
            storage_context = StorageContext.from_defaults(persist_dir=str(persist_dir))
            index = load_index_from_storage(storage_context)
            
            # Load and check for updated documents
            docs = SimpleDirectoryReader(
                input_dir="./src",
                recursive=True,
                required_exts=[".py"],
                exclude=["__pycache__", "*.pyc", "venv", ".git", "__init__.py"]
            ).load_data()
            
            # Use refresh_ref_docs for incremental updates - TRUE 2025 pattern
            print("🔄 Performing incremental updates with refresh_ref_docs...")
            refresh_results = index.refresh_ref_docs(docs)
            updated_count = sum(refresh_results)
            print(f"✅ Updated {updated_count} of {len(docs)} documents")
        else:
            print("🆕 Creating new PropertyGraphIndex...")
            # Load codebase with native SimpleDirectoryReader
            docs = SimpleDirectoryReader(
                input_dir="./src",
                recursive=True,
                required_exts=[".py"],
                exclude=["__pycache__", "*.pyc", "venv", ".git", "__init__.py"]
            ).load_data()
            
            if not docs:
                return {"error": "No Python files found to document"}
            
            # Create new PropertyGraphIndex with persistent storage
            index = PropertyGraphIndex.from_documents(
                documents=docs,
                show_progress=True
            )
            
            # Persist the index for future incremental updates
            persist_dir.parent.mkdir(exist_ok=True)
            index.storage_context.persist(persist_dir=str(persist_dir))
            print(f"💾 Index persisted to {persist_dir}")
    
    except Exception as e:
        print(f"⚠️ Error with persistent index: {e}")
        print("🔄 Falling back to fresh index creation...")
        # Fallback to creating fresh index
        docs = SimpleDirectoryReader(
            input_dir="./src",
            recursive=True,
            required_exts=[".py"],
            exclude=["__pycache__", "*.pyc", "venv", ".git", "__init__.py"]
        ).load_data()
        
        if not docs:
            return {"error": "No Python files found to document"}
        
        index = PropertyGraphIndex.from_documents(
            documents=docs,
            show_progress=True
        )
    
    # Native query patterns for structured API extraction
    api_queries = {
        "endpoints": """
        Extract all API endpoints from this FastAPI codebase.
        For each endpoint provide:
        - HTTP method and path
        - Purpose and description
        - Parameters (path, query, body)
        - Response format
        - Example usage
        Format as structured markdown.
        """,
        
        "classes": """
        Extract all Python classes with their methods and properties.
        For each class provide:
        - Class name and purpose
        - Constructor parameters
        - Public methods with parameters
        - Usage examples
        Format as structured markdown.
        """,
        
        "functions": """
        Extract all standalone functions (not in classes).
        For each function provide:
        - Function name and purpose
        - Parameters with types
        - Return value
        - Usage example
        Format as structured markdown.
        """
    }
    
    # Execute queries using native query engine
    query_engine = index.as_query_engine(
        include_text=True,
        similarity_top_k=10,
        response_mode="tree_summarize"
    )
    
    results = {}
    for section, query in api_queries.items():
        print(f"📊 Generating {section} documentation...")
        response = query_engine.query(query)
        results[section] = str(response)
    
    # Generate final API reference
    api_reference = f"""# API Reference

*Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} using native LlamaIndex PropertyGraphIndex*

## Overview
This API reference was automatically generated from the codebase using LlamaIndex PropertyGraphIndex for structured code analysis.

## API Endpoints
{results['endpoints']}

## Classes and Components  
{results['classes']}

## Utility Functions
{results['functions']}

## Generation Details
- Generated using: LlamaIndex PropertyGraphIndex
- Source files: {len(docs)} Python files
- Analysis mode: Graph-based semantic extraction
- Last updated: {datetime.now().isoformat()}
"""
    
    # Write to file
    output_path = Path("docs/API_REFERENCE.md")
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, "w") as f:
        f.write(api_reference)
    
    print(f"✅ API reference generated: {output_path}")
    return {
        "generated": True,
        "output": str(output_path),
        "sections": list(api_queries.keys()),
        "source_files": len(docs)
    }

def generate():
    """Main entry point - maintains backward compatibility"""
    return generate_api_reference()

def functions():
    """Extract function signatures using NATIVE patterns"""
    print("🔍 Extracting function signatures using native patterns...")
    
    # Load code files
    docs = SimpleDirectoryReader(
        input_dir="./src",
        recursive=True,
        required_exts=[".py"]
    ).load_data()
    
    # Use CodeSplitter to parse code properly
    code_splitter = CodeSplitter(
        language="python",
        chunk_lines=40,
        chunk_lines_overlap=0,  # No overlap for signature extraction
        max_chars=1500
    )
    nodes = code_splitter.get_nodes_from_documents(docs)
    
    # Build index for querying
    index = PropertyGraphIndex.from_documents(docs)
    query_engine = index.as_query_engine()
    
    # Query for function signatures
    signatures_response = query_engine.query(
        "List all function signatures (def statements) in the codebase. "
        "Format as a bullet list with just the function signatures."
    )
    
    # Write to file
    output_path = Path("docs/FUNCTION_SIGNATURES.md")
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, "w") as f:
        f.write("# Function Signatures\n\n")
        f.write(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} using native LlamaIndex*\n\n")
        f.write(str(signatures_response))
    
    print(f"✅ Function signatures extracted to {output_path}")
    return True

def refresh():
    """Refresh documentation - uses native incremental patterns"""
    print("🔄 Refreshing documentation...")
    # For incremental refresh, we could use refresh_ref_docs() pattern
    # but for documentation generation, full regeneration is appropriate
    return generate()

if __name__ == "__main__":
    # CLI interface
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "generate":
            generate()
        elif command == "functions":
            functions()
        elif command == "refresh":
            refresh()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python auto_docs.py [generate|functions|refresh]")
    else:
        # Default action
        generate()