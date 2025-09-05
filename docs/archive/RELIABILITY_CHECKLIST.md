# Semantic Search Service - Reliability Checklist

## For temporal-hooks integration

### ✅ Must Have (Before temporal-hooks can use)
- [ ] Fix embedding dimension mismatch
- [ ] All collections use correct embeddings (OpenAI or FastEmbed)
- [ ] Health check endpoint `/health`
- [ ] Response time <1s for searches
- [ ] Error recovery (auto-reconnect to Qdrant)

### 📊 Current Status (Aug 30, 2025)
```bash
# Check health
curl http://localhost:8000/health

# Test search speed
time curl http://localhost:8000/search?q=test&project=semantic-search-service
```

### 🎯 Target Metrics
- Uptime: 99.9% (max 8.64s downtime/day)
- Response: p95 < 500ms, p99 < 1s
- Accuracy: 95%+ relevant results
- Collections: All indexed and searchable

### 🔍 Monitoring
```python
# Add to semantic_search.py
def health_check():
    return {
        "status": "healthy",
        "collections": self.list_projects(),
        "qdrant": qdrant_client.info(),
        "timestamp": datetime.now()
    }
```

### 🚀 When Ready
- [ ] All collections searchable
- [ ] Hook can query without errors
- [ ] Response times consistently <1s
- [ ] No embedding mismatches
- [ ] Health endpoint returns 200

Then temporal-hooks can build workflows!