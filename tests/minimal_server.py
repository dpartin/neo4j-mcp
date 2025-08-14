#!/usr/bin/env python3
"""
Minimal FastMCP server for testing
"""

from fastmcp import FastMCP

# Create FastMCP server
mcp = FastMCP("minimal-test-server")

@mcp.tool
def test_echo(message: str) -> str:
    """Echo back the input message."""
    return f"Echo: {message}"

@mcp.tool
def test_add(a: int, b: int) -> str:
    """Add two numbers."""
    result = a + b
    return f"Result: {a} + {b} = {result}"

if __name__ == "__main__":
    print("Starting minimal FastMCP server...")
    mcp.run()
