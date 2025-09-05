# TASK TRACKER - Complete Missing LlamaIndex Native Features

## 🎯 CURRENT MISSION: Implement Missing Native Patterns
**Strategy**: Use doc_search to find patterns, implement TRUE one-liners, test everything
**Critical**: DO NOT touch semantic_search.py until ALL other features work!

## 📊 IMPLEMENTATION STATUS

### ✅ What's Working:
- Basic indexing and search (49 lines in semantic_search.py)
- doc_search.py with 25,929 vectors
- OpenAI embeddings + ElectronHub LLM (conflict resolved)
- Qdrant hybrid search

### ❌ What's Missing (From VISION.md Table):
1. **IngestionPipeline** - Prevents re-indexing
2. **refresh_ref_docs()** - Updates only changed docs
3. **load_index_from_storage()** - Load saved indexes
4. **persist with persist_dir** - Save indexes properly
5. **RouterQueryEngine** - Route between query types
6. **SubQuestionQueryEngine** - Complex Q&A (needs fixing)
7. **CodeHierarchyNodeParser** - Code structure analysis
8. **PropertyGraphIndex** - Architecture visualization
9. **GraphRAGQueryEngine** - Graph-based Q&A
10. **KnowledgeGraphIndex** - Knowledge integration

## 📝 IMPLEMENTATION PLAN (Based on Doc Search)

### Phase 1: Core Persistence Features
These are foundational - implement first!

#### 1. IngestionPipeline with DocstoreStrategy.UPSERTS
```python
from llama_index.core.ingestion import IngestionPipeline, DocstoreStrategy
from llama_index.core.storage.docstore import SimpleDocumentStore

# Pattern from doc_search:
pipeline = IngestionPipeline(
    transformations=[SentenceSplitter(), Settings.embed_model],
    docstore=SimpleDocumentStore(),
    docstore_strategy=DocstoreStrategy.UPSERTS
)
nodes = pipeline.run(documents=docs)
```
**Purpose**: Prevents re-indexing same documents
**Lines**: ~7-10

#### 2. refresh_ref_docs() for Smart Updates
```python
# Pattern from doc_search:
from llama_index.core import Document

# Documents must have IDs
docs = [Document(text="...", id_="doc_1")]
index.refresh_ref_docs(docs)  # Only updates changed ones
```
**Purpose**: Updates only changed documents
**Lines**: ~3

#### 3. load_index_from_storage
```python
from llama_index.core import StorageContext, load_index_from_storage

# Pattern from doc_search:
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
```
**Purpose**: Load saved indexes
**Lines**: 2

#### 4. persist_index with persist_dir
```python
# Pattern from doc_search:
index.storage_context.persist(persist_dir="./storage")
```
**Purpose**: Save indexes to disk
**Lines**: 1

### Phase 2: Query Engines (After Persistence Works)

#### 5. RouterQueryEngine
```python
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.tools import QueryEngineTool

# Pattern from doc_search:
tools = [
    QueryEngineTool.from_defaults(query_engine=code_engine, description="For code"),
    QueryEngineTool.from_defaults(query_engine=doc_engine, description="For docs")
]
router = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=tools
)
```
**Purpose**: Route queries to appropriate engine
**Lines**: ~10

#### 6. SubQuestionQueryEngine (Fix existing)
```python
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.tools import QueryEngineTool

# Pattern from doc_search:
tools = [QueryEngineTool(...)]
engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=tools,
    use_async=True  # Fix timeout issues
)
```
**Purpose**: Break complex questions into sub-questions
**Lines**: ~8

### Phase 3: Advanced Features (Optional - After Core Works)

#### 7. CodeHierarchyNodeParser
```python
from llama_index.core.node_parser import CodeHierarchyNodeParser

parser = CodeHierarchyNodeParser()
nodes = parser.get_nodes_from_documents(docs)
```
**Purpose**: Parse code structure
**Lines**: 3

#### 8. PropertyGraphIndex
```python
from llama_index.core import PropertyGraphIndex

index = PropertyGraphIndex.from_documents(docs)
```
**Purpose**: Create property graphs
**Lines**: 1

## 🚀 EXECUTION CHECKLIST - COMPLETED (Aug 31, 2025)

### Step 1: Create test_features.py (DO NOT modify semantic_search.py yet!)
- [x] Create new test file to implement features
- [x] Import all necessary modules
- [x] Test each feature independently

### Step 2: Implement Core Features (Phase 1)
- [x] IngestionPipeline with UPSERTS
- [x] refresh_ref_docs()
- [x] load_index_from_storage
- [x] persist with persist_dir

### Step 3: Test Core Features
- [x] Test prevent re-indexing works
- [x] Test smart updates work
- [x] Test save/load works

### Step 4: Implement Query Engines (Phase 2)
- [x] RouterQueryEngine
- [x] Fix SubQuestionQueryEngine

### Step 5: Test Query Engines
- [x] Test routing works
- [x] Test sub-questions work

### Step 6: ONLY NOW Update semantic_search.py
- [x] Add IngestionPipeline to index_project
- [x] Add persist/load functions
- [x] Add refresh function
- [x] Keep under 100 lines total! (Achieved: ~80 lines)

## ⚠️ CRITICAL RULES

1. **DO NOT touch semantic_search.py until Step 6**
2. **Each feature must be TRUE one-liner/minimal**
3. **Test in isolation first**
4. **Use doc_search for patterns**
5. **Total file must stay under 100 lines**

## 📊 SUCCESS METRICS - ALL ACHIEVED!

- [x] All features work in test file
- [x] No re-indexing of same documents
- [x] Smart updates only process changes
- [x] Indexes persist and load correctly
- [x] Query routing works
- [x] semantic_search.py still under 100 lines (~80 lines)

## 🎉 IMPLEMENTATION SUMMARY

### Files Created (DDD Structure):
1. **src/core/ingestion.py** - IngestionPipeline with UPSERTS (21 lines)
2. **src/core/persistence.py** - Save/load indexes (17 lines)
3. **src/core/updates.py** - Smart document updates (9 lines)
4. **src/core/query_engines.py** - Router & SubQuestion engines (28 lines)

### Features Added to semantic_search.py:
- `index_project_smart()` - Index with deduplication
- `save_index()` / `load_saved_index()` - Persistence
- `update_documents()` - Smart updates
- `create_multi_project_router()` - Query routing
- `answer_complex()` - Complex Q&A breakdown

### Total Code:
- **semantic_search.py**: ~80 lines (was 55, now enhanced)
- **DDD modules**: ~75 lines total
- **Total**: ~155 lines for complete solution

## 🔍 DEBUGGING TIPS

If something doesn't work:
1. Use doc_search to find correct pattern
2. Check if imports are correct
3. Verify Settings are configured
4. Test with minimal example first
5. DO NOT create custom implementations