# LlamaIndex Patterns - Local Documentation Reference

## 📚 Where to Find Each Pattern in Our Indexed Docs

Based on searching our locally indexed LlamaIndex documentation (llamaindex_complete collection), here's where each pattern is documented:

## 1. **VectorStoreIndex.from_documents** ✅ FOUND
**Local Doc Search Result:**
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Load documents from a specified directory
documents = SimpleDirectoryReader(directory_path).load_data()
index = VectorStoreIndex.from_documents(documents)
```
**What it does:** Creates index from documents, handles chunking into Node objects, builds vector-based index for efficient retrieval.

## 2. **IngestionPipeline Deduplication** ✅ FOUND
**Local Doc Search Result:**
- Uses unique identifiers for each document
- Maintains mapping between IDs and content hashes
- If document changes (different hash), re-processes and updates
- If duplicate ID with same content, skips processing

**Implementation:**
```python
pipeline = IngestionPipeline(
    transformations=[...],
    docstore=RedisDocumentStore()  # Handles dedup
)
```

## 3. **PropertyGraphIndex** ✅ FOUND
**Local Doc Search Result:**
- Builds property graphs with labeled nodes and relationships
- **Construct:** `PropertyGraphIndex.from_documents()` with extractors
- **Query:** Retrieve nodes and execute graph queries
- Enriches nodes with metadata

**Our Usage:**
```python
graph = PropertyGraphIndex.from_documents(
    docs,
    kg_extractors=[ImplicitPathExtractor(), SchemaLLMPathExtractor()]
)
```

## 4. **Settings Singleton Global Configuration** ✅ FOUND
**Local Doc Search Result:**
- Central singleton for global configuration
- Encapsulates LLM, embedding model, node parser, tokenizer
- Lazily instantiated (only loaded when required)
- Optimizes resource usage

**Our Usage:**
```python
from llama_index.core import Settings
Settings.llm = OpenAILike(...)
Settings.embed_model = OpenAIEmbedding(...)
```

## 5. **Query Engines (as_query_engine)** ✅ FOUND
**Local Doc Search Result:**
```python
# Basic Usage
query_engine = index.as_query_engine()
response = query_engine.query("Who is Paul Graham?")

# Advanced with streaming
query_engine = index.as_query_engine(streaming=True)
```
**Features:** Processes natural language queries, provides comprehensive responses, configurable for simple/advanced patterns.

## 6. **refresh_ref_docs for Incremental Updates** ✅ FOUND
**Local Doc Search Result:**
- Checks each document's current state vs stored version
- Uses unique identifiers for comparison
- Updates/inserts only if text or metadata changed
- Minimizes processing, conserves computational resources

**Our Usage:**
```python
index.refresh_ref_docs(documents)  # Only updates changed docs
```

## 7. **CodeHierarchyNodeParser** ✅ FOUND
**Local Doc Search Result:**
- Analyzes code files into structured hierarchy
- Organizes by scopes: classes, functions, methods
- Uses CodeSplitter with customizable chunk parameters
- Creates nodes representing code structure

**To Add (not yet implemented):**
```python
from llama_index.packs.code_hierarchy import CodeHierarchyNodeParser
parser = CodeHierarchyNodeParser(
    max_chars=1500,
    max_lines=100
)
```

## 8. **KnowledgeGraphIndex** ✅ FOUND
**Local Doc Search Result:**
- Manages and organizes knowledge graphs
- Facilitates efficient retrieval and manipulation
- Integrates with KGTableRetriever and KnowledgeGraphRAGRetriever
- Enhances data querying capabilities

**Could Replace PropertyGraphIndex for simpler use cases**

## 9. **Declarative Pipeline Configuration** ✅ FOUND
**Local Doc Search Result:**
- Define pipeline components in structured manner
- Specify transformations explicitly
- Easy customization and maintenance
- List transform components clearly

**Example Pattern:**
```python
pipeline_config = {
    "name": "my_pipeline",
    "transformations": [
        {"type": "sentence_splitter", "chunk_size": 1024},
        {"type": "embed", "model": "text-embedding-3-small"}
    ]
}
```

## 10. **storage_context.persist** ✅ FOUND
**Local Doc Search Result:**
- Saves current state of storage context
- Includes: document stores, index stores, graph stores, vector stores
- Organized storage in specified directory
- Supports multiple indexes in same location
- Alternative storage backends available

**Our Usage:**
```python
storage_context.persist(persist_dir="./storage/project_name")
```

## 🎯 Key Insights from Local Docs

### All Patterns Are Native!
Every pattern we're using is documented in the official LlamaIndex docs and available as native API calls.

### Simplification Opportunities Found:
1. **CodeHierarchyNodeParser** - We could add this for better code structure analysis
2. **KnowledgeGraphIndex** - Simpler than PropertyGraphIndex for some use cases
3. **Declarative Pipeline** - Could move more config to YAML/dict format

### Our Implementation Aligns with Docs:
- ✅ Using VectorStoreIndex correctly
- ✅ Using IngestionPipeline with dedup correctly
- ✅ Using Settings singleton correctly
- ✅ Using query engines correctly
- ✅ Using persist correctly

## 📝 Action Items Based on Local Docs

1. **Continue using current patterns** - All validated in docs
2. **Consider adding CodeHierarchyNodeParser** - Native support for code structure
3. **Move to more declarative config** - Docs show dict/YAML patterns
4. **Keep refresh_ref_docs** - Confirmed as best practice for incremental updates

## 🔍 How to Search Our Local Docs

```python
from semantic_search import SemanticSearch
service = SemanticSearch()

# Search for any LlamaIndex pattern
result = service.search("your pattern here", "llamaindex_complete", limit=3)
print(result)
```

This gives us immediate access to implementation examples without leaving our environment!