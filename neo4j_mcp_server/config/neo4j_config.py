"""Neo4j-specific configuration settings."""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class Neo4jConfig(BaseModel):
    """Neo4j connection and configuration settings."""
    
    # Connection settings
    uri: str = Field(default="bolt://localhost:7687")
    user: str = Field(default="neo4j")
    password: str = Field(default="password")
    database: str = Field(default="neo4j")
    
    # Connection pool settings
    max_connection_pool_size: int = Field(default=10)
    connection_timeout: int = Field(default=30)
    connection_liveness_check_timeout: int = Field(default=30)
    max_connection_lifetime: int = Field(default=3600)
    
    # Query settings
    query_timeout: int = Field(default=30)
    max_transaction_retry_time: int = Field(default=15)
    
    # Security settings
    encrypted: bool = Field(default=True)
    trusted_certificates: str = Field(default="TRUST_SYSTEM_CA_SIGNED_CERTIFICATES")
    
    # Performance settings
    fetch_size: int = Field(default=1000)
    routing_policy: str = Field(default="READ_WRITE")
    
    # Advanced settings
    user_agent: Optional[str] = Field(default=None)
    notification_filters: Optional[Dict[str, Any]] = Field(default=None)
    
    def get_connection_config(self) -> Dict[str, Any]:
        """Get Neo4j connection configuration dictionary."""
        from neo4j import TrustSystemCAs
        
        config = {
            "max_connection_pool_size": self.max_connection_pool_size,
            "connection_timeout": self.connection_timeout,
            "max_connection_lifetime": self.max_connection_lifetime,
            "encrypted": self.encrypted,
            "trusted_certificates": TrustSystemCAs(),
        }
        
        if self.user_agent:
            config["user_agent"] = self.user_agent
            
        return config
