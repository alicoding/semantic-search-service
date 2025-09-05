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
    result = semantic_search.refresh_project(name, path)
    typer.echo(f"Refresh result: {result}")

@app.command()
def search(query: str, project: str, limit: int = 5):
    """Search for code patterns."""
    result = semantic_search.search(query, project, limit)
    typer.echo(result)

@app.command()
def smart(query: str):
    """Smart query - automatically routes to the right index."""
    result = semantic_search.smart_query(query)
    typer.echo(result)

@app.command()
def violations(project: str):
    """Find SOLID/DRY/DDD violations."""
    violations = semantic_search.find_violations(project)
    for v in violations:
        typer.echo(f"❌ {v}")

@app.command()
def suggest(task: str):
    """Suggest libraries for a task."""
    suggestions = semantic_search.suggest_libraries(task)
    typer.echo(suggestions)

@app.command()
def complex(query: str, project: str):
    """Answer complex multi-part questions by breaking them into sub-questions."""
    result = semantic_search.answer_complex(query, [project])
    typer.echo(result)

# Documentation search commands
@app.command()
def index_docs(library: str, path: str):
    """Index library documentation for semantic search."""
    result = doc_search.index_library_docs(library, path)
    typer.echo(f"✅ Indexed {library} docs: {result['total_docs']} documents")

@app.command()
def search_docs(query: str, library: str = "llamaindex"):
    """Search library documentation."""
    result = doc_search.search_docs(query, library)
    typer.echo(result)

@app.command()
def howto(task: str, library: str = "llamaindex"):
    """Get implementation guide for a task."""
    result = doc_search.how_to(task, library)
    typer.echo(result)

@app.command()
def list_docs():
    """List indexed documentation libraries."""
    libraries = doc_search.list_indexed_docs()
    if libraries:
        typer.echo("📚 Indexed libraries:")
        for lib in libraries:
            info = doc_search.get_library_info(lib)
            typer.echo(f"  - {lib}: {info.get('doc_count', 0)} documents")
    else:
        typer.echo("No libraries indexed yet. Use 'index_docs' command first.")

@app.command()
def exists(component: str, project: str):
    """Check if a component exists in the codebase."""
    result = semantic_search.check_exists(component, project)
    if result["exists"]:
        typer.echo(f"✅ Found: {component}")
        if "file" in result:
            typer.echo(f"  File: {result['file']}")
        if "snippet" in result:
            typer.echo(f"  Context: {result['snippet']}")
    else:
        typer.echo(f"❌ Not found: {component}")
        if "error" in result:
            typer.echo(f"  Error: {result['error']}")

@app.command()
def diagram(project: str, format: str = "mermaid"):
    """Generate sequence diagram for project."""
    from src.core.diagram_generator import generate_sequence_diagram, generate_mermaid_diagram
    
    typer.echo(f"📊 Generating {format} diagram for {project}...")
    
    if format == "mermaid":
        result = generate_mermaid_diagram(project)
    else:
        result = generate_sequence_diagram(project)
    
    if isinstance(result, dict) and "error" in result:
        typer.echo(f"❌ {result['error']}")
    else:
        typer.echo(result if isinstance(result, str) else str(result))

@app.command()
def business(project: str, type: str = "logic"):
    """Extract business logic from project."""
    from src.core.business_extractor import extract_business_logic, extract_business_rules
    
    typer.echo(f"💼 Extracting business {type} from {project}...")
    
    if type == "rules":
        results = extract_business_rules(project)
        for rule in results:
            typer.echo(f"  • {rule}")
    else:
        result = extract_business_logic(project)
        if "error" in result:
            typer.echo(f"❌ {result['error']}")
        else:
            typer.echo(result.get("business_logic", "No logic extracted"))

@app.command()
def index_conversations(jsonl_path: str, collection: str = "conversations"):
    """Index JSONL conversations from Claude/Anthropic."""
    from src.core.jsonl_indexer import index_conversations as idx_convos
    
    typer.echo(f"💬 Indexing conversations from {jsonl_path}...")
    result = idx_convos(jsonl_path, collection)
    
    if "error" in result:
        typer.echo(f"❌ {result['error']}")
    else:
        typer.echo(f"✅ Indexed {result.get('messages', 0)} messages from {result.get('conversations', 0)} conversations")

@app.command()
def check_violation(action: str, context: str):
    """Check for violations in real-time (temporal-hooks integration)."""
    import httpx
    
    typer.echo(f"🔍 Checking violation for action='{action}' in context='{context}'...")
    
    try:
        response = httpx.get(f"http://localhost:8000/check/violation?action={action}&context={context}")
        data = response.json()
        
        if data.get("violation"):
            typer.echo(f"⚠️ Violation detected: {data['violation']}")
            if data.get("cached"):
                typer.echo("  (cached response)")
        else:
            typer.echo("✅ No violations detected")
    except Exception as e:
        typer.echo(f"❌ Error: {e}")

def cleanup():
    """Cleanup function called on exit"""
    from src.core.config import close_qdrant_client
    close_qdrant_client()

if __name__ == "__main__":
    import atexit
    atexit.register(cleanup)  # Register cleanup on exit
    app()