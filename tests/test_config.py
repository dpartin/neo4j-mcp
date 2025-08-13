"""Tests for configuration management."""

import pytest
from neo4j_mcp_server.config.settings import Settings
from neo4j_mcp_server.config.neo4j_config import Neo4jConfig


class TestSettings:
    """Test settings configuration."""
    
    def test_settings_defaults(self):
        """Test that settings have proper defaults."""
        settings = Settings()
        
        assert settings.neo4j_uri == "bolt://localhost:7687"
        assert settings.neo4j_user == "neo4j"
        assert settings.neo4j_database == "neo4j"
        assert settings.mcp_server_port == 8000
        assert settings.log_level == "INFO"
    
    def test_settings_environment_override(self, monkeypatch):
        """Test that environment variables override defaults."""
        monkeypatch.setenv("NEO4J_URI", "bolt://test:7687")
        monkeypatch.setenv("NEO4J_USER", "test_user")
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        
        settings = Settings()
        
        assert settings.neo4j_uri == "bolt://test:7687"
        assert settings.neo4j_user == "test_user"
        assert settings.log_level == "DEBUG"


class TestNeo4jConfig:
    """Test Neo4j configuration."""
    
    def test_neo4j_config_defaults(self):
        """Test that Neo4j config has proper defaults."""
        config = Neo4jConfig()
        
        assert config.uri == "bolt://localhost:7687"
        assert config.user == "neo4j"
        assert config.database == "neo4j"
        assert config.max_connection_pool_size == 10
        assert config.encrypted is True
    
    def test_get_connection_config(self):
        """Test connection config generation."""
        config = Neo4jConfig(
            uri="bolt://test:7687",
            user="test_user",
            password="test_pass",
            database="test_db"
        )
        
        connection_config = config.get_connection_config()
        
        assert connection_config["uri"] == "bolt://test:7687"
        assert connection_config["user"] == "test_user"
        assert connection_config["password"] == "test_pass"
        assert connection_config["database"] == "test_db"
        assert "max_connection_pool_size" in connection_config
        assert "connection_timeout" in connection_config
