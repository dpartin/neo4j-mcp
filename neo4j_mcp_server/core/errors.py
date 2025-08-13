"""Custom exception classes for Neo4j MCP Server."""


class Neo4jMCPError(Exception):
    """Base exception for Neo4j MCP Server."""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ConnectionError(Neo4jMCPError):
    """Raised when there's an issue with Neo4j connection."""
    pass


class QueryError(Neo4jMCPError):
    """Raised when there's an issue with Cypher queries."""
    pass


class ValidationError(Neo4jMCPError):
    """Raised when input validation fails."""
    pass


class AuthenticationError(Neo4jMCPError):
    """Raised when authentication fails."""
    pass


class AuthorizationError(Neo4jMCPError):
    """Raised when authorization fails."""
    pass


class ResourceNotFoundError(Neo4jMCPError):
    """Raised when a requested resource is not found."""
    pass


class ConflictError(Neo4jMCPError):
    """Raised when there's a conflict with existing data."""
    pass


class TimeoutError(Neo4jMCPError):
    """Raised when an operation times out."""
    pass


class ConfigurationError(Neo4jMCPError):
    """Raised when there's a configuration issue."""
    pass
