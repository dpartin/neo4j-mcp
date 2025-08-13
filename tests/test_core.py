"""Tests for core functionality."""

import pytest
from neo4j_mcp_server.core.errors import (
    Neo4jMCPError,
    ConnectionError,
    QueryError,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    ResourceNotFoundError,
    ConflictError,
    TimeoutError,
    ConfigurationError
)
from neo4j_mcp_server.core.logging import setup_logging, get_logger


class TestErrors:
    """Test custom exception classes."""
    
    def test_base_error(self):
        """Test base Neo4jMCPError."""
        error = Neo4jMCPError("Test error", {"detail": "test"})
        
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.details == {"detail": "test"}
    
    def test_connection_error(self):
        """Test ConnectionError."""
        error = ConnectionError("Connection failed")
        
        assert isinstance(error, Neo4jMCPError)
        assert str(error) == "Connection failed"
    
    def test_query_error(self):
        """Test QueryError."""
        error = QueryError("Query failed")
        
        assert isinstance(error, Neo4jMCPError)
        assert str(error) == "Query failed"
    
    def test_validation_error(self):
        """Test ValidationError."""
        error = ValidationError("Validation failed")
        
        assert isinstance(error, Neo4jMCPError)
        assert str(error) == "Validation failed"
    
    def test_authentication_error(self):
        """Test AuthenticationError."""
        error = AuthenticationError("Auth failed")
        
        assert isinstance(error, Neo4jMCPError)
        assert str(error) == "Auth failed"
    
    def test_authorization_error(self):
        """Test AuthorizationError."""
        error = AuthorizationError("Not authorized")
        
        assert isinstance(error, Neo4jMCPError)
        assert str(error) == "Not authorized"
    
    def test_resource_not_found_error(self):
        """Test ResourceNotFoundError."""
        error = ResourceNotFoundError("Resource not found")
        
        assert isinstance(error, Neo4jMCPError)
        assert str(error) == "Resource not found"
    
    def test_conflict_error(self):
        """Test ConflictError."""
        error = ConflictError("Conflict occurred")
        
        assert isinstance(error, Neo4jMCPError)
        assert str(error) == "Conflict occurred"
    
    def test_timeout_error(self):
        """Test TimeoutError."""
        error = TimeoutError("Operation timed out")
        
        assert isinstance(error, Neo4jMCPError)
        assert str(error) == "Operation timed out"
    
    def test_configuration_error(self):
        """Test ConfigurationError."""
        error = ConfigurationError("Config error")
        
        assert isinstance(error, Neo4jMCPError)
        assert str(error) == "Config error"


class TestLogging:
    """Test logging functionality."""
    
    def test_setup_logging(self):
        """Test logging setup."""
        # Should not raise an exception
        setup_logging(level="INFO", format_type="json")
    
    def test_get_logger(self):
        """Test logger retrieval."""
        logger = get_logger("test_logger")
        
        assert logger is not None
        assert hasattr(logger, "info")
        assert hasattr(logger, "error")
        assert hasattr(logger, "debug")
    
    def test_setup_logging_invalid_level(self):
        """Test logging setup with invalid level."""
        # Should use default level when invalid
        setup_logging(level="INVALID_LEVEL", format_type="json")
    
    def test_setup_logging_invalid_format(self):
        """Test logging setup with invalid format."""
        # Should use default format when invalid
        setup_logging(level="INFO", format_type="INVALID_FORMAT")
