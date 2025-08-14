#!/usr/bin/env python3
"""
Simple script to run the Neo4j MCP Server for development and testing.
"""

import asyncio
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from neo4j_mcp_server.server import main_mcp


if __name__ == "__main__":
    main_mcp()
