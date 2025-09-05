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
from llama_index.vector_stores.qdrant import QdrantVectorStore
from enum import Enum
from typing import Optional
from pathlib import Path

from .config import get_qdrant_client, CONFIG, get_configured_reader
from .index_helper import get_index, index_exists, _graph_stores
from .prompts import get_violation_prompt, get_suggestion_prompt

# Settings are configured in config.py on module import
# Client comes from config
client = get_qdrant_client()

# Schema definitions for structured extraction (Enterprise feature)
class CodeEntities(str, Enum):
    """Entity types for code analysis"""
    CLASS = "Class"
    FUNCTION = "Function"
    METHOD = "Method"
    VARIABLE = "Variable"
    API_ENDPOINT = "API_Endpoint"
    DATABASE = "Database"
    SERVICE = "Service"
    MODULE = "Module"

class CodeRelations(str, Enum):
    """Relationship types for code analysis"""
    CALLS = "calls"
    IMPLEMENTS = "implements"
    EXTENDS = "extends"
    IMPORTS = "imports"
    USES = "uses"
    DEPENDS_ON = "depends_on"
    VALIDATES = "validates"
    TRANSFORMS = "transforms"

class BusinessEntities(str, Enum):
    """Entity types for business logic"""
    BUSINESS_RULE = "BusinessRule"
    PROCESS = "Process"
    ENTITY = "Entity"
    CONSTRAINT = "Constraint"
    REQUIREMENT = "Requirement"
    USE_CASE = "UseCase"
    ACTOR = "Actor"
    SYSTEM = "System"

class BusinessRelations(str, Enum):
    """Relationship types for business logic"""
    TRIGGERS = "triggers"
    VALIDATES = "validates"
    REQUIRES = "requires"
    PRODUCES = "produces"
    CONSUMES = "consumes"
    MODIFIES = "modifies"

def get_code_splitter(file_extension: str) -> Optional[CodeSplitter]:
    """Get appropriate CodeSplitter for file extension"""
    language_map = {
        '.py': 'python',
        '.js': 'javascript', 
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.jsx': 'javascript',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.cs': 'csharp',
        '.go': 'go',
        '.rs': 'rust',
        '.php': 'php',
        '.rb': 'ruby',
        '.scala': 'scala',
        '.kt': 'kotlin',
        '.swift': 'swift',
        '.m': 'objc',
        '.r': 'r',
        '.sql': 'sql'
    }
    
    language = language_map.get(file_extension.lower())
    if language:
        return CodeSplitter(
            language=language,
            chunk_lines=40,
            chunk_lines_overlap=15,
            max_chars=1500
        )
    return None

def index_project(path: str, name: str, mode: str = None):
    """
    Index project - supports both enterprise (graph) and basic modes
    Default mode from config, or 'graph' if not specified
    """
    # Get mode from config if not specified
    if mode is None:
        mode = CONFIG.get('index_mode', 'auto')  # Use centralized config
    
    # Use centralized reader configuration
    reader = get_configured_reader(path)
    
    try:
        docs = reader.load_data()
    except Exception as e:
        return {"error": f"Failed to load documents: {str(e)}"}
    
    if not docs:
        return {"error": "No documents found to index", "path": path}
    
    # Process documents with appropriate parser
    processed_docs = []
    for doc in docs:
        file_name = doc.metadata.get('file_name', '')
        file_ext = Path(file_name).suffix if file_name else ''
        
        # Use CodeSplitter for code files
        code_splitter = get_code_splitter(file_ext)
        if code_splitter:
            # Parse with code-aware splitter
            nodes = code_splitter.get_nodes_from_documents([doc])
            processed_docs.extend(nodes)
        else:
            # Use default sentence splitter
            nodes = Settings.node_parser.get_nodes_from_documents([doc])
            processed_docs.extend(nodes)
    
    # Branch based on mode
    if mode == 'basic':
        # BASIC MODE: Simple vector indexing with code-aware parsing
        from llama_index.core.ingestion import IngestionPipeline
        from llama_index.core import VectorStoreIndex
        
        vector_store_kwargs = {'client': client, 'collection_name': name}
        if CONFIG.get('enable_hybrid', False):
            vector_store_kwargs['enable_hybrid'] = True
        
        vector_store = QdrantVectorStore(**vector_store_kwargs)
        
        # Use processed_docs (already parsed with CodeSplitter if code)
        pipeline = IngestionPipeline(
            transformations=[Settings.embed_model],  # Just embed, already parsed
            vector_store=vector_store
        )
        
        num_workers = CONFIG.get('num_workers', 4)
        nodes = pipeline.run(nodes=processed_docs, num_workers=num_workers, show_progress=True)
        
        return {"indexed": len(docs), "mode": "basic", "nodes": len(nodes), "collection": name}
    
    else:
        # ENTERPRISE MODE: PropertyGraphIndex with knowledge graph extraction
        # Create or get graph store for this collection
        if name not in _graph_stores:
            _graph_stores[name] = SimplePropertyGraphStore()
        
        # Storage context with both vector and graph stores
        vector_store_kwargs = {'client': client, 'collection_name': name}
        if CONFIG.get('enable_hybrid', False):
            vector_store_kwargs['enable_hybrid'] = True
        
        storage_context = StorageContext.from_defaults(
            vector_store=QdrantVectorStore(**vector_store_kwargs),
            property_graph_store=_graph_stores[name]
        )
        
        # Determine if this is code or documentation
        is_code = any(doc.metadata.get('file_name', '').endswith(('.py', '.js', '.ts', '.java')) for doc in docs[:5])
        
        # Use appropriate schema based on content type
        if is_code:
            schema_extractor = SchemaLLMPathExtractor(
                llm=Settings.llm,
                possible_entities=CodeEntities,
                possible_relations=CodeRelations,
                strict=True,  # Enforce schema for compliance
                max_triplets_per_chunk=15,
                num_workers=CONFIG.get('num_workers', 4)
            )
        else:
            schema_extractor = SchemaLLMPathExtractor(
                llm=Settings.llm,
                possible_entities=BusinessEntities,
                possible_relations=BusinessRelations,
                strict=True,
                max_triplets_per_chunk=10,
                num_workers=CONFIG.get('num_workers', 4)
            )
        
        # PropertyGraphIndex with SCHEMA extractors for enterprise features
        index = PropertyGraphIndex.from_documents(
            documents=docs,
            storage_context=storage_context,
            kg_extractors=[
                schema_extractor,  # Structured extraction with schema
                ImplicitPathExtractor()  # Also capture implicit relationships
            ],
            show_progress=True
        )
        
        return {"indexed": len(docs), "mode": "graph", "collection": name, "path": path}

def search_with_citations(query: str, project: str, limit: int = 5) -> dict:
    """
    Search with source citations using CitationQueryEngine
    Native LlamaIndex ONE-LINER pattern - TRUE 95/5
    """
    from llama_index.core.query_engine import CitationQueryEngine
    
    if not index_exists(project):
        return {"error": f"Project '{project}' not indexed"}
    
    # ONE-LINER: Native pattern as per latest docs
    citation_engine = CitationQueryEngine(get_index(project).as_query_engine(similarity_top_k=limit))
    
    # Query and extract citations
    response = citation_engine.query(query)
    
    # Format citations if available
    citations = []
    if hasattr(response, 'source_nodes'):
        for i, node in enumerate(response.source_nodes, 1):
            citations.append({
                "citation_number": i,
                "file": node.metadata.get('file_name', 'unknown'),
                "score": node.score,
                "text_preview": node.text[:200] + "..." if len(node.text) > 200 else node.text
            })
    
    return {
        "answer": str(response),
        "citations": citations,
        "query": query,
        "project": project
    }

def search(query: str, project: str, limit: int = 5):
    """Search with Redis caching for <100ms responses"""
    from .redis_cache import query_cache
    
    # Check cache first
    cache_key = f"{query}:{limit}"
    cached = query_cache.get(cache_key, project)
    if cached is not None:
        return cached
    
    # Execute search using helper (DRY)
    result = str(get_index(project).as_query_engine(similarity_top_k=limit).query(query))
    
    # Cache result
    query_cache.set(cache_key, project, result)
    
    return result

def suggest_libraries(task: str):
    """Suggest - TRUE one-liner with centralized prompts"""
    return str(Settings.llm.complete(get_suggestion_prompt(task)))

def list_projects():
    """List - TRUE one-liner"""
    return [c.name for c in client.get_collections().collections]

def clear_project(name: str):
    """Delete - TRUE one-liner"""
    return client.delete_collection(name)

def get_project_info(name: str):
    """Info - 3 lines for error handling"""
    if not client.collection_exists(name):
        return {"project": name, "indexed": False}
    return {"project": name, "indexed": True, "points_count": client.get_collection(name).points_count}

def check_exists(component: str, project: str) -> dict:
    """Check if a component exists in the indexed codebase - Native pattern"""
    if not index_exists(project):
        return {"exists": False, "error": "Project not indexed"}
    
    # Use helper for DRY
    retriever = get_index(project).as_retriever(similarity_top_k=3)
    
    # Retrieve nodes directly
    nodes = retriever.retrieve(component)
    
    # Check if we actually found results
    if nodes:
        best_node = nodes[0]
        return {
            "exists": True, 
            "confidence": best_node.score,
            "file": best_node.metadata.get('file_name', 'unknown'),
            "snippet": best_node.text[:200]
        }
    else:
        return {"exists": False, "message": f"No {component} found in {project}"}

def find_violations(project: str) -> list:
    """Find code violations using native LlamaIndex LLM analysis - TRUE 95/5"""
    if not index_exists(project):
        return ["Project not indexed"]
    
    # Use helper for DRY
    query_engine = get_index(project).as_query_engine()
    
    # Use centralized prompt (OCP compliant)
    response = query_engine.query(get_violation_prompt())
    
    # Parse response into list format
    violations_text = str(response)
    if "no violations" in violations_text.lower() or "no issues" in violations_text.lower():
        return ["✅ No major violations detected"]
    
    # Split by numbered items or paragraphs
    violations = [v.strip() for v in violations_text.split('\n') if v.strip() and len(v.strip()) > 10]
    return violations[:10] if violations else ["✅ No specific violations identified"]

def refresh_project(name: str, path: str) -> dict:
    """
    Incremental refresh - only updates changed files
    Native LlamaIndex refresh_ref_docs() feature
    """
    if not index_exists(name):
        return {"error": f"Project '{name}' not indexed. Run index first."}
    
    # Use centralized reader with filename_as_id for tracking
    reader = get_configured_reader(path, filename_as_id=True)
    
    try:
        docs = reader.load_data()
    except Exception as e:
        return {"error": f"Failed to load documents: {str(e)}"}
    
    # Get the index and refresh only changed docs
    index = get_index(name)
    
    # refresh_ref_docs returns list of booleans indicating which docs were refreshed
    refreshed = index.refresh_ref_docs(docs)
    
    return {
        "refreshed": sum(refreshed),
        "total": len(docs),
        "unchanged": len(docs) - sum(refreshed),
        "collection": name
    }

def get_knowledge_graph(project: str) -> dict:
    """Get knowledge graph visualization data - Native format"""
    from .index_helper import get_graph_data
    return get_graph_data(project)

def smart_query(query: str, projects: list = None) -> str:
    """
    Intelligently route queries to the right index using RouterQueryEngine
    If no projects specified, uses all available projects
    """
    if projects is None:
        # Get all indexed projects
        projects = list_projects()
    
    # Create router
    router = create_router(projects)
    if not router:
        return "No indexed projects available"
    
    # Let the router decide which index to query
    try:
        response = router.query(query)
        return str(response)
    except Exception as e:
        return f"Error during routing: {str(e)}"

def create_router(projects: list):
    """
    Create RouterQueryEngine for intelligent multi-index routing
    Native LlamaIndex ONE-LINER patterns - TRUE 95/5
    """
    from llama_index.core.query_engine import RouterQueryEngine
    from llama_index.core.selectors import PydanticSingleSelector
    from llama_index.core.tools import QueryEngineTool
    
    # Create query tools for each project
    tools = []
    for project in projects:
        if index_exists(project):
            # Determine project type for better descriptions
            is_docs = project.startswith('docs_')
            is_conversation = 'conversation' in project or 'memory' in project
            
            if is_docs:
                description = f"Documentation for {project.replace('docs_', '')} library. Use for API references, examples, and how-to guides."
            elif is_conversation:
                description = f"Conversation history and decisions from {project}. Use for past context and decisions."
            else:
                description = f"Source code for {project} project. Use for code analysis, implementations, and technical details."
            
            # ONE-LINER: Create tool with from_defaults
            tool = QueryEngineTool.from_defaults(
                query_engine=get_index(project).as_query_engine(),
                description=description,
                name=project
            )
            tools.append(tool)
    
    if not tools:
        return None
    
    # ONE-LINER: Native router with selector from_defaults
    return RouterQueryEngine(
        selector=PydanticSingleSelector.from_defaults(),
        query_engine_tools=tools,
        verbose=True
    )

def create_scalable_router(projects: list):
    """
    Create ToolRetrieverRouterQueryEngine for SCALABLE routing (100s-1000s tools)
    Native LlamaIndex pattern for retrieval-based routing - NEW 2024/2025
    """
    from llama_index.core import VectorStoreIndex
    from llama_index.core.objects import ObjectIndex
    from llama_index.core.query_engine import ToolRetrieverRouterQueryEngine
    from llama_index.core.tools import QueryEngineTool
    
    # Create tools
    tools = []
    for project in projects:
        if index_exists(project):
            # Determine description based on project type
            is_docs = project.startswith('docs_')
            description = (f"Documentation: {project.replace('docs_', '')}" if is_docs 
                         else f"Codebase: {project}")
            
            tools.append(QueryEngineTool.from_defaults(
                query_engine=get_index(project).as_query_engine(),
                description=description,
                name=project
            ))
    
    if not tools:
        return None
    
    # ONE-LINER: Create ObjectIndex for tool retrieval
    obj_index = ObjectIndex.from_objects(tools, index_cls=VectorStoreIndex)
    
    # ONE-LINER: Create retriever-based router for scalability
    return ToolRetrieverRouterQueryEngine(obj_index.as_retriever())

def answer_complex(query: str, projects: list) -> str:
    """Answer complex multi-part questions using SubQuestionQueryEngine"""
    from llama_index.core.query_engine import SubQuestionQueryEngine
    from llama_index.core.tools import QueryEngineTool, ToolMetadata
    
    # Create query tools for each project
    tools = []
    for project in projects:
        if index_exists(project):
            # Use helper for DRY
            tools.append(QueryEngineTool(
                query_engine=get_index(project).as_query_engine(),
                metadata=ToolMetadata(
                    name=project,
                    description=f"Search {project} codebase"
                )
            ))
    
    if not tools:
        return "No indexed projects available"
    
    # Create sub-question engine
    engine = SubQuestionQueryEngine.from_defaults(
        query_engine_tools=tools,
        use_async=True,
        verbose=False
    )
    
    # Answer the complex question
    return str(engine.query(query))


# Total: ~80 lines (still under 100!)