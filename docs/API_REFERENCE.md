# API Reference

*Auto-generated on 2025-09-04 13:44:03*

## Table of Contents

- [__init__.py](#__init__py)
- [api.py](#apipy)
- [auto_docs.py](#auto_docspy)
- [business_extractor.py](#business_extractorpy)
- [cli.py](#clipy)
- [config.py](#configpy)
- [conversation_memory.py](#conversation_memorypy)
- [diagram_generator.py](#diagram_generatorpy)
- [doc_intelligence.py](#doc_intelligencepy)
- [doc_refresh.py](#doc_refreshpy)
- [doc_search.py](#doc_searchpy)
- [index_helper.py](#index_helperpy)
- [jsonl_indexer.py](#jsonl_indexerpy)
- [knowledge_graph.py](#knowledge_graphpy)
- [mcp_fastmcp.py](#mcp_fastmcppy)
- [mcp_server.py](#mcp_serverpy)
- [prompts.py](#promptspy)
- [redis_cache.py](#redis_cachepy)
- [semantic_search.py](#semantic_searchpy)

---

## __init__.py

```python
# Semantic Search Service
```

---

```python
"""Core semantic search functionality"""
from .semantic_search import *
from .doc_search import *
```

---

```python
"""Integration layers for MCP, API, and CLI"""
```

---

## api.py

```python
#!/usr/bin/env python3
"""
Context7 FastAPI - Thin wrapper only
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from pathlib import Path
import subprocess
import os

# Clean environment for OpenAI
app = FastAPI(title="AI Documentation Intelligence API", version="2.0.0")

# Import functions directly - TRUE 95/5 pattern
from src.core import semantic_search, doc_search
from src.core.doc_intelligence import get_doc_intellige
# ... (truncated)
```

---

## auto_docs.py

### Function: `generate`
```python
#!/usr/bin/env python3
"""
Auto Documentation Generator - TRUE 95/5 Pattern
Uses native LlamaIndex patterns for documentation generation
No custom parsing - let the framework do the work
"""

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SimpleFileNodeParser
from pathlib import Path
import sys
from datetime import datetime

def generate():
    """Generate API documentation using native LlamaIndex - TRUE 95/5"""
    print("📚 Generating API documentati
# ... (truncated)
```

---

## business_extractor.py

### Function: `extract_business_logic`
```python
#!/usr/bin/env python3
"""
Business Logic Extractor - TRUE 95/5 Pattern
Extract business rules and logic from codebase using native LlamaIndex
"""

from .index_helper import get_index, index_exists
from typing import Dict, Any, List

def extract_business_logic(project: str) -> Dict[str, Any]:
    """
    Extract core business logic - TRUE 95/5 pattern
    Returns structured business rules and logic
    """
    if not index_exists(project):
        return {"error": f"Project '{project}' not index
# ... (truncated)
```

---

## cli.py

### Function: `index`
### Function: `refresh`
### Function: `search`
### Function: `violations`
### Function: `suggest`
```python
#!/usr/bin/env python3
"""
Context7 CLI - Thin wrapper
"""

import typer
from src.core import semantic_search, doc_search

app = typer.Typer()

@app.command()
def index(path: str, name: str, mode: str = None):
    """Index a project with optional mode (graph/basic/auto)."""
    result = semantic_search.index_project(path, name, mode)
    typer.echo(f"Indexed: {result}")

@app.command()
def refresh(name: str, path: str):
    """Incremental refresh - only updates changed files."""
    result = sem
# ... (truncated)
```

---

## config.py

### Function: `load_config`
```python
"""
AI Development Intelligence - Configuration Module
Uses native LlamaIndex Settings with yaml/env configuration
TRUE 95/5: All configuration is native LlamaIndex
"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()
from typing import Optional
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from llama_index.llms.openai_like import OpenAILike
from llama_index
# ... (truncated)
```

---

## conversation_memory.py

### Function: `create_memory_session`
```python
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
from qdrant_client import QdrantClient, models

# Impo
# ... (truncated)
```

---

## diagram_generator.py

### Function: `generate_sequence_diagram`
```python
#!/usr/bin/env python3
"""
Diagram Generator - ENHANCED with Knowledge Graphs
Generate VISUAL diagrams using PropertyGraphIndex - matching LlamaIndex Cloud
Now with native visualization, not just text output
"""

from .index_helper import get_index, index_exists
from .knowledge_graph import EnterpriseKnowledgeGraph
from .prompts import PROMPTS
import json
from typing import Dict, Any, Optional

def generate_sequence_diagram(project: str) -> Dict[str, Any]:
    """
    Generate sequence diagram f
# ... (truncated)
```

---

## doc_intelligence.py

### Class: `DocIntelligence`
### Function: `__init__`
### Function: `index_framework`
```python
#!/usr/bin/env python3
"""
Documentation Intelligence System
Provides precise documentation snippets to prevent AI agents from guessing
Accessible via CLI, REST API, and MCP tools
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.vector_stores.qdrant import QdrantVectorStore
from .config import get_qdrant_client, CONFIG
from .semantic_s
# ... (truncated)
```

---

## doc_refresh.py

### Function: `refresh_documentation_collection`
```python
#!/usr/bin/env python3
"""
Documentation Auto-Refresh - Native LlamaIndex refresh patterns
Following TRUE 95/5 principle - LlamaIndex refresh_ref_docs() does everything
"""

import time
import threading
from typing import Dict, List
from pathlib import Path
from llama_index.core import SimpleDirectoryReader, Document, VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from .config import get_qdrant_client, CONFIG

def refresh_documentation_collection(collection_name:
# ... (truncated)
```

---

## doc_search.py

### Function: `index_library_docs`
### Function: `search_docs`
```python
#!/usr/bin/env python3
"""
Documentation Search - Context7 Tamer
Indexes library documentation for semantic search without context overload
NO INHERITANCE - Direct function calls only
"""

from typing import Dict, Any, List
from .semantic_search import index_project, search, list_projects, get_project_info

def index_library_docs(library_name: str, docs_path: str) -> Dict[str, Any]:
    """Index library documentation into dedicated collection."""
    collection_name = f"docs_{library_name.lower(
# ... (truncated)
```

---

## index_helper.py

### Function: `get_graph_index`
```python
#!/usr/bin/env python3
"""
Index Helper - DRY pattern for index access
Enterprise by default with PropertyGraphIndex
Basic mode available when explicitly requested
"""

from llama_index.core import PropertyGraphIndex, StorageContext, Settings, VectorStoreIndex
from llama_index.core.graph_stores import SimplePropertyGraphStore
from llama_index.core.indices.property_graph import SimpleLLMPathExtractor, ImplicitPathExtractor
from llama_index.vector_stores.qdrant import QdrantVectorStore
from .confi
# ... (truncated)
```

---

## jsonl_indexer.py

### Function: `index_conversations`
```python
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
    In
# ... (truncated)
```

---

## knowledge_graph.py

### Class: `EnterpriseKnowledgeGraph`
```python
#!/usr/bin/env python3
"""
Knowledge Graph with PropertyGraphIndex - Enterprise Grade
Full LlamaIndex Cloud features but 100% local for enterprise/PII compliance
Using Qdrant for vector store (not ChromaDB) for enterprise features
"""

from llama_index.core import Settings, StorageContext
from llama_index.core.indices.property_graph import PropertyGraphIndex
from llama_index.core.indices.property_graph import (
    ImplicitPathExtractor,
    SimpleLLMPathExtractor,
    SchemaLLMPathExtractor,
)
fro
# ... (truncated)
```

---

## mcp_fastmcp.py

### Function: `get_pattern`
```python
#!/usr/bin/env python3
"""
MCP Server using FastMCP
Exposes documentation intelligence as MCP tools for Claude and other AI agents
"""

from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from fastmcp import FastMCP
from src.core.doc_intelligence import get_doc_intelligence
from src.core import semantic_search

# Initialize FastMCP server
mcp = FastMCP("semantic-search-intelligence")

# Get shared DocIntellige
# ... (truncated)
```

---

## mcp_server.py

### Function: `index_project`
### Function: `search_code`
### Function: `find_violations`
### Function: `suggest_libraries`
```python
#!/usr/bin/env python3
"""
Context7 MCP Server - Thin wrapper
"""

from pathlib import Path
from typing import Optional
from mcp.server.fastmcp import FastMCP

# Initialize MCP
mcp = FastMCP("Semantic Search")

# Import functions directly
from src.core import semantic_search

@mcp.tool()
def index_project(project_path: str, collection_name: Optional[str] = None) -> str:
    """Index a project for semantic search."""
    name = collection_name or Path(project_path).name
    semantic_search.index_
# ... (truncated)
```

---

## prompts.py

### Function: `load_prompts`
### Function: `get_prompt`
### Function: `get_violation_prompt`
### Function: `get_suggestion_prompt`
```python
#!/usr/bin/env python3
"""
Prompts loader - Centralized prompt management
Following OCP principle - extend via YAML, not code changes
"""

import yaml
from pathlib import Path
from typing import Dict, Any

# Load prompts once at module import
PROMPTS_FILE = Path(__file__).parent / "prompts.yaml"

def load_prompts() -> Dict[str, Any]:
    """Load prompts from YAML - TRUE 95/5"""
    with open(PROMPTS_FILE, 'r') as f:
        return yaml.safe_load(f)

# Load once at import
PROMPTS = load_prompts()
# ... (truncated)
```

---

## redis_cache.py

### Function: `get_redis_client`
```python
#!/usr/bin/env python3
"""
Redis Caching for Sub-100ms Responses
Following TRUE 95/5 principle - using native LlamaIndex caching
"""

import redis
import hashlib
import json
import pickle
from typing import Any, Optional
from .config import CONFIG

# Get Redis config from YAML
REDIS_HOST = CONFIG.get('redis_host', 'localhost')
REDIS_PORT = CONFIG.get('redis_port', 6380)  # Using 6380 to avoid conflict
REDIS_TTL = CONFIG.get('cache_ttl', 3600)  # Default 1 hour

def get_redis_client():
    """Get
# ... (truncated)
```

---

## semantic_search.py

### Class: `CodeEntities`
```python
#!/usr/bin/env python3
"""Semantic Search - TRUE 95/5 Pattern (PropertyGraphIndex for enterprise)"""

from llama_index.core import SimpleDirectoryReader, Settings, PropertyGraphIndex, StorageContext
from llama_index.core.graph_stores import SimplePropertyGraphStore
from llama_index.core.indices.property_graph import (
    SimpleLLMPathExtractor, 
    ImplicitPathExtractor,
    SchemaLLMPathExtractor
)
from llama_index.core.node_parser import CodeSplitter, SentenceSplitter
from llama_index.vector
# ... (truncated)
```

---

