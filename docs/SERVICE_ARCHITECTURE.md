# Service Architecture - Correct Pattern Hierarchy

## Our Use Case: MCP Server & API Service

We are building a **SERVICE**, not an application. This changes the pattern hierarchy:

### ✅ CORRECT Hierarchy for Services

1. **MCP/API Endpoints** (Highest Level)
   - Thin wrappers around core functions
   - Lazy initialization
   - No business logic
   
2. **CLI Wrappers** (For Testing/Admin)
   - `./search` bash script
   - Simple Python CLI for operations
   
3. **Core SDK Functions** (The Actual Service)
   - `semantic_search.py` - Core indexing/search
   - `doc_search.py` - Documentation wrapper
   - Simple, stateless functions
   - Native LlamaIndex one-liners

### ❌ WRONG Approach (What we were doing)

Adding complex query engines directly to semantic_search.py. These belong in the APPLICATION layer, not the service layer!

## Architecture Layers

```
┌─────────────────────────────────┐
│         MCP Clients             │  <- Claude, other AI assistants
├─────────────────────────────────┤
│      MCP Server (mcp_server.py) │  <- Thin wrapper, lazy init
├─────────────────────────────────┤
│         HTTP Clients            │  <- Web apps, tools
├─────────────────────────────────┤
│      FastAPI (api.py)           │  <- Thin wrapper, lazy init
├─────────────────────────────────┤
│      Core Service Layer         │
│   - semantic_search.py          │  <- Simple functions
│   - doc_search.py               │  <- No complex logic
│   - conversation_memory.py      │  <- Just the essentials
└─────────────────────────────────┘
```

## What Goes Where

### Core Service (semantic_search.py)
✅ Basic operations:
- `index_project()` - Index documents
- `search()` - Simple search
- `find_violations()` - Business logic
- `suggest_libraries()` - Custom prompts

❌ NOT in core service:
- SubQuestionQueryEngine
- RouterQueryEngine  
- Complex orchestration
- Application-specific logic

### MCP/API Layer
✅ What belongs here:
- Endpoint definitions
- Parameter validation
- Response formatting
- Lazy initialization

❌ What doesn't:
- Business logic
- Complex query engines
- Direct LlamaIndex imports

### When to Use Advanced Query Engines

Advanced query engines (SubQuestion, Router, etc.) should be used:
1. **In the APPLICATION** that consumes our service
2. **By the CLIENT** (like Claude) orchestrating multiple calls
3. **NOT in the service itself**

Example:
```python
# ❌ WRONG - In semantic_search.py service
def answer_complex(question):
    return SubQuestionQueryEngine.from_defaults(...).query(question)

# ✅ RIGHT - In the client application
# Claude or app makes multiple service calls and combines results
response1 = mcp.search_code("part 1 of question")
response2 = mcp.search_code("part 2 of question")
# Client combines and reasons about responses
```

## Native LlamaIndex Patterns We DO Use

### In Core Service (Simple, One-Line)
```python
# Indexing
VectorStoreIndex.from_documents(docs, storage_context=storage_context)

# Search
index.as_query_engine().query("question")

# Settings singleton
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
```

### In Client Applications (Complex, Multi-Step)
```python
# These belong in the APPLICATION, not our service
SubQuestionQueryEngine.from_defaults(tools)
RouterQueryEngine(selector, tools)
ReActAgent.from_tools(tools)
```

## Key Principles

1. **Services should be simple** - Just index and search
2. **Complexity belongs in clients** - Let Claude orchestrate
3. **MCP/API are thin wrappers** - No logic, just translation
4. **One function, one purpose** - No kitchen sinks
5. **Lazy initialization** - Load only when needed

## File Purposes

| File | Purpose | LOC | Complexity |
|------|---------|-----|------------|
| semantic_search.py | Core index/search | ~150 | Simple |
| doc_search.py | Doc-specific wrapper | ~90 | Simple |
| mcp_server.py | MCP interface | ~40 | Thin wrapper |
| api.py | HTTP interface | ~180 | Thin wrapper |
| conversation_memory.py | Claude integration | ~190 | Integration |
| architecture.py | Simple analysis | ~50 | Simple wrapper |

## Summary

We're building a **service**, not an application. Keep it simple:
- Core functions do one thing well
- MCP/API are just interfaces
- Complex orchestration happens in clients
- No unnecessary abstractions

The TRUE 95/5 principle for services: 95% of complexity should be in the framework (LlamaIndex) or the client (Claude), only 5% in our service code.