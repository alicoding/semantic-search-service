"""
AI Development Intelligence - Configuration Module
Uses native LlamaIndex Settings with yaml/env configuration
TRUE 95/5: All configuration is native LlamaIndex
"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()
from typing import Optional
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from qdrant_client import QdrantClient

def load_config() -> dict:
    """Load configuration from yaml or environment variables"""
    config_path = Path("config.yaml")
    
    if config_path.exists():
        with open(config_path) as f:
            config = yaml.safe_load(f)
            # Replace environment variables
            for key, value in config.items():
                if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                    env_var = value[2:-1]
                    config[key] = os.getenv(env_var, value)
    else:
        # Fallback to environment variables
        config = {
            "llm_provider": os.getenv("LLM_PROVIDER", "openai"),
            "embed_provider": os.getenv("EMBED_PROVIDER", "openai"),
            "ollama_model": os.getenv("OLLAMA_MODEL", "llama3.1:latest"),
            "openai_model": os.getenv("OPENAI_MODEL", "gpt-4"),
            "openai_embed_model": os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small"),
            "huggingface_embed_model": os.getenv("HUGGINGFACE_EMBED_MODEL", "BAAI/bge-base-en-v1.5"),
            "ollama_base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            "ollama_request_timeout": float(os.getenv("OLLAMA_REQUEST_TIMEOUT", "120.0")),
            "ollama_context_window": int(os.getenv("OLLAMA_CONTEXT_WINDOW", "8000")),
            "num_workers": int(os.getenv("NUM_WORKERS", "4")),
            "chunk_size": int(os.getenv("CHUNK_SIZE", "512")),
            "chunk_overlap": int(os.getenv("CHUNK_OVERLAP", "50")),
            "qdrant_url": os.getenv("QDRANT_URL", "http://localhost:6333"),
            "collection_prefix": os.getenv("COLLECTION_PREFIX", "ai_intelligence_"),
        }
    
    return config

def initialize_settings(config: Optional[dict] = None) -> None:
    """
    Initialize LlamaIndex Settings - Native way!
    This is called once at startup, then all components use these settings.
    """
    if config is None:
        config = load_config()
    
    # Configure LLM - Native Settings
    if config["llm_provider"] == "ollama":
        Settings.llm = Ollama(
            model=config["ollama_model"],
            base_url=config.get("ollama_base_url", "http://localhost:11434"),
            request_timeout=config.get("ollama_request_timeout", 120.0),
            context_window=config.get("ollama_context_window", 8000),
        )
    else:
        # Check if ElectronHub is configured
        electronhub_key = os.getenv("ELECTRONHUB_API_KEY")
        electronhub_base = os.getenv("ELECTRONHUB_BASE_URL")
        
        if electronhub_key and electronhub_base:
            # Use ElectronHub with OpenAILike to bypass model validation
            Settings.llm = OpenAILike(
                model=config["openai_model"],  # Claude Opus 4.1, Grok 4, etc.
                api_key=electronhub_key,
                api_base=electronhub_base,
                is_chat_model=True,  # Required for chat-completion style
            )
        else:
            # Fallback to standard OpenAI
            Settings.llm = OpenAI(
                model=config["openai_model"],
                api_key=os.getenv("OPENAI_API_KEY"),
            )
    
    # Configure Embeddings - Native Settings
    if config["embed_provider"] == "ollama":
        # Use Ollama embeddings
        Settings.embed_model = OllamaEmbedding(
            model_name=config.get("ollama_embed_model", "nomic-embed-text"),
            base_url=config.get("ollama_base_url", "http://localhost:11434"),
        )
    else:
        Settings.embed_model = OpenAIEmbedding(
            model=config.get("openai_embed_model", "text-embedding-3-small"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    
    # Configure Node Parser - Native SentenceSplitter works for all files
    Settings.node_parser = SentenceSplitter(
        chunk_size=config.get("chunk_size", 512),
        chunk_overlap=config.get("chunk_overlap", 50),
    )
    
    # Store config for other uses
    Settings._config = config

# Global Qdrant client instance (singleton pattern)
_qdrant_client = None

def get_qdrant_client() -> QdrantClient:
    """Get Qdrant client singleton with configured URL - prevents connection warnings"""
    global _qdrant_client
    if _qdrant_client is None:
        config = getattr(Settings, '_config', load_config())
        _qdrant_client = QdrantClient(url=config["qdrant_url"])
    return _qdrant_client

def close_qdrant_client():
    """Explicitly close Qdrant client - call this on shutdown to prevent warnings"""
    global _qdrant_client
    if _qdrant_client is not None:
        try:
            _qdrant_client.close()
        except Exception:
            pass  # Ignore errors on close
        _qdrant_client = None

def get_collection_name(project: str) -> str:
    """Get collection name with configured prefix"""
    config = getattr(Settings, '_config', load_config())
    prefix = config.get("collection_prefix", "ai_intelligence_")
    return f"{prefix}{project}"

# Initialize on module import
initialize_settings()

def get_configured_reader(path: str, filename_as_id: bool = False):
    """
    Get SimpleDirectoryReader with config settings - DRY pattern
    This eliminates duplication across the codebase
    """
    from llama_index.core import SimpleDirectoryReader
    config = load_config()
    index_config = config.get('indexing', {})
    
    return SimpleDirectoryReader(
        path,
        recursive=index_config.get('recursive', True),
        required_exts=index_config.get('file_extensions', ['.py', '.js', '.md']),
        exclude=index_config.get('exclude_patterns', ['node_modules', '__pycache__', '.git']),
        filename_as_id=filename_as_id  # For refresh tracking
    )

# Export config for use in other modules
CONFIG = load_config()