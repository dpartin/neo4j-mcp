# Neo4j MCP Server

A Model Context Protocol (MCP) server for Neo4j graph database operations, built using the official MCP SDK for Python.

## 🎯 Current Status

✅ **Successfully implemented using official MCP SDK**  
✅ **Server tested and working**  
✅ **Configuration files updated**  
🔄 **Ready for Cursor integration testing**

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- `uv` package manager
- Neo4j database (optional for testing)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd neo4j_mcp
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Test the server:**
   ```bash
   uv run python neo4j_mcp_server.py
   ```

## 🔧 MCP Server Implementation

### File: `neo4j_mcp_server.py`

This is the main MCP server implementation using the **official MCP SDK**:

- ✅ **Uses official MCP SDK** (`mcp>=1.0.0`)
- ✅ **Proper decorator-based tool registration**
- ✅ **Correct notification options and capabilities**
- ✅ **Full MCP protocol compliance**

### Available Tools

1. **`echo`** - Test tool that echoes back input
   - Parameters: `message` (string)

2. **`create_node`** - Create a new Neo4j node
   - Parameters: 
     - `labels`: Array of strings (required)
     - `properties`: Object (optional)

## 📋 Configuration Files

### Project Configuration: `mcp.json`
```json
{
  "mcpServers": {
    "neo4j-mcp-server": {
      "command": "D:\\Users\\dpartin\\AppData\\Local\\Programs\\Python\\Python312\\Scripts\\uv.exe",
      "args": ["run", "python", "neo4j_mcp_server.py"],
      "env": {
        "PYTHONPATH": "E:\\Projects\\neo4j_mcp"
      },
      "cwd": "E:\\Projects\\neo4j_mcp"
    }
  }
}
```

### Global Configuration: `d:\Users\dpartin\.cursor\mcp.json`
The global Cursor configuration includes the complete MCP server setup with all required fields.

## 🧪 Testing

### Manual Server Test
```bash
# Test initialization
echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "cursor", "version": "1.0"}}}' | uv run python neo4j_mcp_server.py
```

### Expected Response
```json
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05","capabilities":{"tools":{"listChanged":false}},"serverInfo":{"name":"neo4j-mcp-server","version":"1.0.0"}}}
```

## 🎯 Cursor Integration

### Steps to Enable

1. **Restart Cursor completely**
2. **Open the project**: `E:\Projects\neo4j_mcp`
3. **Go to Tools & Integrations panel**
4. **Look for "neo4j-mcp-server"**
5. **Try to enable it**

### Expected Results

- ✅ **Green dot** instead of red dot
- ✅ **"Connected" or "Running" status**
- ✅ **Tools available** when asking "What tools are available?"
- ✅ **Tool calls work** through natural language

### Testing Tools

Once connected, you can test:

```
"What tools are available?"
"Create a node with labels ['Movie'] and properties {'title': 'Test Movie'}"
"Echo the message 'Hello World'"
```

## 🔍 Troubleshooting

### If Still Red Dot

1. **Check Developer Console** (`Help → Toggle Developer Tools → Console`)
2. **Look for error messages** related to MCP or neo4j-mcp-server
3. **Verify server starts manually** with the test command above
4. **Check Cursor version** - ensure you have the latest version

### Common Issues

- **Server not starting**: Check Python and `uv` installation
- **Configuration errors**: Verify paths in `mcp.json` are correct
- **Permission issues**: Ensure Cursor has access to the project directory

## 📁 Project Structure

```
neo4j_mcp/
├── neo4j_mcp_server.py      # Main MCP server implementation
├── mcp.json                 # Project MCP configuration
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── .vscode/                # VS Code/Cursor settings
└── neo4j_mcp_server/       # Core Neo4j integration (future)
```

## 🔮 Next Steps

1. **Test Cursor integration** - Verify the red dot turns green
2. **Add Neo4j connection** - Integrate with actual Neo4j database
3. **Expand tools** - Add more Neo4j operations (queries, relationships, etc.)
4. **Add error handling** - Improve robustness for production use

## 📞 Support

If you encounter issues:

1. **Check the troubleshooting section above**
2. **Verify the server starts manually**
3. **Check Cursor's developer console for errors**
4. **Ensure all configuration paths are correct**

---

**🎯 This implementation uses the official MCP SDK and should provide reliable integration with Cursor!**
