# mcp_server.py - Code Audit Report

## 📊 File Overview
- **Lines**: 39
- **Purpose**: MCP (Model Context Protocol) server wrapper
- **Complexity**: Low

## 🔴 CRITICAL ISSUES

### 1. **Global Service Instance (Line 13)**
```python
service = SemanticSearch()
```
**Problem**: Service initialized at module level
**Impact**: 
- Can't use dependency injection
- Initialized even when importing for tests
- Hard to mock
**Fix**: Create service inside functions or use lazy initialization
**LlamaIndex Pattern**: Services should be created on-demand

## 🟡 MODERATE ISSUES

### 2. **No Error Handling**
All functions lack try/except blocks
**Problem**: Errors will crash the MCP server
**Fix**: Add proper error handling with meaningful messages

### 3. **Return Type Hints Missing**
```python
@mcp.tool()
def index_project(project_path: str, ...) -> str:  # Only return type present
```
**Problem**: Inconsistent type hints
**Fix**: Add complete type hints

### 4. **Magic Values**
```python
limit: int = 5  # Line 23 - magic default
```
**Problem**: Hardcoded default
**Fix**: Define as constant

## 🟢 GOOD PATTERNS

1. ✅ Clean, simple wrapper
2. ✅ Good use of FastMCP decorators
3. ✅ Clear function names
4. ✅ Minimal code (39 lines)

## 🎯 RECOMMENDED REFACTOR

### Lazy Service Initialization
```python
from functools import lru_cache

@lru_cache(maxsize=1)
def get_service() -> SemanticSearch:
    """Lazy initialization of service."""
    return SemanticSearch()

@mcp.tool()
def index_project(project_path: str, collection_name: Optional[str] = None) -> str:
    """Index a project for semantic search."""
    try:
        service = get_service()
        name = collection_name or Path(project_path).name
        count = service.index_project(project_path, name)
        return f"Indexed {count} documents in '{name}'"
    except Exception as e:
        return f"Error indexing project: {str(e)}"
```

## 💡 IMPACT
- Better testability
- Graceful error handling
- Lazy initialization saves resources

## 📊 METRICS
| Issue Type | Count | Severity |
|------------|-------|----------|
| Global instance | 1 | High |
| No error handling | 4 | Medium |
| Missing types | 3 | Low |
| Magic values | 1 | Low |