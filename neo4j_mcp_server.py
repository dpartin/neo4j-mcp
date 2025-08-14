#!/usr/bin/env python3
"""
Working MCP Server using the official MCP SDK for Python.
"""

import asyncio
import logging
from typing import Any, Dict

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import CallToolResult, ListToolsResult, Tool, TextContent

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

# Create server
server = Server("neo4j-mcp-server")

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List available tools."""
    logger.info("Listing tools")
    return ListToolsResult(
        tools=[
            Tool(
                name="echo",
                description="Echo back the input",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Message to echo"
                        }
                    },
                    "required": ["message"]
                }
            ),
            Tool(
                name="create_node",
                description="Create a new node with labels and properties",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "labels": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Node labels"
                        },
                        "properties": {
                            "type": "object",
                            "description": "Node properties"
                        }
                    },
                    "required": ["labels"]
                }
            )
        ]
    )

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls."""
    logger.info(f"Calling tool: {name} with arguments: {arguments}")
    
    try:
        if name == "echo":
            message = arguments.get("message", "No message")
            result = f"Echo: {message}"
        elif name == "create_node":
            labels = arguments.get("labels", [])
            properties = arguments.get("properties", {})
            result = f"Node created with labels: {labels}, properties: {properties}"
        else:
            result = f"Unknown tool: {name}"
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=result
                )
            ]
        )
    except Exception as e:
        logger.error(f"Tool execution failed: {e}")
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Error executing tool {name}: {str(e)}"
                )
            ]
        )

async def main():
    """Main entry point."""
    # Create notification options
    notification_options = NotificationOptions(tools_changed=False)
    
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="neo4j-mcp-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=notification_options,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
