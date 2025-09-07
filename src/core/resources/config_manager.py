#!/usr/bin/env python3
"""
Configuration Resource Manager - Centralized Resource Layer
Single Responsibility: Manage shared configuration resources (prevent duplicate loading)
Pattern: Singleton resource manager for efficient config sharing across components
"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, Dict, Any
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter

# Load .env file once
load_dotenv()


class ConfigurationResourceManager:
    """
    Centralized configuration resource manager
    Prevents duplicate config loading by sharing single config instance
    """
    
    _instance: Optional['ConfigurationResourceManager'] = None
    _config: Optional[Dict[str, Any]] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @property
    def config(self) -> Dict[str, Any]:
        """Get shared config (lazy initialization)"""
        if self._config is None:
            self._config = self._load_config()
        return self._config
    
    def _load_config(self) -> Dict[str, Any]:
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
    
    def initialize_settings(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize LlamaIndex Settings - Native way (called once)"""
        if self._initialized:
            return
            
        if config is None:
            config = self.config
        
        self._setup_llm_models(config)
        self._setup_embeddings(config)
        self._setup_node_parser(config)
        
        # Store config in Settings for other uses
        Settings._config = config
        self._initialized = True
    
    def _setup_llm_models(self, config: Dict[str, Any]) -> None:
        """Setup LLM models based on configuration"""
        electronhub_key = os.getenv("ELECTRONHUB_API_KEY")
        electronhub_base = os.getenv("ELECTRONHUB_BASE_URL")
        
        if config["llm_provider"] == "ollama":
            # Ollama setup - single model
            Settings.llm = Settings.llm_fast = Settings.llm_complex = Ollama(
                model=config["ollama_model"],
                base_url=config.get("ollama_base_url", "http://localhost:11434"),
                request_timeout=config.get("ollama_request_timeout", 120.0),
                context_window=config.get("ollama_context_window", 8000),
            )
        elif electronhub_key and electronhub_base:
            self._setup_electronhub_models(config, electronhub_key, electronhub_base)
        else:
            # Fallback to standard OpenAI
            Settings.llm = Settings.llm_fast = Settings.llm_complex = OpenAI(
                model=config["openai_model"],
                api_key=os.getenv("OPENAI_API_KEY"),
            )
    
    def _setup_electronhub_models(self, config: Dict[str, Any], api_key: str, api_base: str) -> None:
        """Setup ElectronHub dual-model configuration"""
        # Fast model - Gemini 2.5 Flash
        Settings.llm_fast = OpenAILike(
            model=config.get("fast_model", "gemini-2.5-flash"),
            api_key=api_key,
            api_base=api_base,
            is_chat_model=True,
            max_requests_per_minute=30,
            request_timeout=60.0,
        )
        
        # Complex model - Claude Opus 4.1
        Settings.llm_complex = OpenAILike(
            model=config.get("complex_model", "claude-opus-4-1-20250805"), 
            api_key=api_key,
            api_base=api_base,
            is_chat_model=True,
            max_requests_per_minute=30,
            request_timeout=120.0,
        )
        
        # Alternative complex model - Gemini 2.5 Pro
        Settings.llm_complex_alt = OpenAILike(
            model=config.get("complex_alt_model", "gemini-2.5-pro"),
            api_key=api_key,
            api_base=api_base,
            is_chat_model=True,
            max_requests_per_minute=30,
            request_timeout=90.0,
        )
        
        # Default to fast model
        Settings.llm = Settings.llm_fast
    
    def _setup_embeddings(self, config: Dict[str, Any]) -> None:
        """Setup embedding models based on configuration"""
        if config["embed_provider"] == "ollama":
            Settings.embed_model = OllamaEmbedding(
                model_name=config.get("ollama_embed_model", "nomic-embed-text"),
                base_url=config.get("ollama_base_url", "http://localhost:11434"),
            )
        else:
            Settings.embed_model = OpenAIEmbedding(
                model=config.get("openai_embed_model", "text-embedding-3-small"),
                api_key=os.getenv("OPENAI_API_KEY"),
                max_requests_per_minute=60,  # Prevent rate limiting
                max_query_length=8191,
            )
    
    def _setup_node_parser(self, config: Dict[str, Any]) -> None:
        """Setup node parser based on configuration"""
        Settings.node_parser = SentenceSplitter(
            chunk_size=config.get("chunk_size", 512),
            chunk_overlap=config.get("chunk_overlap", 50),
        )
    
    def get_collection_name(self, project: str) -> str:
        """Get collection name with configured prefix"""
        prefix = self.config.get("collection_prefix", "ai_intelligence_")
        return f"{prefix}{project}"
    
    def get_configured_reader(self, path: str, filename_as_id: bool = False):
        """Get SimpleDirectoryReader with config settings"""
        from llama_index.core import SimpleDirectoryReader
        from pathlib import Path
        index_config = self.config.get('indexing', {})
        
        # Native 2025 pattern: Use explicit include paths if configured
        include_paths = index_config.get('include_paths')
        if include_paths and isinstance(include_paths, list):
            # Collect all file paths from include_paths (native LlamaIndex approach)
            base_path = Path(path)
            file_paths = []
            file_exts = set(index_config.get('file_extensions', ['.py', '.js', '.md']))
            
            for include_path in include_paths:
                abs_path = base_path / include_path
                
                if abs_path.is_file():
                    # Individual file
                    file_paths.append(str(abs_path))
                elif abs_path.is_dir():
                    # Directory - collect all matching files recursively
                    for file_path in abs_path.rglob("*"):
                        if file_path.is_file() and file_path.suffix in file_exts:
                            file_paths.append(str(file_path))
                else:
                    print(f"Warning: Include path {abs_path} does not exist")
            
            if file_paths:
                # Use native input_files for explicit file inclusion
                return SimpleDirectoryReader(
                    input_files=file_paths,
                    filename_as_id=filename_as_id
                )
        
        # Fallback to traditional directory + exclude pattern
        return SimpleDirectoryReader(
            path,
            recursive=index_config.get('recursive', True),
            required_exts=index_config.get('file_extensions', ['.py', '.js', '.md']),
            exclude=index_config.get('exclude_patterns', ['node_modules', '__pycache__', '.git']),
            filename_as_id=filename_as_id
        )


# Global instance for component sharing
_config_manager = ConfigurationResourceManager()

def get_config_resource() -> ConfigurationResourceManager:
    """Get shared configuration resource manager"""
    return _config_manager