#!/usr/bin/env python3
"""
Minimal test to check if FastMCP is working
"""

import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_minimal_mcp():
    """Test minimal MCP server functionality."""
    
    print("🧪 Testing minimal MCP server...")
    
    # Create a minimal server configuration
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-c", """
import asyncio
from fastmcp import FastMCP

mcp = FastMCP("test-server")

@mcp.tool
def test_echo(message: str) -> str:
    return f"Echo: {message}"

if __name__ == "__main__":
    mcp.run()
"""],
        env={"PYTHONPATH": "."},
        cwd="."
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                print("✅ MCP client connected successfully!")
                
                # List available tools
                tools_result = await session.list_tools()
                print(f"✅ Found {len(tools_result.tools)} tools:")
                
                for tool in tools_result.tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                # Test calling the echo tool
                if tools_result.tools:
                    print("\n🧪 Testing echo tool...")
                    echo_result = await session.call_tool("test_echo", arguments={"message": "Hello from test!"})
                    print(f"✅ Echo result: {echo_result.content[0].text}")
                
                return True
                
    except Exception as e:
        print(f"❌ MCP test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_minimal_mcp())
    if success:
        print("\n🎉 Minimal MCP test passed!")
    else:
        print("\n❌ Minimal MCP test failed!")
