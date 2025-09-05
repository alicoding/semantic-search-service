#!/bin/bash

# AI Documentation Intelligence System - One-Command Setup
# This script sets up everything needed to prevent AI agents from guessing method names

set -e  # Exit on error

echo "🚀 Setting up AI Documentation Intelligence System"
echo "================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Check Prerequisites
echo "📋 Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

# Check Docker
if ! docker info > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Docker not running. Trying to start...${NC}"
    
    # Try to start Docker Desktop on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open -a Docker 2>/dev/null || echo "Please start Docker Desktop manually"
        echo "Waiting for Docker to start (10 seconds)..."
        sleep 10
    fi
    
    # Check again
    if ! docker info > /dev/null 2>&1; then
        echo -e "${RED}❌ Docker is required. Please start Docker Desktop.${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✅ Prerequisites OK${NC}"

# 2. Start Qdrant Vector Database
echo ""
echo "🗄️  Starting Qdrant vector database..."

# Check if Qdrant is already running
if curl -s http://localhost:6333/health > /dev/null 2>&1; then
    echo "  Qdrant already running"
else
    # Try docker-compose first
    if [ -f "docker-compose.yml" ] && command -v docker-compose &> /dev/null; then
        docker-compose up -d qdrant 2>/dev/null
    else
        # Fallback to direct docker
        docker run -d \
            --name qdrant \
            -p 6333:6333 \
            -p 6334:6334 \
            -v $(pwd)/qdrant_storage:/qdrant/storage:z \
            qdrant/qdrant:latest 2>/dev/null || echo "  Container already exists"
        
        # Start if stopped
        docker start qdrant 2>/dev/null || true
    fi
    
    # Wait for Qdrant to be ready
    echo "  Waiting for Qdrant to be ready..."
    for i in {1..30}; do
        if curl -s http://localhost:6333/health > /dev/null 2>&1; then
            break
        fi
        sleep 1
    done
fi

echo -e "${GREEN}✅ Qdrant ready${NC}"

# 3. Setup Python Environment
echo ""
echo "🐍 Setting up Python environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  Created virtual environment"
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip -q

# 4. Install Dependencies
echo ""
echo "📦 Installing dependencies..."

# Core dependencies
pip install -q \
    llama-index-core \
    llama-index-vector-stores-qdrant \
    llama-index-llms-openai \
    llama-index-llms-ollama \
    llama-index-embeddings-openai \
    llama-index-embeddings-ollama \
    qdrant-client \
    fastapi \
    uvicorn \
    typer \
    python-dotenv \
    pyyaml \
    redis \
    httpx

# Optional: MCP support
pip install -q fastmcp 2>/dev/null || echo "  Note: FastMCP not available"

# Optional: Web crawling
pip install -q llama-index-readers-web 2>/dev/null || echo "  Note: Web readers not installed"

echo -e "${GREEN}✅ Dependencies installed${NC}"

# 5. Check Configuration
echo ""
echo "🔑 Checking configuration..."

# Load .env if it exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "  Loaded .env file"
else
    echo -e "${YELLOW}⚠️  No .env file found${NC}"
fi

# Check which provider is available
if [ -n "$OPENAI_API_KEY" ]; then
    echo -e "${GREEN}✅ OpenAI API key found${NC}"
    PROVIDER="openai"
elif command -v ollama &> /dev/null; then
    echo -e "${GREEN}✅ Ollama available (offline mode)${NC}"
    PROVIDER="ollama"
    
    # Pull default model if not present
    ollama list 2>/dev/null | grep -q "llama3.1" || {
        echo "  Pulling Ollama model..."
        ollama pull llama3.1:latest
    }
else
    echo -e "${YELLOW}⚠️  No LLM provider found${NC}"
    echo "  Install Ollama or add OPENAI_API_KEY to .env"
    PROVIDER="none"
fi

# 6. Initialize System
echo ""
echo "🚀 Initializing system..."

python3 << 'PYTHON_SCRIPT'
import sys
import os
sys.path.insert(0, os.getcwd())

try:
    from src.core.config import CONFIG, initialize_settings
    print("  Configuration loaded")
    
    # Test connection to Qdrant
    from qdrant_client import QdrantClient
    client = QdrantClient(url="http://localhost:6333")
    collections = client.get_collections()
    print(f"  Connected to Qdrant ({len(collections.collections)} collections)")
    
    # Check if we should index default docs
    doc_config = CONFIG.get('documentation', {})
    auto_index = doc_config.get('auto_index', {})
    
    for framework, config in auto_index.items():
        if config.get('enabled', False):
            print(f"  Note: {framework} documentation can be indexed with:")
            print(f"    ./semantic-search docs index {framework}")
            
except Exception as e:
    print(f"  Warning: {e}")
    print("  System will initialize on first use")
PYTHON_SCRIPT

# 7. Create CLI Wrapper
echo ""
echo "📝 Creating CLI wrapper..."

cat > semantic-search << 'EOF'
#!/bin/bash
# Semantic Search CLI Wrapper
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
source venv/bin/activate 2>/dev/null || true
python -m src.integrations.cli "$@"
EOF

chmod +x semantic-search

# Create additional wrapper for docs command
cat > semantic-search-docs << 'EOF'
#!/bin/bash
# Documentation Intelligence CLI
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
source venv/bin/activate 2>/dev/null || true

case "$1" in
    index)
        if [ -z "$2" ]; then
            echo "Usage: semantic-search-docs index <framework> [url]"
            exit 1
        fi
        python -c "
from src.core.doc_intelligence import get_doc_intelligence
di = get_doc_intelligence()
result = di.index_framework('$2', '$3' if '$3' else None)
print(result)
"
        ;;
    search)
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo "Usage: semantic-search-docs search <query> <framework>"
            exit 1
        fi
        python -c "
from src.core.doc_intelligence import get_doc_intelligence
di = get_doc_intelligence()
result = di.search_pattern('$2', '$3')
print(result)
"
        ;;
    list)
        python -c "
from src.core.doc_intelligence import get_doc_intelligence
di = get_doc_intelligence()
frameworks = di.list_frameworks()
if frameworks:
    print('Indexed frameworks:')
    for f in frameworks:
        info = di.get_framework_info(f)
        print(f'  - {f}: {info.get(\"documents\", 0)} documents')
else:
    print('No frameworks indexed yet')
"
        ;;
    *)
        echo "Usage: semantic-search-docs {index|search|list}"
        echo ""
        echo "Commands:"
        echo "  index <framework> [url]  - Index framework documentation"
        echo "  search <query> <framework> - Search for patterns"
        echo "  list                      - List indexed frameworks"
        ;;
esac
EOF

chmod +x semantic-search-docs

echo -e "${GREEN}✅ CLI tools created${NC}"

# 8. Start API Server (optional)
echo ""
read -p "Start API server? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Starting API server..."
    
    # Kill any existing server
    pkill -f "uvicorn src.integrations.api" 2>/dev/null || true
    
    # Start in background
    nohup venv/bin/python -m uvicorn src.integrations.api:app \
        --host 0.0.0.0 \
        --port 8000 \
        > api.log 2>&1 &
    
    echo "  API server started on http://localhost:8000"
    echo "  Logs: tail -f api.log"
fi

# 9. Setup MCP for Claude (optional)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo ""
    read -p "Configure MCP for Claude Desktop? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cat > claude_mcp_config.json << EOF
{
  "mcpServers": {
    "semantic-search": {
      "command": "$(pwd)/venv/bin/python",
      "args": ["-m", "src.integrations.mcp_fastmcp"],
      "cwd": "$(pwd)"
    }
  }
}
EOF
        echo -e "${GREEN}✅ MCP config created: claude_mcp_config.json${NC}"
        echo "  Import this in Claude Desktop settings"
    fi
fi

# 10. Summary
echo ""
echo "========================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "========================================="
echo ""
echo "📍 Services:"
echo "  • Qdrant: http://localhost:6333"
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "  • API: http://localhost:8000/docs"
fi
echo "  • Provider: $PROVIDER"
echo ""
echo "🎯 Quick Start Commands:"
echo ""
echo "  # Index documentation (prevents guessing):"
echo "  ./semantic-search-docs index nextjs https://nextjs.org/docs"
echo ""
echo "  # Search for patterns:"
echo "  ./semantic-search-docs search 'app router' nextjs"
echo ""
echo "  # Index a project:"
echo "  ./semantic-search index . my-project"
echo ""
echo "  # Check if component exists:"
echo "  ./semantic-search exists 'AuthHandler' my-project"
echo ""
echo "📚 Full documentation: README.md"
echo ""

# Remind about temp_docs
if [ -d "temp_docs" ]; then
    echo "ℹ️  Note: temp_docs folder found (offline documentation)"
    echo "  This will be used if web crawling is unavailable"
fi