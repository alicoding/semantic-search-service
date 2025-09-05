# Native LlamaIndex Configuration System

## Overview

This project uses LlamaIndex's native Settings pattern with YAML configuration support for maximum flexibility and maintainability.

## How It Works

1. **Native Settings Pattern**: Uses `llama_index.core.Settings` singleton (official pattern)
2. **YAML Configuration**: External config files for different environments/projects
3. **Environment Variables**: Override YAML settings with environment variables
4. **Provider Abstraction**: Switch between providers without code changes

## Configuration Files

### Project Configuration (`.llm-config.yaml`)

```yaml
# LLM Configuration
llm:
  provider: fastembed  # openai, openai-like, ollama, azure
  model: BAAI/bge-small-en-v1.5
  api_key: ${OPENAI_API_KEY}  # Resolved from environment
  
# Embedding Configuration  
embed:
  provider: fastembed
  model: BAAI/bge-small-en-v1.5
```

### Location Priority

1. `.llm-config.yaml` in current directory
2. `config/llm-config.yaml` in project
3. `~/.config/llama-index/config.yaml` (user global)
4. Environment variables (override all)

## Usage

### Basic Setup

```python
from config import configure_project

# Auto-detect and load configuration
configure_project()
```

### Explicit Configuration

```python
# Load specific config file
configure_project("config/production.yaml")

# Or configure manually
from llama_index.core import Settings
Settings.llm = OpenAI(model="gpt-4")
Settings.embed_model = FastEmbedEmbedding()
```

### Environment Variables

Override any setting with environment variables:

```bash
export LLM_PROVIDER=openai
export LLM_MODEL=gpt-4-turbo
export EMBED_PROVIDER=fastembed
export EMBED_MODEL=BAAI/bge-large-en-v1.5
```

## Supported Providers

### LLM Providers

| Provider | Example Config | Notes |
|----------|---------------|-------|
| `openai` | `model: gpt-4-turbo` | Official OpenAI API |
| `openai-like` | `api_base: https://api.electronhub.ai/v1` | Compatible APIs |
| `ollama` | `base_url: http://localhost:11434` | Local models |
| `azure` | `deployment_name: my-gpt4` | Azure OpenAI |

### Embedding Providers

| Provider | Example Config | Notes |
|----------|---------------|-------|
| `fastembed` | `model: BAAI/bge-small-en-v1.5` | Local, no API |
| `openai` | `model: text-embedding-3-small` | OpenAI embeddings |
| `ollama` | `model: nomic-embed-text` | Local embeddings |
| `huggingface` | `model: sentence-transformers/all-MiniLM-L6-v2` | HF models |

## Per-Project Examples

### High-Security Project

```yaml
# secure-project/.llm-config.yaml
llm:
  provider: azure  # Corporate requirement
  model: gpt-4
  deployment_name: corp-gpt4
  azure_endpoint: https://corp.openai.azure.com
  api_version: 2024-02-01
  
embed:
  provider: azure
  model: text-embedding-ada-002
  
# No fallbacks allowed for security
fallback: error
```

### Local Development

```yaml
# dev/.llm-config.yaml
llm:
  provider: ollama
  model: llama2
  base_url: http://localhost:11434
  
embed:
  provider: fastembed
  model: BAAI/bge-small-en-v1.5
```

### Production API

```yaml
# api/.llm-config.yaml
llm:
  provider: openai
  model: gpt-3.5-turbo
  temperature: 0.1  # Low temp for consistency
  
embed:
  provider: openai
  model: text-embedding-3-small
  api_key: ${OPENAI_API_KEY}
```

## Why This Approach?

1. **Native Pattern**: Uses official LlamaIndex Settings singleton
2. **No Custom Code**: Configuration is data, not code
3. **Environment Aware**: Different configs for dev/test/prod
4. **Provider Agnostic**: Switch providers without code changes
5. **Secure**: API keys from environment, not in config files
6. **Scalable**: Each project/service has its own config

## Best Practices

1. **Never commit API keys** - Use `${ENV_VAR}` syntax
2. **Use local embeddings** when possible (FastEmbed)
3. **Set temperature explicitly** for reproducibility
4. **Document provider requirements** in config comments
5. **Test with multiple providers** to ensure compatibility

## Native Patterns

### HuggingFace Tokenizers with FastEmbed

When using FastEmbed (which uses HuggingFace tokenizers internally), you may see parallelism warnings. The **native LlamaIndex pattern** is to set the environment variable before imports:

```python
# This is the official pattern from LlamaIndex docs
# Must be set BEFORE importing LlamaIndex components
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Then import LlamaIndex
from llama_index.core import Settings
```

This is **not** a workaround - it's the documented native approach from both HuggingFace and LlamaIndex. See [LlamaIndex HuggingFace docs](https://docs.llamaindex.ai/en/stable/examples/embeddings/huggingface/).

## Troubleshooting

### Config Not Found

```python
# Check which config was loaded
config = configure_project()
print(config.config_path)  # Shows loaded file or None
```

### Wrong Provider Loading

```python
# Check current settings
from llama_index.core import Settings
print(f"LLM: {Settings.llm}")
print(f"Embeddings: {Settings.embed_model}")
```

### Environment Variable Issues

```bash
# Verify environment variables are set
python -c "import os; print(os.getenv('LLM_PROVIDER'))"
```

## Migration from Hardcoded Settings

### Before (Hardcoded)

```python
Settings.llm = OpenAI(model="gpt-3.5-turbo")
Settings.embed_model = OpenAIEmbedding()
```

### After (Configurable)

```python
from config import configure_project
configure_project()  # Loads from YAML/env
```

## Advanced Features

### Dynamic Provider Selection

```python
# config.py already handles this internally
if provider == "openai":
    return OpenAI(...)
elif provider == "ollama":
    return Ollama(...)
```

### Environment-Specific Configs

```yaml
environments:
  development:
    llm:
      provider: ollama
  production:
    llm:
      provider: openai
```

### Fallback Chains

```yaml
llm:
  provider: openai
  fallback:
    provider: ollama
    model: llama2
```

## Integration with CI/CD

```yaml
# .github/workflows/test.yml
env:
  LLM_PROVIDER: openai
  LLM_MODEL: gpt-3.5-turbo
  EMBED_PROVIDER: fastembed
```

## Conclusion

This native configuration approach provides:
- ✅ Full LlamaIndex compatibility
- ✅ Zero custom abstractions
- ✅ Environment flexibility
- ✅ Provider independence
- ✅ Production readiness

All while following the official Settings pattern recommended by LlamaIndex documentation.