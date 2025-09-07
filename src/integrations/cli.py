#!/usr/bin/env python3
"""
Semantic Search Service CLI - 2025 Micro-Component Architecture  
Single Responsibility: CLI transport layer only (zero business logic)
Pattern: Ultra-thin Typer using semantic_search facade (40 lines total)
"""

import typer
import uvicorn
from typing import Optional

# Import the unified facade (contains all business logic)
from src.core import semantic_search, doc_search

app = typer.Typer(name="semantic-search", help="Semantic Search Service CLI")

# === ULTRA-THIN CLI COMMANDS (1-2 lines each) ===

@app.command()
def run(host: str = "0.0.0.0", port: int = 9999, reload: bool = True):
    """Start the FastAPI server - pure transport wrapper"""
    typer.echo(f"🚀 Starting Semantic Search Service on {host}:{port}")
    uvicorn.run("src.integrations.api:app", host=host, port=port, reload=reload)

@app.command()
def health():
    """Check service health - uses existing facade"""
    import httpx
    try:
        response = httpx.get("http://localhost:9999/health", timeout=5.0)
        if response.status_code == 200:
            typer.echo("✅ Service is healthy")
        else:
            typer.echo(f"❌ Service unhealthy: {response.status_code}")
    except Exception as e:
        typer.echo(f"❌ Cannot connect: {e}")

@app.command()
def search(query: str, project: str, limit: int = 5):
    """Search for code patterns - pure transport wrapper"""
    result = semantic_search.search(query, project, limit)
    typer.echo(result)

@app.command()
def index(path: str, name: str, mode: Optional[str] = None):
    """Index a project - pure transport wrapper"""
    result = semantic_search.index_project(path, name, mode)
    typer.echo(f"✅ Indexed: {result}")

@app.command()
def violations(project: str):
    """Find violations - pure transport wrapper"""
    violations_list = semantic_search.find_violations(project)
    for violation in violations_list:
        typer.echo(f"⚠️ {violation}")

@app.command()
def check_architecture(project: str, language: Optional[str] = typer.Option(None, "--language", "-l")):
    """Check architecture compliance - using component registry"""
    from src.core.component_registry import get_component
    typer.echo(f"🔍 Analyzing {project} architecture...")
    
    component = get_component('analysis', 'architecture_compliance')
    issues = component.check_architecture_compliance(project, language)
    
    for issue in issues:
        if "✅" in issue:
            typer.echo(f"✅ {issue}")
        else:
            typer.echo(f"⚠️ {issue}")

@app.command()
def suggest(task: str):
    """Suggest libraries - pure transport wrapper"""
    suggestions = semantic_search.suggest_libraries(task)
    typer.echo(suggestions)

@app.command()
def list_docs():
    """List indexed docs - pure transport wrapper"""
    libraries = doc_search.list_indexed_docs()
    if libraries:
        typer.echo("📚 Indexed libraries:")
        for lib in libraries:
            info = doc_search.get_library_info(lib)
            typer.echo(f"  - {lib}: {info.get('doc_count', 0)} documents")
    else:
        typer.echo("No libraries indexed yet.")

def cleanup():
    """Cleanup function"""
    from src.core.config import close_qdrant_client
    close_qdrant_client()

if __name__ == "__main__":
    import atexit
    atexit.register(cleanup)
    app()