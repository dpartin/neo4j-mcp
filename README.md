# Neo4j MCP Server

A production-ready Model Context Protocol (MCP) server for Neo4j graph database operations. This server provides comprehensive tools for creating, reading, updating, and deleting nodes and relationships in Neo4j, as well as executing custom Cypher queries with full data formatting.

## 🚀 Features

- **CRUD Operations**: Create, read, update, and delete nodes and relationships
- **Custom Queries**: Execute any Cypher query with parameters and formatted results
- **Real Database Connection**: Proven connection logic with robust error handling
- **FastMCP Implementation**: Built with FastMCP 2.0 for optimal performance
- **Data Formatting**: Properly formatted results with actual data display
- **Environment Management**: Secure configuration via .env files
- **Comprehensive Testing**: Full test suite with automated validation

## 📋 Prerequisites

- Python 3.8+
- Neo4j database running locally or remotely
- `uv` package manager (recommended) or `pip`

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd neo4j_mcp
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```
   Or with pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment**:
   ```bash
   cd tests
   uv run python setup_env.py
   ```

## ⚙️ Configuration

### Environment Variables

The server uses environment variables for configuration. Create a `.env` file in the project root:

```env
# Neo4j Database Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password
NEO4J_DATABASE=neo4j

# Logging Configuration
LOG_LEVEL=INFO
DEBUG=false

# MCP Server Configuration
MCP_SERVER_NAME=neo4j-mcp-server
```

### MCP Configuration

The `mcp.json` file is configured for Cursor integration:

```json
{
  "mcpServers": {
    "neo4j-mcp-server": {
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "env": {
        "PYTHONPATH": "E:\\Projects\\neo4j_mcp",
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "your-password",
        "NEO4J_DATABASE": "neo4j"
      }
    }
  }
}
```

## 🏃‍♂️ Running the Server

### Start the MCP Server

```bash
uv run python server.py
```

The server will:
- ✅ Load environment variables from .env file
- ✅ Test Neo4j connection on startup
- ✅ Start the MCP server with stdio transport
- ✅ Display formatted results with actual data

### Expected Output

```
Loaded environment variables from .env file
INFO:__main__:DEBUG: Connecting to Neo4j at bolt://localhost:7687 as neo4j to database neo4j
```

## 🛠️ Available Tools

### Core Operations

- **`echo(message: str)`** - Echo back a message (for testing)
- **`create_node(labels: List[str], properties: Optional[Dict])`** - Create a new node
- **`list_nodes(label: Optional[str])`** - List nodes with formatted results
- **`create_relationship(from_node_id: str, to_node_id: str, relationship_type: str, properties: Optional[Dict])`** - Create a relationship
- **`execute_query(query: str, parameters: Optional[Dict])`** - Execute custom Cypher queries with formatted results

### Advanced Operations

- **`get_node(node_id: Optional[int], labels: Optional[List[str]], properties: Optional[Dict])`** - Get nodes by criteria
- **`update_node(node_id: int, properties: Optional[Dict], labels: Optional[List[str]])`** - Update a node
- **`delete_node(node_id: int, cascade: bool)`** - Delete a node

## 🧪 Testing

### Run Complete Test Suite

```bash
cd tests
uv run python test_suite.py
```

### Run Individual Tests

```bash
# Verify MCP server functionality
uv run python verify_mcp.py

# Setup environment
uv run python setup_env.py
```

## 📊 Test Results

The test suite will output:
- ✅ PASS for successful tests
- ❌ FAIL for failed tests
- Detailed error messages for debugging

## 🔧 Recent Improvements

### ✅ Implemented Features

1. **Data Formatting**: Added proper result formatting with actual data display
2. **Environment Management**: Secure configuration via .env files with python-dotenv
3. **Comprehensive Testing**: Full test suite with automated validation
4. **Tool Consolidation**: All tests organized in `/tests` directory
5. **Error Handling**: Robust error handling with real error messages
6. **Connection Logic**: Proven connection logic with proper driver lifecycle management

### 🔄 Key Improvements

- **Data Display**: Tools now show actual formatted data instead of just success messages
- **Environment Setup**: Automated .env file creation and validation
- **Test Organization**: Consolidated all tests into a structured test suite
- **Documentation**: Updated installation and configuration instructions

## 📁 Project Structure

```
neo4j_mcp/
├── server.py                 # Main MCP server implementation
├── mcp.json                  # MCP configuration for Cursor
├── requirements.txt          # Python dependencies
├── README.md                # This documentation
├── LICENSE                  # MIT License
├── TRD_Neo4j_MCP_Server.md  # Technical Requirements Document
├── tests/                   # Test suite directory
│   ├── test_suite.py        # Comprehensive test suite
│   ├── verify_mcp.py        # MCP server verification
│   ├── setup_env.py         # Environment setup helper
│   └── README.md           # Test documentation
└── .env                     # Environment variables (created by setup)
```

## 🐛 Troubleshooting

### Common Issues

1. **Connection Failed**: Ensure Neo4j is running and credentials are correct
2. **MCP Tools Not Responding**: Restart the MCP server and Cursor
3. **Environment Variables**: Check that `.env` file exists and is configured
4. **Test Failures**: Run the test suite to identify specific issues

### Debug Steps

1. **Run Test Suite**: `cd tests && uv run python test_suite.py`
2. **Check Environment**: `cd tests && uv run python setup_env.py`
3. **Verify MCP Server**: `cd tests && uv run python verify_mcp.py`
4. **Check Server Logs**: Look for connection messages in server output

## 🚀 Usage Examples

### Using with Cursor

Once configured, you can use the MCP tools in Cursor:

```
mcp_neo4j-mcp-server_list_nodes
mcp_neo4j-mcp-server_create_node
mcp_neo4j-mcp-server_execute_query
```

### Example Queries

```cypher
# Create a movie node
CREATE (m:Movie {title: 'Dune', director: 'Denis Villeneuve', year: 2021})

# List all movies
MATCH (m:Movie) RETURN m.title, m.director, m.year

# Find relationships
MATCH (m1:Movie)-[r:SIMILAR_GENRE]->(m2:Movie) RETURN m1.title, m2.title
```

## 🤝 Contributing

This is a production-ready implementation with comprehensive testing and documentation. The project follows best practices for MCP development and Neo4j integration.

## 📄 License

This project is open source and available under the MIT License.
