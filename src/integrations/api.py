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

# === BASIC HEALTH ENDPOINTS ===
@app.get("/")
async def root():
    """Root endpoint - API information and basic usage"""
    return {
        "name": "Semantic Search Service",
        "version": "2.0.0", 
        "description": "Enterprise-grade semantic search powered by LlamaIndex PropertyGraphIndex",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "search": "/search",
            "index": "/index"
        },
        "status": "online"
    }

@app.get("/health")
async def health():
    """Health check endpoint with system status"""
    try:
        # Check Qdrant connection
        from src.core.config import get_qdrant_client
        client = get_qdrant_client()
        collections = client.get_collections()
        qdrant_status = "connected"
        collection_count = len(collections.collections)
    except Exception as e:
        qdrant_status = f"error: {str(e)}"
        collection_count = 0
    
    return {
        "status": "healthy",
        "service": "semantic-search-service",
        "timestamp": "2025-01-09T00:00:00Z",
        "components": {
            "qdrant": qdrant_status,
            "collections": collection_count
        }
    }

# Import functions directly - TRUE 95/5 pattern
from src.core import semantic_search, doc_search
from src.core.doc_intelligence import get_doc_intelligence
from src.core.doc_refresh import start_refresh_scheduler
from src.core.diagram_generator import generate_sequence_diagram, generate_mermaid_diagram
from src.core.business_extractor import extract_business_logic, extract_business_rules
from src.core.jsonl_indexer import index_conversations, search_conversations
from src.core.redis_cache import query_cache

@app.on_event("startup")
async def startup_event():
    """Initialize auto-refresh scheduler on startup"""
    start_refresh_scheduler()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown - close connections properly"""
    from src.core.config import close_qdrant_client
    close_qdrant_client()  # Prevent connection warnings

# Request models
class IndexRequest(BaseModel):
    path: str
    name: str

class SearchRequest(BaseModel):
    query: str
    project: str
    limit: int = 5

class SuggestRequest(BaseModel):
    task: str

class EvaluateRequest(BaseModel):
    query: str
    response: str
    reference: Optional[str] = None

class AnalyzeOverviewRequest(BaseModel):
    project_path: str
    include: List[str] = ["structure", "violations", "patterns", "dependencies"]

# === TEMPORAL-HOOKS INTEGRATION ===
@app.get("/check/violation")
async def check_violation(action: str, context: str):
    """Real-time violation check for temporal-hooks - <100ms cached"""
    cache_key = f"violation:{action}:{context}"
    cached = query_cache.get(cache_key, "violations")
    if cached:
        return {"violation": cached, "cached": True, "response_time_ms": 1}
    
    # Check if the specific action would violate principles in the project
    from src.core.index_helper import get_index, index_exists
    
    if not index_exists(context):
        return {"violation": None, "error": f"Project '{context}' not indexed"}
    
    # Query specifically about this action
    query = f"""
    Would the action '{action}' violate SOLID principles, DRY patterns, or best practices 
    in this codebase? If yes, explain why. If no, return 'No violation'.
    Consider: Is this creating duplication? Breaking single responsibility? 
    Creating tight coupling? Violating existing patterns?
    """
    
    response = get_index(context).as_query_engine().query(query)
    result = str(response)
    
    # Determine if it's a violation
    if "no violation" in result.lower() or "would not violate" in result.lower():
        violation = None
    else:
        violation = result
    
    # Cache for fast response
    query_cache.set(cache_key, "violations", violation or "none")
    return {"violation": violation, "cached": False, "action": action, "context": context}

# === INTELLIGENT ROUTING ===
@app.get("/smart/query")
def smart_query_endpoint(query: str):
    """Intelligently route query to appropriate index using RouterQueryEngine"""
    from src.core.semantic_search import smart_query
    result = smart_query(query)
    return {"query": query, "result": result}

@app.get("/smart/scalable")
def scalable_query_endpoint(query: str):
    """Scalable routing for 100s-1000s of indexes using ToolRetrieverRouterQueryEngine"""
    from src.core.semantic_search import create_scalable_router, list_projects
    
    # Get all projects and create scalable router
    projects = list_projects()
    router = create_scalable_router(projects)
    
    if not router:
        return {"error": "No indexed projects available"}
    
    try:
        response = router.query(query)
        return {"query": query, "result": str(response), "mode": "scalable_retrieval"}
    except Exception as e:
        return {"error": str(e)}

# === MEMORY SEARCH ===
@app.get("/search/memory")
def search_memory(query: str, limit: int = 5):
    """Search conversation memory"""
    results = search_conversations(query, "conversations", limit)
    return {"query": query, "results": results}

# === KNOWLEDGE GRAPH ===
@app.get("/graph/{project}")
def get_project_graph(project: str):
    """Get knowledge graph data for visualization - Enterprise feature"""
    from src.core.semantic_search import get_knowledge_graph
    return get_knowledge_graph(project)

@app.get("/graph/{project}/export")
def export_graph_networkx(project: str):
    """Export graph to NetworkX/Cytoscape format - Native feature"""
    from src.core.index_helper import export_to_networkx
    result = export_to_networkx(project)
    if result and "networkx" in result:
        # Remove the actual networkx object, keep the rest
        result.pop("networkx", None)
    return result

@app.get("/graph/{project}/visualize")
def visualize_graph_native(project: str):
    """Native ONE-LINER graph visualization using store.visualize()"""
    from src.core.index_helper import visualize_graph
    return visualize_graph(project)

# === DIAGRAM GENERATION ===
@app.post("/diagram/sequence")
def generate_diagram(project: str, format: str = "json"):
    """Generate sequence diagram - <3s response time"""
    if format == "mermaid":
        diagram = generate_mermaid_diagram(project)
        return {"project": project, "format": "mermaid", "diagram": diagram}
    else:
        return generate_sequence_diagram(project)

# === BUSINESS LOGIC EXTRACTION ===
@app.post("/extract/business-logic")
def extract_logic(project: str):
    """Extract business logic from codebase"""
    return extract_business_logic(project)

# === CONVERSATION INDEXING ===
class ConversationIndexRequest(BaseModel):
    path: str
    collection: str = "conversations"

@app.post("/index/conversations")
def index_convos(req: ConversationIndexRequest):
    """Index JSONL conversations from Claude/Anthropic"""
    return index_conversations(req.path, req.collection)

# === VIOLATION ANALYSIS ===
@app.post("/analyze/violations")
def analyze_violations(project: str):
    """Full codebase violation analysis"""
    violations = semantic_search.find_violations(project)
    rules = extract_business_rules(project)
    return {
        "project": project,
        "violations": violations,
        "business_rules": rules,
        "analysis_complete": True
    }

# === PROPER ENDPOINT PATHS (matching VISION.md) ===
@app.post("/index/project")
def index_project(req: IndexRequest):
    """Index project - proper path matching VISION.md"""
    try:
        result = semantic_search.index_project(req.path, req.name)
        return result
    except Exception as e:
        raise HTTPException(400, str(e))

@app.post("/refresh/project")
def refresh_project_endpoint(req: IndexRequest):
    """Incremental refresh - only updates changed files"""
    try:
        result = semantic_search.refresh_project(req.name, req.path)
        return result
    except Exception as e:
        raise HTTPException(400, str(e))

@app.post("/index/docs")
def index_documentation(library: str, path: str):
    """Index documentation - proper path matching VISION.md"""
    try:
        result = doc_search.index_library_docs(library, path)
        return result
    except Exception as e:
        raise HTTPException(400, str(e))

# Original endpoints (kept for compatibility)
@app.post("/index")
def index(req: IndexRequest):
    try:
        semantic_search.index_project(req.path, req.name)
        return {"indexed": True, "project": req.name}
    except Exception as e:
        raise HTTPException(400, str(e))

@app.post("/search")
def search(req: SearchRequest):
    try:
        result = semantic_search.search(req.query, req.project, req.limit)
        return {"result": result}
    except Exception as e:
        raise HTTPException(400, str(e))

@app.get("/violations/{project}")
def violations(project: str):
    try:
        violations = semantic_search.find_violations(project)
        return {"violations": violations, "count": len(violations)}
    except Exception as e:
        raise HTTPException(400, str(e))

@app.post("/suggest")
def suggest(req: SuggestRequest):
    try:
        suggestions = semantic_search.suggest_libraries(req.task)
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(400, str(e))

@app.get("/exists")
def check_exists(component: str, project: str):
    """Check if a component exists - For task-enforcer integration"""
    try:
        result = semantic_search.check_exists(component, project)
        return result
    except Exception as e:
        raise HTTPException(400, str(e))

class ComplexQueryRequest(BaseModel):
    query: str
    project: str

@app.post("/complex")
def answer_complex_question(req: ComplexQueryRequest):
    """Break complex questions into sub-questions and answer them"""
    try:
        response = semantic_search.answer_complex(req.query, [req.project])
        return {"query": req.query, "project": req.project, "response": response}
    except Exception as e:
        raise HTTPException(400, str(e))

# Documentation search endpoints
class IndexDocsRequest(BaseModel):
    library_name: str
    docs_path: str

class SearchDocsRequest(BaseModel):
    query: str
    library: str
    examples_only: bool = False
    
class HowToRequest(BaseModel):
    task: str
    library: str

class ArchitectureRequest(BaseModel):
    project: str
    output_path: Optional[str] = None

@app.post("/docs/index")
def index_library_docs(req: IndexDocsRequest) -> Dict[str, Any]:
    """Index library documentation for semantic search"""
    try:
        result = doc_search.index_library_docs(req.library_name, req.docs_path)
        return result
    except Exception as e:
        raise HTTPException(400, str(e))

@app.post("/docs/search")
def search_documentation(req: SearchDocsRequest) -> Dict[str, str]:
    """Search library documentation semantically"""
    try:
        result = doc_search.search_docs(req.query, req.library, req.examples_only)
        return {"query": req.query, "library": req.library, "result": result}
    except Exception as e:
        raise HTTPException(400, str(e))

@app.post("/docs/howto")
def how_to_implement(req: HowToRequest) -> Dict[str, str]:
    """Get implementation guide for a specific task"""
    try:
        result = doc_search.how_to(req.task, req.library)
        return {"task": req.task, "library": req.library, "guide": result}
    except Exception as e:
        raise HTTPException(400, str(e))

@app.get("/docs/libraries")
def list_indexed_libraries() -> List[str]:
    """List all indexed documentation libraries"""
    return doc_search.list_indexed_docs()

@app.get("/docs/library/{library}")
def get_library_info(library: str) -> Dict[str, Any]:
    """Get information about an indexed library"""
    info = doc_search.get_library_info(library)
    if "error" in info:
        raise HTTPException(404, info["error"])
    return info

@app.get("/context/project")
def get_project_context(name: str) -> Dict[str, Any]:
    """Get project patterns and conventions - For AI agent context"""
    try:
        info = semantic_search.get_project_info(name)
        if info.get("indexed"):
            # Get project patterns
            patterns = semantic_search.search("project patterns conventions architecture", name, 3)
            return {"project": name, "patterns": patterns, "info": info}
        else:
            return {"project": name, "error": "Project not indexed"}
    except Exception as e:
        raise HTTPException(400, str(e))

# Documentation Intelligence Endpoints

@app.get("/docs/pattern")
def get_documentation_pattern(query: str, framework: str = "llamaindex") -> Dict[str, Any]:
    """Get precise documentation pattern - prevents AI from guessing"""
    try:
        doc_intel = get_doc_intelligence()
        pattern = doc_intel.search_pattern(query, framework)
        return {
            "query": query,
            "framework": framework,
            "pattern": pattern
        }
    except Exception as e:
        raise HTTPException(400, str(e))

@app.get("/docs/exists")
def check_component_in_docs(component: str, framework: str = "llamaindex") -> Dict[str, Any]:
    """Check if component exists in framework documentation"""
    try:
        doc_intel = get_doc_intelligence()
        return doc_intel.check_exists(component, framework)
    except Exception as e:
        raise HTTPException(400, str(e))

@app.post("/docs/index-framework")
def index_framework_documentation(framework: str, url: Optional[str] = None) -> Dict[str, Any]:
    """Index a framework's documentation"""
    try:
        doc_intel = get_doc_intelligence()
        return doc_intel.index_framework(framework, url)
    except Exception as e:
        raise HTTPException(400, str(e))

@app.get("/docs/frameworks")
def list_documented_frameworks() -> List[str]:
    """List all indexed documentation frameworks"""
    doc_intel = get_doc_intelligence()
    return doc_intel.list_frameworks()

@app.get("/docs/framework/{framework}")
def get_framework_documentation_info(framework: str) -> Dict[str, Any]:
    """Get information about indexed framework documentation"""
    doc_intel = get_doc_intelligence()
    info = doc_intel.get_framework_info(framework)
    if not info.get("indexed"):
        raise HTTPException(404, f"Framework '{framework}' not indexed")
    return info

@app.post("/analyze/overview")
def analyze_overview(req: AnalyzeOverviewRequest) -> Dict[str, Any]:
    """Generate basic project overview without complex operations"""
    try:
        result = {}
        project_path = Path(req.project_path)
        
        # Get project structure
        if "structure" in req.include:
            try:
                tree_cmd = ['tree', '-L', '2', '-I', '__pycache__|*.pyc|.git|.venv|venv|node_modules|*.lock', str(project_path)]
                tree_result = subprocess.run(tree_cmd, capture_output=True, text=True, timeout=2)
                result["structure"] = tree_result.stdout if tree_result.returncode == 0 else "Unable to generate tree"
            except:
                result["structure"] = "Tree command not available"
        
        # Native semantic pattern detection using PropertyGraphIndex
        if "patterns" in req.include:
            project_name = project_path.name
            from src.core.index_helper import get_index, index_exists
            
            if index_exists(project_name):
                query_engine = get_index(project_name).as_query_engine()
                patterns_response = query_engine.query("Identify architectural patterns, frameworks, and design patterns used in this codebase")
                result["patterns"] = [str(patterns_response)]
            else:
                result["patterns"] = [f"Project '{project_name}' not indexed for semantic analysis"]
        
        # Native violation detection using PropertyGraphIndex and sophisticated prompts
        if "violations" in req.include:
            project_name = project_path.name
            from src.core.semantic_search import find_violations
            result["violations"] = find_violations(project_name)
        
        # Identify important files
        result["important_files"] = {
            "Documentation": [f.name for f in (project_path / "docs").glob("*.md")][:3] if (project_path / "docs").exists() else [],
            "API": [str(f.relative_to(project_path)) for f in project_path.glob("**/*.py") if "api" in f.name.lower() and ".git" not in str(f) and "venv" not in str(f)][:3],
            "Core": [str(f.relative_to(project_path)) for f in project_path.glob("**/*search*.py") if ".git" not in str(f) and "venv" not in str(f)][:3]
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(500, f"Overview generation failed: {str(e)}")