#!/usr/bin/env python3
"""
Comprehensive test suite for Neo4j MCP Server
This test suite consolidates the most important tests for the server.
"""

import asyncio
import os
import sys
import logging
from typing import Dict, Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

class Neo4jMCPServerTestSuite:
    """Comprehensive test suite for Neo4j MCP Server."""
    
    def __init__(self):
        self.test_results = {}
        self.session = None
    
    async def setup(self):
        """Setup test environment."""
        print("🔧 Setting up test environment...")
        
        # Check if .env file exists
        if not os.path.exists(".env"):
            print("❌ .env file missing - run setup_env.py first")
            return False
        
        # Load environment variables
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            required_vars = ["NEO4J_URI", "NEO4J_USER", "NEO4J_PASSWORD", "NEO4J_DATABASE"]
            missing_vars = [var for var in required_vars if not os.getenv(var)]
            
            if missing_vars:
                print(f"❌ Missing environment variables: {missing_vars}")
                return False
            
            print("✅ Environment variables loaded correctly")
            return True
            
        except Exception as e:
            print(f"❌ Error loading environment variables: {e}")
            return False
    
    async def test_mcp_connection(self):
        """Test MCP server connection."""
        print("\n🧪 Testing MCP server connection...")
        
        server_params = StdioServerParameters(
            command="uv",
            args=["run", "python", "../server.py"],
            env={"PYTHONPATH": ".."},
            cwd=".."
        )
        
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    self.session = session
                    
                    # Initialize the connection
                    await session.initialize()
                    print("✅ MCP client connected successfully!")
                    
                    # List available tools
                    tools_result = await session.list_tools()
                    print(f"✅ Found {len(tools_result.tools)} tools")
                    
                    # Store tools for later tests
                    self.tools = {tool.name: tool for tool in tools_result.tools}
                    
                    return True
                    
        except Exception as e:
            print(f"❌ MCP server connection failed: {e}")
            return False
    
    async def test_echo_tool(self):
        """Test the echo tool."""
        print("\n🧪 Testing echo tool...")
        
        if not self.session:
            print("❌ No active session")
            return False
        
        try:
            result = await self.session.call_tool("echo", {"message": "Hello, MCP!"})
            response = result.content[0].text
            
            if "Hello, MCP!" in response:
                print("✅ Echo tool working correctly")
                return True
            else:
                print(f"❌ Echo tool failed: {response}")
                return False
                
        except Exception as e:
            print(f"❌ Echo tool test failed: {e}")
            return False
    
    async def test_list_nodes_tool(self):
        """Test the list_nodes tool."""
        print("\n🧪 Testing list_nodes tool...")
        
        if not self.session:
            print("❌ No active session")
            return False
        
        try:
            result = await self.session.call_tool("list_nodes", {})
            response = result.content[0].text
            
            if "Found" in response and "nodes" in response:
                print("✅ List nodes tool working correctly")
                return True
            else:
                print(f"❌ List nodes tool failed: {response}")
                return False
                
        except Exception as e:
            print(f"❌ List nodes tool test failed: {e}")
            return False
    
    async def test_create_node_tool(self):
        """Test the create_node tool."""
        print("\n🧪 Testing create_node tool...")
        
        if not self.session:
            print("❌ No active session")
            return False
        
        try:
            result = await self.session.call_tool("create_node", {
                "labels": ["TestNode"],
                "properties": {"name": "Test Node", "value": 42}
            })
            response = result.content[0].text
            
            if "created successfully" in response:
                print("✅ Create node tool working correctly")
                return True
            else:
                print(f"❌ Create node tool failed: {response}")
                return False
                
        except Exception as e:
            print(f"❌ Create node tool test failed: {e}")
            return False
    
    async def test_execute_query_tool(self):
        """Test the execute_query tool."""
        print("\n🧪 Testing execute_query tool...")
        
        if not self.session:
            print("❌ No active session")
            return False
        
        try:
            result = await self.session.call_tool("execute_query", {
                "query": "MATCH (n:TestNode) RETURN count(n) as count"
            })
            response = result.content[0].text
            
            if "executed successfully" in response:
                print("✅ Execute query tool working correctly")
                return True
            else:
                print(f"❌ Execute query tool failed: {response}")
                return False
                
        except Exception as e:
            print(f"❌ Execute query tool test failed: {e}")
            return False
    
    async def run_all_tests(self):
        """Run all tests."""
        print("🚀 Starting Neo4j MCP Server Test Suite")
        print("=" * 50)
        
        tests = [
            ("Environment Setup", self.setup),
            ("MCP Connection", self.test_mcp_connection),
            ("Echo Tool", self.test_echo_tool),
            ("List Nodes Tool", self.test_list_nodes_tool),
            ("Create Node Tool", self.test_create_node_tool),
            ("Execute Query Tool", self.test_execute_query_tool),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                result = await test_func()
                self.test_results[test_name] = result
                if result:
                    passed += 1
            except Exception as e:
                print(f"❌ {test_name} failed with exception: {e}")
                self.test_results[test_name] = False
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 Test Results Summary")
        print("=" * 50)
        
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name}: {status}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 All tests passed! The server is ready for production.")
            print("\n📋 Available MCP tools for Cursor:")
            if hasattr(self, 'tools'):
                for tool_name in self.tools.keys():
                    print(f"   - mcp_neo4j-mcp-server_{tool_name}")
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Check the errors above.")
        
        return passed == total

async def main():
    """Main test function."""
    test_suite = Neo4jMCPServerTestSuite()
    
    try:
        success = await test_suite.run_all_tests()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Test suite interrupted by user")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
