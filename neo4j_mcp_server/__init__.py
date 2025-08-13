"""
Neo4j MCP Server

A Model Context Protocol (MCP) server that exposes Neo4j graph database functionality
to AI assistants and applications, enabling CRUD operations, advanced analytics, and RAG capabilities.
"""

__version__ = "0.1.0"
__author__ = "Neo4j MCP Team"
__description__ = "MCP server for Neo4j graph database operations"

from .server import Neo4jMCPServer

__all__ = ["Neo4jMCPServer"]
