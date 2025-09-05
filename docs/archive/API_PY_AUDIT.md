# api.py - Code Audit Report

## 📊 File Overview
- **Lines**: 198
- **Purpose**: FastAPI REST endpoints
- **Complexity**: Low-Medium

## 🔴 CRITICAL ISSUES

### 1. **Global Service Instances (Lines 17-18)**
```python
service = SemanticSearch()
doc_service = DocumentationSearch()
```
**Problem**: Creating service instances at module level
**Impact**: 
- Services initialized even when importing for testing
- Can't use dependency injection
- Hard to mock for tests
**Fix**: Use FastAPI dependency injection

### 2. **Generic Exception Handling EVERYWHERE**
```python
except Exception as e:
    raise HTTPException(400, str(e))  # Used 12+ times!
```
**Problem**: 
- All errors become 400 Bad Request (even 500 errors)
- Loses exception type information
- No proper logging
**Fix**: Specific exception handling with appropriate status codes

### 3. **Bare except: Statement (Line 163)**
```python
except:  # Line 163 - catches EVERYTHING
    result["structure"] = "Tree command not available"
```
**Problem**: Catches all exceptions including system exits
**Fix**: Use specific exception

## 🟡 MODERATE ISSUES

### 4. **subprocess.run Without Shell Safety (Line 161)**
```python
tree_cmd = ['tree', '-L', '2', '-I', '...', str(project_path)]
subprocess.run(tree_cmd, capture_output=True, text=True, timeout=2)
```
**Problem**: 
- No validation of project_path
- Could potentially access system paths
**Fix**: Validate paths, use safe directory listing

### 5. **Hardcoded Magic Values**
```python
'-L', '2'  # Line 160 - magic number
limit: int = 5  # Line 28 - magic default
timeout=2  # Line 161 - magic timeout
```
**Problem**: Magic values scattered
**Fix**: Define as constants

### 6. **Missing Return Type Hints**
Many endpoints missing return type hints
```python
@app.post("/index")  # No return type
def index(req: IndexRequest):
```
**Fix**: Add proper type hints

## 🟢 GOOD PATTERNS (Keep These)

1. ✅ Using Pydantic models for validation
2. ✅ Clear endpoint organization
3. ✅ Descriptive docstrings

## 📊 METRICS

| Issue Type | Count | Severity |
|------------|-------|----------|
| Global instances | 2 | High |
| Generic exceptions | 12+ | High |
| Bare except | 1 | High |
| Missing types | 8 | Low |
| Magic values | 5 | Low |

## 🎯 PRIORITY FIXES

### Fix #1: Use Dependency Injection
```python
from fastapi import Depends

def get_semantic_search() -> SemanticSearch:
    return SemanticSearch()

def get_doc_search() -> DocumentationSearch:
    return DocumentationSearch()

@app.post("/search")
def search(
    req: SearchRequest,
    service: SemanticSearch = Depends(get_semantic_search)
):
    # Now testable and mockable
```

### Fix #2: Proper Exception Handling
```python
import logging
logger = logging.getLogger(__name__)

try:
    result = service.search(...)
except ValueError as e:
    logger.warning(f"Invalid search request: {e}")
    raise HTTPException(400, f"Invalid request: {e}")
except ConnectionError as e:
    logger.error(f"Service connection error: {e}")
    raise HTTPException(503, "Service temporarily unavailable")
except Exception as e:
    logger.exception("Unexpected error in search")
    raise HTTPException(500, "Internal server error")
```

### Fix #3: Define Constants
```python
# At top of file
DEFAULT_SEARCH_LIMIT = 5
TREE_DEPTH_LIMIT = 2
SUBPROCESS_TIMEOUT = 2.0
MAX_IMPORTANT_FILES = 3
```

### Fix #4: Add Return Types
```python
@app.post("/search") -> Dict[str, Any]:
@app.get("/violations/{project}") -> Dict[str, Union[List[str], int]]:
```

## 💡 ESTIMATED IMPACT
- **Testability**: 100% improvement with dependency injection
- **Error handling**: Proper status codes and logging
- **Maintainability**: Much better with constants
- **Type safety**: Full with return types

## 🚨 SECURITY CONCERN

The `analyze_overview` endpoint with subprocess.run could be a security risk if project_path isn't validated. Should add:
```python
# Validate path is within allowed directory
if not project_path.resolve().is_relative_to(Path.cwd()):
    raise HTTPException(403, "Access to path not allowed")
```