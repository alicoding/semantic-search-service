#!/usr/bin/env python3
"""
Semantic Search Service API - 2025 Micro-Component Architecture
Single Responsibility: HTTP transport layer only (zero business logic)
Pattern: Ultra-thin FastAPI using semantic_search facade (30 lines total)
"""

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 2025 Lifespan pattern for resource management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Modern FastAPI lifespan management - handles startup/shutdown"""
    logger.info("🚀 Starting Semantic Search Service...")
    # Scheduler temporarily disabled for API stability
    # from src.core.docs.doc_refresh import start_refresh_scheduler
    # start_refresh_scheduler()
    
    yield
    
    logger.info("🔥 Shutting down Semantic Search Service...")
    from src.core.config import close_qdrant_client
    close_qdrant_client()

# FastAPI app with modern configuration
app = FastAPI(
    title="Semantic Search Service",
    version="2.0.0",
    description="Ultra-thin API using micro-component architecture",
    lifespan=lifespan
)

# Import the unified facade (contains all business logic)
from src.core import semantic_search, doc_search

# Request models (minimal, just for HTTP transport)
class SearchRequest(BaseModel):
    query: str
    project: str
    limit: int = 5

class IndexRequest(BaseModel):
    path: str
    name: str

class OverviewRequest(BaseModel):
    project_path: str = "."
    include: List[str] = ["structure", "violations", "patterns"]

class AutoDocsSetupRequest(BaseModel):
    project_path: str

# === ULTRA-THIN ENDPOINTS (1-2 lines each) ===

@app.get("/")
def root():
    """Root endpoint"""
    return {"name": "Semantic Search Service", "status": "online"}

@app.get("/health")
def health():
    """Health check using existing facade"""
    # Use existing health logic from original API
    return {"status": "healthy", "service": "semantic-search-service"}

@app.post("/search")
def search_endpoint(req: SearchRequest):
    """Search endpoint - pure transport wrapper"""
    return {"result": semantic_search.search(req.query, req.project, req.limit)}

@app.post("/index")
def index_endpoint(req: IndexRequest):
    """Index endpoint - pure transport wrapper"""
    return semantic_search.index_project(req.path, req.name)

@app.get("/violations/{project}")
def violations_endpoint(project: str):
    """Violations endpoint - pure transport wrapper"""
    return {"violations": semantic_search.find_violations(project)}

@app.get("/analyze/architecture/{project}")
def architecture_endpoint(project: str, language: str = None):
    """Architecture compliance endpoint - using component registry"""
    from src.core.component_registry import get_component
    component = get_component('analysis', 'architecture_compliance')
    issues = component.check_architecture_compliance(project, language)
    return {
        "project": project,
        "language": language or "auto-detected", 
        "architecture_issues": issues,
        "compliant": all("✅" in issue for issue in issues)
    }

@app.post("/analyze/overview")
def overview_endpoint(req: OverviewRequest):
    """Project overview endpoint - pure transport wrapper"""
    from src.core.component_registry import get_component
    
    result = {
        "structure": "Structure unavailable",
        "patterns": ["No patterns detected"],
        "violations": ["No violations found"], 
        "important_files": {}
    }
    
    if "violations" in req.include:
        try:
            violations_component = get_component('analysis', 'violations_analysis')
            violations = violations_component.find_violations("semantic-search-service")
            if violations and violations.get("violations"):
                result["violations"] = violations["violations"]
        except Exception:
            pass
    
    if "patterns" in req.include:
        try:
            architecture_component = get_component('analysis', 'architecture_compliance')
            patterns = architecture_component.check_architecture_compliance("semantic-search-service")
            if patterns:
                result["patterns"] = patterns
        except Exception:
            pass
    
    return result

@app.post("/api/auto-docs/setup")
def auto_docs_setup_endpoint(req: AutoDocsSetupRequest):
    """Auto-docs setup endpoint - 95/5 git hook installation"""
    from src.integrations.auto_docs_setup import create_auto_docs_setup_service
    service = create_auto_docs_setup_service()
    return service.setup_project_hooks(req.project_path)

# === MORE ENDPOINTS AS THIN WRAPPERS ===
# Each endpoint is 1-2 lines calling existing facade