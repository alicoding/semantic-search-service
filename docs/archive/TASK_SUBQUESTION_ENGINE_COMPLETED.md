# TASK TRACKER - Living Documentation & Native Features Implementation

## 🎯 NEXT SESSION: Implement SubQuestionQueryEngine
**Start with Task 1 below** - All implementation steps provided!

## Current Sprint: Auto-Documentation System + Pending Features

### Completed This Session:
- ✅ Auto-documentation system (`auto_docs.py`)
- ✅ Git hooks for automatic updates
- ✅ Living documentation (1300+ lines)
- ✅ Updated CLAUDE.md with mandatory workflow
- ✅ Reduced codebase from 1,319 → 837 LOC (36% reduction)

### Carried Forward (Uncompleted from Previous Sprint)

#### Task 1: Implement SubQuestionQueryEngine
**Status**: 🎯 NEXT PRIORITY - START HERE!
**Goal**: Add complex question handling (~10 lines)

**Implementation Steps**:
1. First, search LlamaIndex docs for correct pattern:
   ```python
   from src.core.doc_search import how_to
   print(how_to("use SubQuestionQueryEngine to break complex questions", "llamaindex"))
   ```

2. Add to `src/core/semantic_search.py`:
   ```python
   def answer_complex(query: str, project: str) -> str:
       """Break complex questions into sub-questions."""
       from llama_index.core.query_engine import SubQuestionQueryEngine
       from llama_index.core.tools import QueryEngineTool
       
       # Get existing index
       if not client.collection_exists(project):
           return f"Project '{project}' not found. Index it first."
       
       index = VectorStoreIndex.from_vector_store(
           QdrantVectorStore(client=client, collection_name=project)
       )
       
       # Create tool for the query engine
       tool = QueryEngineTool.from_defaults(
           query_engine=index.as_query_engine(),
           description=f"Search {project} codebase"
       )
       
       # Create sub-question engine
       engine = SubQuestionQueryEngine.from_defaults([tool])
       return str(engine.query(query))
   ```

3. Add to API (`src/integrations/api.py`):
   ```python
   @app.post("/complex")
   def answer_complex_question(req: ComplexQueryRequest):
       # Implementation here
   ```

4. Add to CLI (`src/integrations/cli.py`):
   ```python
   @app.command()
   def complex(query: str, project: str):
       # Implementation here
   ```

5. Test the implementation:
   ```bash
   # Test with a complex multi-part question
   python -c "from src.core.semantic_search import answer_complex; 
              print(answer_complex('What are the main components and how do they interact?', 'semantic-search-service'))"
   ```

**Success Criteria**:
- Function added to semantic_search.py
- API endpoint working
- CLI command working
- Handles multi-part questions
- Documentation auto-updates

#### Task 2: Add RouterQueryEngine
**Status**: ⏳ PENDING
**Goal**: Route between code search and doc search automatically (~10 lines)

#### Task 3: Implement IngestionPipeline
**Status**: ⏳ PENDING
**Goal**: Replace manual document processing (~20 lines)

#### Task 4: Create Integration Tests
**Status**: ⏳ PENDING
**Test Coverage Needed**:
```
tests/
├── test_semantic_search.py    # Core functionality
├── test_doc_search.py         # Documentation search
├── test_conversation_memory.py # Claude integration
├── test_api.py                # FastAPI endpoints
└── test_mcp_server.py         # MCP protocol
```

---

### New Priority Task: Living Documentation System

#### Task 5: Implement Auto-Documentation Generator
**Status**: ✅ COMPLETED
**Goal**: Create self-maintaining documentation using LlamaIndex patterns

**Result**: 
- Created `src/core/auto_docs.py` (100 lines)
- Uses native CodeHierarchyNodeParser from LlamaIndex
- Generates complete API documentation automatically
- Successfully generated 1300+ line API_REFERENCE.md
- TRUE 95/5 pattern - no custom parsing!

**Implementation Plan**:
```python
# src/core/auto_docs.py
from llama_index.core import SimpleDirectoryReader, Document
from llama_index.core.node_parser import CodeHierarchyNodeParser
from llama_index.core.ingestion import DocstoreStrategy
import ast
import inspect

def generate_api_docs() -> str:
    """Auto-generate API documentation from our codebase."""
    # 1. Parse Python files
    parser = CodeHierarchyNodeParser(language="python")
    docs = SimpleDirectoryReader("src", recursive=True).load_data()
    code_nodes = parser.get_nodes_from_documents(docs)
    
    # 2. Extract functions, classes, methods
    # 3. Generate markdown documentation
    # 4. Return formatted docs
```

**Features to Document**:
1. All public functions in semantic_search.py
2. All public functions in doc_search.py  
3. All public functions in conversation_memory.py
4. API endpoints from api.py
5. CLI commands from cli.py
6. MCP server tools from mcp_server.py

**Auto-Update Strategy**:
```python
def refresh_documentation():
    """Refresh docs when code changes."""
    # Use refresh_ref_docs pattern
    # Monitor src/ directory
    # Update only changed files
```

---

## Success Metrics

### From Previous Sprint (Completed ✅):
- [x] All files follow native patterns (violation FIXED!)
- [x] Reduced LOC from 1,313 → 837 (36% reduction!)
- [x] enterprise_architecture.py: 112 → 33 lines (71% reduction)

### Current Sprint Goals:
- [x] Auto-documentation system working ✅
- [x] Living documentation generated (1300+ lines)
- [ ] SubQuestionQueryEngine implemented (~10 lines)
- [ ] RouterQueryEngine implemented (~10 lines)
- [ ] IngestionPipeline implemented (~20 lines)
- [ ] Integration tests passing
- [ ] VISION.md updated with all features

---

## Workflow (Per CLAUDE.md)
1. ✅ Archive completed TASK.md → docs/archive/
2. ✅ Create new TASK.md with uncompleted + new tasks
3. ✅ Update VISION.md capability table (auto_docs.py added)
4. ✅ Test implementation (Git hooks tested and working!)
5. ✅ Update CLAUDE.md with workflow (auto-docs now mandatory)

---

## Notes
- Following TRUE 95/5 principle
- Using native LlamaIndex patterns only
- No custom code where native exists
- Test before marking complete