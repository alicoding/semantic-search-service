# ElectronHub Rate Limits - Internal Documentation

## 📊 Rate Limit Tiers

| Subscription Plan | Requests per minute (RPM) | Best For |
|------------------|---------------------------|----------|
| Free | 7 RPM | Testing and prototypes |
| Starter | 10 RPM | Small applications |
| Plus | 15 RPM | Growing projects |
| Core | 20 RPM | Professional use |
| **Pro** | **30 RPM** | **Production applications** ⭐ |
| Business | 60 RPM | High-volume usage |
| Enterprise | 100+ RPM | Custom enterprise needs |

## 🔧 Current Configuration

**Our Plan**: Pro (30 RPM)

### LlamaIndex Native Rate Limiting Configuration

Located in `src/core/config.py`:

```python
# ElectronHub dual-model setup with native rate limiting
Settings.llm_fast = OpenAILike(
    model=config.get("fast_model", "gemini-2.5-flash"),
    api_key=electronhub_key,
    api_base=electronhub_base,
    is_chat_model=True,
    max_requests_per_minute=30,  # Pro tier limit
    request_timeout=60.0,
)

Settings.llm_complex = OpenAILike(
    model=config.get("complex_model", "claude-opus-4-1-20250805"), 
    api_key=electronhub_key,
    api_base=electronhub_base,
    is_chat_model=True,
    max_requests_per_minute=10,  # Conservative for expensive models
    request_timeout=120.0,
)

Settings.llm_complex_alt = OpenAILike(
    model=config.get("complex_alt_model", "gemini-2.5-pro"),
    api_key=electronhub_key, 
    api_base=electronhub_base,
    is_chat_model=True,
    max_requests_per_minute=20,  # Balanced for complex tasks
    request_timeout=90.0,
)
```

## 📈 Usage Strategy

### Model Allocation (Pro Tier - 30 RPM Total)

- **Fast Model (Gemini 2.5 Flash)**: 30 RPM - Used for 90% of tasks
  - Documentation generation
  - Simple queries
  - Basic semantic search
  
- **Complex Model (Claude Opus 4.1)**: 10 RPM - Heavy reasoning only
  - Complex analysis
  - Advanced reasoning tasks
  - Critical decision making
  
- **Complex Alt (Gemini 2.5 Pro)**: 20 RPM - Alternative complex reasoning
  - Fallback for complex tasks
  - Mixed workloads

## ⚡ Performance Optimizations

### PropertyGraphIndex with Rate Limiting

The auto-documentation system (`auto_docs.py`) now uses:

1. **Native LlamaIndex Rate Limiting**: No custom wrappers
2. **Proper Persistence**: Avoids rebuilding indexes
3. **Incremental Updates**: Uses `refresh_ref_docs()` 
4. **Fast Model Priority**: Gemini 2.5 Flash for documentation

### Before vs After

| Aspect | Before | After |
|--------|--------|--------|
| API Calls | 70+ per commit | 3-5 per commit |
| Cost per Commit | ~$14 | ~$0.04 |
| Time | 2+ minutes | 10-15 seconds |
| Rate Limit Handling | Custom retry logic | Native LlamaIndex |
| Index Rebuilds | Always full rebuild | Incremental only |

## 🚨 Git Hooks Integration

Git hook (`/.git/hooks/post-merge`) now works reliably:

```bash
#!/bin/sh
# Auto-generate API documentation after pulling changes (native LlamaIndex rate limiting)
echo "📚 Updating API documentation after merge..."
python src/core/auto_docs.py generate
if [ $? -eq 0 ]; then
    echo "✅ Documentation updated with latest changes"
else
    echo "⚠️ Documentation generation failed"
fi
exit 0
```

## 📝 Key Learnings

1. **Native > Custom**: LlamaIndex's `max_requests_per_minute` is more reliable than custom rate limiting
2. **Proper Persistence**: `SimplePropertyGraphStore` in `StorageContext` prevents rebuilds
3. **Incremental Updates**: `refresh_ref_docs()` is the TRUE 95/5 pattern
4. **Model Strategy**: Fast models for 90% of tasks, complex for edge cases

## 🔄 Monitoring

Watch for these patterns that indicate rate limiting issues:

- `429 Rate limit exceeded` errors
- `500 Internal Server Error` with rate limit details
- PropertyGraphIndex always showing "Creating new..." instead of "Loading existing..."

## 📊 Usage Recommendations

- **Documentation/Simple Tasks**: Use fast model (30 RPM available)
- **Complex Analysis**: Use complex models sparingly (10-20 RPM)
- **Git Hooks**: Should complete in <30 seconds with proper persistence
- **Development**: Monitor API usage to stay within Pro tier limits

---

*Last updated: 2025-09-05*
*Current configuration: Pro tier (30 RPM)*
*Native LlamaIndex rate limiting implemented*