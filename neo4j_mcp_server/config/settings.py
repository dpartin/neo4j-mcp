"""Main settings configuration for Neo4j MCP Server."""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Main application settings."""
    
    # Neo4j Configuration
    neo4j_uri: str = Field(default="bolt://localhost:7687", alias="NEO4J_URI")
    neo4j_user: str = Field(default="neo4j", alias="NEO4J_USER")
    neo4j_password: str = Field(default="password", alias="NEO4J_PASSWORD")
    neo4j_database: str = Field(default="neo4j", alias="NEO4J_DATABASE")
    
    # MCP Server Configuration
    mcp_server_host: str = Field(default="localhost", alias="MCP_SERVER_HOST")
    mcp_server_port: int = Field(default=8000, alias="MCP_SERVER_PORT")
    mcp_server_name: str = Field(default="neo4j-mcp-server", alias="MCP_SERVER_NAME")
    
    # Vector Embedding Configuration
    embedding_model: str = Field(default="all-MiniLM-L6-v2", alias="EMBEDDING_MODEL")
    vector_dimension: int = Field(default=384, alias="VECTOR_DIMENSION")
    vector_index_name: str = Field(default="node_embeddings", alias="VECTOR_INDEX_NAME")
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", alias="OPENAI_MODEL")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_format: str = Field(default="json", alias="LOG_FORMAT")
    
    # Performance Configuration
    connection_pool_size: int = Field(default=10, alias="CONNECTION_POOL_SIZE")
    query_timeout: int = Field(default=30, alias="QUERY_TIMEOUT")
    cache_ttl: int = Field(default=300, alias="CACHE_TTL")
    
    # Security Configuration
    enable_auth: bool = Field(default=True, alias="ENABLE_AUTH")
    api_key: Optional[str] = Field(default=None, alias="API_KEY")
    
    # Development Configuration
    debug: bool = Field(default=False, alias="DEBUG")
    enable_metrics: bool = Field(default=True, alias="ENABLE_METRICS")
    
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        case_sensitive = False
    )


# Global settings instance
settings = Settings()
