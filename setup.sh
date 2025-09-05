#!/bin/bash
# TRUE 95/5 Setup - Let pip and docker-compose do everything

echo "🚀 Semantic Search Service Setup"
echo "================================"

# 1. Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# 2. Start services  
echo "🐳 Starting Qdrant and Redis..."
docker-compose up -d

# 3. Done
echo "✅ Setup complete! Use ./semantic-search or ./semantic-search-docs"