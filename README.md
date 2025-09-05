```
 ███████ ███████ ███    ███  █████  ███    ██ ████████ ██  ██████ 
 ██      ██      ████  ████ ██   ██ ████   ██    ██    ██ ██      
 ███████ █████   ██ ████ ██ ███████ ██ ██  ██    ██    ██ ██      
      ██ ██      ██  ██  ██ ██   ██ ██  ██ ██    ██    ██ ██      
 ███████ ███████ ██      ██ ██   ██ ██   ████    ██    ██  ██████ 
                                                                   
 ███████ ███████  █████  ██████   ██████ ██   ██                  
 ██      ██      ██   ██ ██   ██ ██      ██   ██                  
 ███████ █████   ███████ ██████  ██      ███████                  
      ██ ██      ██   ██ ██   ██ ██      ██   ██                  
 ███████ ███████ ██   ██ ██   ██  ██████ ██   ██                  
```

# Semantic Search Service

Enterprise-grade semantic search powered by LlamaIndex PropertyGraphIndex with TRUE 95/5 architecture.

> **837 lines of code. 25 Python modules. One unified intelligence layer.**

[![GitHub Issues](https://img.shields.io/github/issues/alicoding/semantic-search-service)](https://github.com/alicoding/semantic-search-service/issues)
[![Production Ready](https://img.shields.io/badge/Production-🔴%20Issues%20Tracked-red)](PRODUCTION_READINESS_AUDIT.md)

## 🎯 What This Actually Does

**Semantic Search Service** is a complete intelligence layer for your development workflow:

- **🔍 Semantic Code Search** - Search your codebase semantically, not just text matching
- **🧠 Conversation Memory** - Index and search your Claude/AI conversations 
- **📊 Knowledge Graphs** - PropertyGraphIndex creates entity relationships from your code
- **🔄 Business Logic Extraction** - Automatically extract business rules and workflows
- **⚡ Real-time Integrations** - Sub-100ms responses for tools like temporal-hooks and task-enforcer
- **🎨 Auto-documentation** - Generate API docs and diagrams automatically
- **🌐 Multiple Interfaces** - FastAPI REST, CLI, and MCP (Model Context Protocol) for Claude

## 🚀 Quick Start

```bash
git clone https://github.com/alicoding/semantic-search-service.git
cd semantic-search-service

# Copy and configure
cp .env.example .env
# Add your OPENAI_API_KEY or ELECTRONHUB_API_KEY

# Start everything
./setup.sh

# Index your project
./semantic-search index . my-project

# Search semantically
./semantic-search search "authentication logic" my-project
```

## ✨ Core Features

### 🔍 Semantic Search
```bash
# Index any codebase
./semantic-search index /path/to/project project-name

# Semantic search (not just text matching)
./semantic-search search "error handling patterns" project-name

# Check if components exist (for task-enforcer integration)
./semantic-search exists "AuthService" project-name

# Find SOLID/DRY violations (for temporal-hooks integration)
./semantic-search violations project-name
```

### 🧠 Conversation Memory
```bash
# Index your Claude conversations
curl -X POST "http://localhost:8000/index/conversations" \
  -H "Content-Type: application/json" \
  -d '{"path": "/path/to/conversations", "collection": "my-conversations"}'

# Search your conversation history
curl "http://localhost:8000/search/memory?query=authentication&limit=5"
```

### 📊 Knowledge Graphs
```bash
# Generate knowledge graph from codebase
curl "http://localhost:8000/graph/my-project"

# Export to NetworkX format
curl "http://localhost:8000/graph/my-project/export"

# Visualize relationships
curl "http://localhost:8000/graph/my-project/visualize"
```

### 🎨 Auto-documentation
```bash
# Generate API documentation
python src/core/auto_docs.py generate

# Generate sequence diagrams
curl -X POST "http://localhost:8000/diagram/sequence?project=my-project"

# Extract business logic
curl -X POST "http://localhost:8000/extract/business-logic?project=my-project"
```

## 🛠️ Configuration

Everything is configured via `config.yaml`:

```yaml
# LLM Configuration - Works with OpenAI, ElectronHub, or Ollama
llm_provider: openai  # or ollama for offline
embed_provider: openai
openai_model: claude-opus-4-1-20250805  # ElectronHub models supported!

# Ollama for offline/enterprise
ollama_model: llama3.1:latest
ollama_base_url: http://localhost:11434

# Performance
num_workers: 4
cache_ttl: 3600

# Vector Store
qdrant_url: http://localhost:6333
redis_host: localhost
redis_enabled: true
```

## 📡 API Endpoints

**Core Search:**
- `POST /search/{project}` - Semantic search in project
- `POST /index` - Index new project
- `GET /exists` - Check component existence
- `GET /violations/{project}` - Find code violations

**Conversation Memory:**
- `POST /index/conversations` - Index Claude/AI conversations
- `GET /search/memory` - Search conversation history

**Knowledge Graphs:**
- `GET /graph/{project}` - Get project knowledge graph
- `GET /graph/{project}/visualize` - Generate visualizations

**Business Intelligence:**
- `POST /extract/business-logic` - Extract business rules
- `POST /diagram/sequence` - Generate sequence diagrams

**Integrations:**
- `GET /check/violation` - Real-time violation check (temporal-hooks)
- `GET /context/project` - Project context (AI agents)

## 🔌 Integrations

### temporal-hooks Integration
Real-time violation detection during development:
```bash
GET /check/violation?action=create-new-service&context=my-project
# Returns violations instantly (<100ms cached)
```

### task-enforcer Integration  
Check if components exist before creating tasks:
```bash
GET /exists?component=UserService&project=my-app
# Returns: {"exists": true, "confidence": 0.92, "file": "user_service.py"}
```

### Claude MCP Integration
Works directly in Claude Code sessions as MCP tools:
- `search_code` - Semantic search in projects
- `check_exists` - Component existence checking  
- `find_violations` - SOLID/DRY violation detection

## 🏗️ Architecture

**TRUE 95/5 Pattern:**
- **95% LlamaIndex Native** - PropertyGraphIndex, StorageContext, Settings
- **5% Glue Code** - Thin wrappers and configuration

**Tech Stack:**
- **LlamaIndex** - PropertyGraphIndex, VectorStoreIndex, query engines
- **Qdrant** - Vector database (enterprise-grade)
- **Redis** - Sub-100ms caching
- **FastAPI** - REST API with auto-generated docs
- **Typer** - Rich CLI interface

## 📊 Performance

| Feature | Target | Status |
|---------|--------|---------|
| Search Response | <500ms | ✅ <200ms |
| Violation Check | <100ms | ✅ Cached |
| Component Exists | <200ms | ✅ <100ms |
| Conversation Search | <500ms | ✅ |
| Knowledge Graph | <3s | ✅ |

## 🔧 Installation

### Prerequisites
- Python 3.8+
- Docker (for Qdrant)
- OpenAI API key OR Ollama (offline mode)

### Full Setup
```bash
# Clone repository
git clone https://github.com/alicoding/semantic-search-service.git
cd semantic-search-service

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Automated setup
./setup.sh

# Test installation
curl http://localhost:8000/docs
```

### Docker Setup
```bash
# Start services
docker-compose up -d

# Index sample project
./semantic-search index . sample-project

# Test search
./semantic-search search "FastAPI endpoints" sample-project
```

## 🧪 Testing Your Conversations

Got Claude conversations? Index and search them:

```bash
# If you have claude-parser installed
curl -X POST "http://localhost:8000/index/conversations" \
  -H "Content-Type: application/json" \
  -d '{"path": "/path/to/conversations", "collection": "my-chats"}'

# Search your conversation history
curl "http://localhost:8000/search/memory?query=how to implement caching&limit=3"
```

## 🐛 Known Issues

We track all issues publicly with proper DoR/DoD:

- [#23](https://github.com/alicoding/semantic-search-service/issues/23) 🚨 **CRITICAL**: Missing health endpoint
- [#24](https://github.com/alicoding/semantic-search-service/issues/24) 🚨 **CRITICAL**: API doesn't initialize LlamaIndex Settings  
- [#25](https://github.com/alicoding/semantic-search-service/issues/25) ⚠️ **HIGH**: Rate limiting crashes git hooks

See [PRODUCTION_READINESS_AUDIT.md](PRODUCTION_READINESS_AUDIT.md) for complete analysis.

## 🤝 Contributing

Found a bug? [Create an issue](https://github.com/alicoding/semantic-search-service/issues) with:
- Clear reproduction steps
- Expected vs actual behavior  
- Your environment (Ollama/OpenAI, OS, etc.)

We fix real bugs that real users encounter.

## 📚 Documentation

- **[PRODUCTION_READINESS_AUDIT.md](PRODUCTION_READINESS_AUDIT.md)** - Current production issues
- **[CAPABILITY_MAPPING.md](CAPABILITY_MAPPING.md)** - What actually works vs. claimed
- **[docs/](docs/)** - Detailed guides and API references

## 🎯 Real-World Example

**Before:** Grep for "authentication" returns 500 text matches  
**After:** Semantic search finds actual auth patterns, business logic, and related components with confidence scores

```bash
./semantic-search search "user authentication flow" my-project
# Returns: AuthService.authenticate() method, login flow, JWT handling, etc.
# With semantic understanding, not just text matching
```

---

**Built with LlamaIndex native patterns. Stop searching. Start finding.** 🎯