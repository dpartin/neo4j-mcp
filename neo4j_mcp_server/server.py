"""Main MCP server for Neo4j operations."""

import asyncio
import sys
import warnings
from typing import Any, Dict, List, Optional

# Suppress Pydantic deprecation warnings
warnings.filterwarnings(
    "ignore",
    message=".*Using extra keyword arguments on `Field` is deprecated.*",
    category=DeprecationWarning,
    module="pydantic"
)
warnings.filterwarnings(
    "ignore",
    message=".*PydanticDeprecatedSince20.*",
    category=DeprecationWarning
)

from fastmcp import FastMCP
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    Resource,
    LoggingLevel,
)

from .config.settings import settings
from .core.connection import connection_manager
from .core.logging import setup_logging, get_logger
from .core.errors import Neo4jMCPError

# Import operation modules (to be implemented in Phase 2)
# from .operations import nodes, relationships, properties
# from .analytics import paths, centrality, communities, metrics
# from .rag import vectors, semantic, context

logger = get_logger(__name__)


class Neo4jMCPServer:
    """MCP server for Neo4j graph database operations."""
    
    def __init__(self):
        """Initialize the MCP server."""
        # Initialize MCP server with proper name and version
        self.server = FastMCP("neo4j-mcp-server")
        
        # Setup logging first
        self._setup_logging()
        
        # Setup tools and resources
        self._setup_tools()
        self._setup_resources()
        
        # Setup MCP protocol handlers
        self._setup_handlers()
    
    def _setup_logging(self):
        """Setup application logging."""
        setup_logging(
            level=settings.log_level,
            format_type=settings.log_format
        )
    
    def _setup_tools(self):
        """Setup MCP tools for Neo4j operations."""
        
        from fastmcp.tools import Tool
        
        # Node CRUD Tools
        create_node_tool = Tool.from_function(
            self._create_node,
            name="create_node",
            description="Create a new node with labels and properties"
        )
        self.server.add_tool(create_node_tool)
        
        get_node_tool = Tool.from_function(
            self._get_node,
            name="get_node",
            description="Retrieve nodes by ID or filters"
        )
        self.server.add_tool(get_node_tool)
        
        update_node_tool = Tool.from_function(
            self._update_node,
            name="update_node",
            description="Update node properties and labels"
        )
        self.server.add_tool(update_node_tool)
        
        delete_node_tool = Tool.from_function(
            self._delete_node,
            name="delete_node",
            description="Delete nodes and handle cascading"
        )
        self.server.add_tool(delete_node_tool)
        
        # Relationship CRUD Tools
        create_relationship_tool = Tool.from_function(
            self._create_relationship,
            name="create_relationship",
            description="Create relationships between nodes"
        )
        self.server.add_tool(create_relationship_tool)
        
        get_relationship_tool = Tool.from_function(
            self._get_relationship,
            name="get_relationship",
            description="Retrieve relationships"
        )
        self.server.add_tool(get_relationship_tool)
        
        update_relationship_tool = Tool.from_function(
            self._update_relationship,
            name="update_relationship",
            description="Update relationship properties"
        )
        self.server.add_tool(update_relationship_tool)
        
        delete_relationship_tool = Tool.from_function(
            self._delete_relationship,
            name="delete_relationship",
            description="Delete relationships"
        )
        self.server.add_tool(delete_relationship_tool)
        
        # Analytics Tools
        find_paths_tool = Tool.from_function(
            self._find_paths,
            name="find_paths",
            description="Find paths between nodes"
        )
        self.server.add_tool(find_paths_tool)
        
        calculate_centrality_tool = Tool.from_function(
            self._calculate_centrality,
            name="calculate_centrality",
            description="Calculate node centrality metrics"
        )
        self.server.add_tool(calculate_centrality_tool)
        
        detect_communities_tool = Tool.from_function(
            self._detect_communities,
            name="detect_communities",
            description="Find community structures"
        )
        self.server.add_tool(detect_communities_tool)
        
        graph_metrics_tool = Tool.from_function(
            self._graph_metrics,
            name="graph_metrics",
            description="Calculate graph-level metrics"
        )
        self.server.add_tool(graph_metrics_tool)
        
        # RAG Tools
        vector_search_tool = Tool.from_function(
            self._vector_search,
            name="vector_search",
            description="Perform vector similarity search"
        )
        self.server.add_tool(vector_search_tool)
        
        semantic_search_tool = Tool.from_function(
            self._semantic_search,
            name="semantic_search",
            description="Semantic graph search"
        )
        self.server.add_tool(semantic_search_tool)
        
        context_retrieval_tool = Tool.from_function(
            self._context_retrieval,
            name="context_retrieval",
            description="Retrieve relevant subgraphs for RAG"
        )
        self.server.add_tool(context_retrieval_tool)
        
        # Query execution tool
        execute_query_tool = Tool.from_function(
            self._execute_query,
            name="execute_query",
            description="Execute a Cypher query and return results"
        )
        self.server.add_tool(execute_query_tool)
    
    def _setup_resources(self):
        """Setup MCP resources for Neo4j information."""
        
        from fastmcp.resources import Resource
        
        # For now, we'll use a simpler approach since FastMCP resource API might be different
        # We'll implement resources in Phase 2 when we have the actual Neo4j connection working
        pass
    
    def _setup_handlers(self):
        """Setup server event handlers."""
        # FastMCP handles tool and resource registration automatically
        # No need for manual handlers
        pass
    
    # Tool implementations (placeholder for Phase 2)
    
    async def _create_node(self, labels: List[str], properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new node."""
        try:
            logger.info("Creating node", labels=labels, properties=properties)
            
            # Build Cypher query
            label_string = ":".join(labels) if labels else ""
            properties = properties or {}
            
            if label_string:
                query = f"CREATE (n:{label_string} $properties) RETURN n"
            else:
                query = "CREATE (n $properties) RETURN n"
            
            # Execute query
            result = await connection_manager.execute_write_query(query, {"properties": properties})
            
            return {
                "success": True,
                "message": f"Node created successfully with labels: {labels}",
                "labels": labels,
                "properties": properties,
                "result": result
            }
        except Exception as e:
            logger.error("Error creating node", error=str(e))
            raise Neo4jMCPError(f"Failed to create node: {str(e)}")
    
    async def _get_node(self, node_id: Optional[int] = None, labels: Optional[List[str]] = None, properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get nodes by criteria."""
        try:
            logger.info("Getting node", node_id=node_id, labels=labels, properties=properties)
            
            # Build Cypher query based on criteria
            if node_id is not None:
                query = "MATCH (n) WHERE id(n) = $node_id RETURN n"
                parameters = {"node_id": node_id}
            elif labels:
                label_string = ":".join(labels)
                if properties:
                    # Build property conditions
                    prop_conditions = []
                    for key, value in properties.items():
                        prop_conditions.append(f"n.{key} = ${key}")
                    conditions = " AND ".join(prop_conditions)
                    query = f"MATCH (n:{label_string}) WHERE {conditions} RETURN n"
                    parameters = properties
                else:
                    query = f"MATCH (n:{label_string}) RETURN n"
                    parameters = {}
            elif properties:
                # Build property conditions
                prop_conditions = []
                for key, value in properties.items():
                    prop_conditions.append(f"n.{key} = ${key}")
                conditions = " AND ".join(prop_conditions)
                query = f"MATCH (n) WHERE {conditions} RETURN n"
                parameters = properties
            else:
                # Get all nodes
                query = "MATCH (n) RETURN n LIMIT 100"
                parameters = {}
            
            # Execute query
            result = await connection_manager.execute_query(query, parameters)
            
            return {
                "success": True,
                "message": f"Retrieved nodes successfully",
                "node_id": node_id,
                "labels": labels,
                "properties": properties,
                "result": result
            }
        except Exception as e:
            logger.error("Error getting node", error=str(e))
            raise Neo4jMCPError(f"Failed to get node: {str(e)}")
    
    async def _update_node(self, node_id: int, properties: Optional[Dict[str, Any]] = None, labels: Optional[List[str]] = None) -> Dict[str, Any]:
        """Update a node."""
        try:
            # Placeholder implementation
            logger.info("Updating node", node_id=node_id, properties=properties, labels=labels)
            return {
                "success": True,
                "message": "Node update placeholder - implement in Phase 2",
                "node_id": node_id,
                "properties": properties,
                "labels": labels
            }
        except Exception as e:
            logger.error("Error updating node", error=str(e))
            raise Neo4jMCPError(f"Failed to update node: {str(e)}")
    
    async def _delete_node(self, node_id: int, cascade: bool = False) -> Dict[str, Any]:
        """Delete a node."""
        try:
            # Placeholder implementation
            logger.info("Deleting node", node_id=node_id, cascade=cascade)
            return {
                "success": True,
                "message": "Node deletion placeholder - implement in Phase 2",
                "node_id": node_id,
                "cascade": cascade
            }
        except Exception as e:
            logger.error("Error deleting node", error=str(e))
            raise Neo4jMCPError(f"Failed to delete node: {str(e)}")
    
    async def _create_relationship(self, from_node_id: int, to_node_id: int, relationship_type: str, properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a relationship."""
        try:
            logger.info("Creating relationship", from_node_id=from_node_id, to_node_id=to_node_id, type=relationship_type, properties=properties)
            
            # Build Cypher query
            properties = properties or {}
            properties_param = {"properties": properties}
            
            query = f"""
            MATCH (a), (b)
            WHERE id(a) = $from_node_id AND id(b) = $to_node_id
            CREATE (a)-[r:{relationship_type} $properties]->(b)
            RETURN r
            """
            
            # Execute query
            result = await connection_manager.execute_write_query(query, {
                "from_node_id": from_node_id,
                "to_node_id": to_node_id,
                **properties_param
            })
            
            return {
                "success": True,
                "message": f"Relationship created successfully: {relationship_type}",
                "from_node_id": from_node_id,
                "to_node_id": to_node_id,
                "type": relationship_type,
                "properties": properties,
                "result": result
            }
        except Exception as e:
            logger.error("Error creating relationship", error=str(e))
            raise Neo4jMCPError(f"Failed to create relationship: {str(e)}")
    
    async def _get_relationship(self, relationship_id: Optional[int] = None, relationship_type: Optional[str] = None, from_node_id: Optional[int] = None, to_node_id: Optional[int] = None) -> Dict[str, Any]:
        """Get relationships by criteria."""
        try:
            # Placeholder implementation
            logger.info("Getting relationship", relationship_id=relationship_id, type=relationship_type, from_node_id=from_node_id, to_node_id=to_node_id)
            return {
                "success": True,
                "message": "Relationship retrieval placeholder - implement in Phase 2",
                "relationship_id": relationship_id,
                "type": relationship_type,
                "from_node_id": from_node_id,
                "to_node_id": to_node_id
            }
        except Exception as e:
            logger.error("Error getting relationship", error=str(e))
            raise Neo4jMCPError(f"Failed to get relationship: {str(e)}")
    
    async def _update_relationship(self, relationship_id: int, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Update a relationship."""
        try:
            # Placeholder implementation
            logger.info("Updating relationship", relationship_id=relationship_id, properties=properties)
            return {
                "success": True,
                "message": "Relationship update placeholder - implement in Phase 2",
                "relationship_id": relationship_id,
                "properties": properties
            }
        except Exception as e:
            logger.error("Error updating relationship", error=str(e))
            raise Neo4jMCPError(f"Failed to update relationship: {str(e)}")
    
    async def _delete_relationship(self, relationship_id: int) -> Dict[str, Any]:
        """Delete a relationship."""
        try:
            # Placeholder implementation
            logger.info("Deleting relationship", relationship_id=relationship_id)
            return {
                "success": True,
                "message": "Relationship deletion placeholder - implement in Phase 2",
                "relationship_id": relationship_id
            }
        except Exception as e:
            logger.error("Error deleting relationship", error=str(e))
            raise Neo4jMCPError(f"Failed to delete relationship: {str(e)}")
    
    # Analytics tool implementations (placeholder for Phase 3)
    
    async def _find_paths(self, start_node_id: int, end_node_id: int, algorithm: str = "shortest_path", max_length: Optional[int] = None) -> Dict[str, Any]:
        """Find paths between nodes."""
        try:
            # Placeholder implementation
            logger.info("Finding paths", start_node_id=start_node_id, end_node_id=end_node_id, algorithm=algorithm, max_length=max_length)
            return {
                "success": True,
                "message": "Path finding placeholder - implement in Phase 3",
                "start_node_id": start_node_id,
                "end_node_id": end_node_id,
                "algorithm": algorithm,
                "max_length": max_length
            }
        except Exception as e:
            logger.error("Error finding paths", error=str(e))
            raise Neo4jMCPError(f"Failed to find paths: {str(e)}")
    
    async def _calculate_centrality(self, node_ids: Optional[List[int]] = None, algorithm: str = "degree") -> Dict[str, Any]:
        """Calculate centrality metrics."""
        try:
            # Placeholder implementation
            logger.info("Calculating centrality", node_ids=node_ids, algorithm=algorithm)
            return {
                "success": True,
                "message": "Centrality calculation placeholder - implement in Phase 3",
                "node_ids": node_ids,
                "algorithm": algorithm
            }
        except Exception as e:
            logger.error("Error calculating centrality", error=str(e))
            raise Neo4jMCPError(f"Failed to calculate centrality: {str(e)}")
    
    async def _detect_communities(self, algorithm: str = "louvain") -> Dict[str, Any]:
        """Detect communities in the graph."""
        try:
            # Placeholder implementation
            logger.info("Detecting communities", algorithm=algorithm)
            return {
                "success": True,
                "message": "Community detection placeholder - implement in Phase 3",
                "algorithm": algorithm
            }
        except Exception as e:
            logger.error("Error detecting communities", error=str(e))
            raise Neo4jMCPError(f"Failed to detect communities: {str(e)}")
    
    async def _graph_metrics(self) -> Dict[str, Any]:
        """Calculate graph-level metrics."""
        try:
            # Placeholder implementation
            logger.info("Calculating graph metrics")
            return {
                "success": True,
                "message": "Graph metrics placeholder - implement in Phase 3"
            }
        except Exception as e:
            logger.error("Error calculating graph metrics", error=str(e))
            raise Neo4jMCPError(f"Failed to calculate graph metrics: {str(e)}")
    
    # RAG tool implementations (placeholder for Phase 4)
    
    async def _vector_search(self, query_vector: List[float], top_k: int = 10) -> Dict[str, Any]:
        """Perform vector similarity search."""
        try:
            # Placeholder implementation
            logger.info("Performing vector search", top_k=top_k)
            return {
                "success": True,
                "message": "Vector search placeholder - implement in Phase 4",
                "query_vector": query_vector,
                "top_k": top_k
            }
        except Exception as e:
            logger.error("Error performing vector search", error=str(e))
            raise Neo4jMCPError(f"Failed to perform vector search: {str(e)}")
    
    async def _semantic_search(self, query: str, limit: int = 20) -> Dict[str, Any]:
        """Perform semantic search."""
        try:
            # Placeholder implementation
            logger.info("Performing semantic search", query=query, limit=limit)
            return {
                "success": True,
                "message": "Semantic search placeholder - implement in Phase 4",
                "query": query,
                "limit": limit
            }
        except Exception as e:
            logger.error("Error performing semantic search", error=str(e))
            raise Neo4jMCPError(f"Failed to perform semantic search: {str(e)}")
    
    async def _context_retrieval(self, query: str, max_nodes: int = 50) -> Dict[str, Any]:
        """Retrieve relevant context for RAG."""
        try:
            # Placeholder implementation
            logger.info("Retrieving context", query=query, max_nodes=max_nodes)
            return {
                "success": True,
                "message": "Context retrieval placeholder - implement in Phase 4",
                "query": query,
                "max_nodes": max_nodes
            }
        except Exception as e:
            logger.error("Error retrieving context", error=str(e))
            raise Neo4jMCPError(f"Failed to retrieve context: {str(e)}")
    
    async def _execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a Cypher query and return results."""
        try:
            logger.info("Executing query", query=query, parameters=parameters)
            
            # Determine if this is a write query
            write_keywords = ["CREATE", "DELETE", "SET", "REMOVE", "MERGE", "DETACH DELETE"]
            is_write_query = any(keyword in query.upper() for keyword in write_keywords)
            
            if is_write_query:
                result = await connection_manager.execute_write_query(query, parameters or {})
            else:
                result = await connection_manager.execute_query(query, parameters or {})
            
            return {
                "success": True,
                "message": f"Query executed successfully ({'write' if is_write_query else 'read'})",
                "query": query,
                "parameters": parameters or {},
                "result": result,
                "query_type": "write" if is_write_query else "read"
            }
        except Exception as e:
            logger.error("Error executing query", error=str(e))
            raise Neo4jMCPError(f"Failed to execute query: {str(e)}")
    
    # Resource implementations (placeholder)
    
    async def _get_graph_schema(self) -> Dict[str, Any]:
        """Get graph schema information."""
        try:
            # Placeholder implementation
            return {
                "success": True,
                "message": "Graph schema placeholder - implement in Phase 2",
                "schema": {}
            }
        except Exception as e:
            logger.error("Error getting graph schema", error=str(e))
            raise Neo4jMCPError(f"Failed to get graph schema: {str(e)}")
    
    async def _get_node_types(self) -> Dict[str, Any]:
        """Get available node types."""
        try:
            # Placeholder implementation
            return {
                "success": True,
                "message": "Node types placeholder - implement in Phase 2",
                "node_types": []
            }
        except Exception as e:
            logger.error("Error getting node types", error=str(e))
            raise Neo4jMCPError(f"Failed to get node types: {str(e)}")
    
    async def _get_relationship_types(self) -> Dict[str, Any]:
        """Get available relationship types."""
        try:
            # Placeholder implementation
            return {
                "success": True,
                "message": "Relationship types placeholder - implement in Phase 2",
                "relationship_types": []
            }
        except Exception as e:
            logger.error("Error getting relationship types", error=str(e))
            raise Neo4jMCPError(f"Failed to get relationship types: {str(e)}")
    
    async def _get_analytics_results(self) -> Dict[str, Any]:
        """Get cached analytics results."""
        try:
            # Placeholder implementation
            return {
                "success": True,
                "message": "Analytics results placeholder - implement in Phase 3",
                "results": {}
            }
        except Exception as e:
            logger.error("Error getting analytics results", error=str(e))
            raise Neo4jMCPError(f"Failed to get analytics results: {str(e)}")
    
    async def _get_vector_indexes(self) -> Dict[str, Any]:
        """Get vector index information."""
        try:
            # Placeholder implementation
            return {
                "success": True,
                "message": "Vector indexes placeholder - implement in Phase 4",
                "indexes": []
            }
        except Exception as e:
            logger.error("Error getting vector indexes", error=str(e))
            raise Neo4jMCPError(f"Failed to get vector indexes: {str(e)}")
    
    async def start(self):
        """Start the MCP server."""
        try:
            logger.info("Starting Neo4j MCP Server")
            
            # Try to connect to Neo4j (optional for MCP server startup)
            try:
                await connection_manager.connect()
                logger.info("Successfully connected to Neo4j database")
            except Exception as e:
                logger.warning("Could not connect to Neo4j database - tools will work in demo mode", error=str(e))
                logger.info("MCP server will start without Neo4j connection")
            
            # Start the MCP server
            await self.server.run()
            
        except Exception as e:
            logger.error("Failed to start MCP server", error=str(e))
            raise
    
    def run_mcp_server(self):
        """Run the MCP server for stdio communication (used by Cursor)."""
        try:
            logger.info("Starting Neo4j MCP Server for stdio communication")
            
            # For MCP stdio communication, we don't need to connect to Neo4j immediately
            # The connection will be established when tools are called
            logger.info("MCP server ready for stdio communication")
            
            # Run the FastMCP server for stdio with proper error handling
            # This will block and wait for MCP protocol messages
            try:
                self.server.run()
            except KeyboardInterrupt:
                logger.info("MCP server interrupted by user")
            except Exception as e:
                logger.error("FastMCP server error", error=str(e))
                # Don't re-raise - just log the error and exit gracefully
                sys.exit(1)
            
        except KeyboardInterrupt:
            logger.info("MCP server interrupted")
        except Exception as e:
            logger.error("Failed to start MCP server for stdio", error=str(e))
            raise
    

    
    async def stop(self):
        """Stop the MCP server."""
        try:
            logger.info("Stopping Neo4j MCP Server")
            
            # Disconnect from Neo4j
            await connection_manager.disconnect()
            
        except Exception as e:
            logger.error("Error stopping MCP server", error=str(e))


# Main entry point
async def main():
    """Main entry point for the MCP server."""
    server = Neo4jMCPServer()
    
    try:
        await server.start()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down")
    except Exception as e:
        logger.error("Server error", error=str(e))
    finally:
        await server.stop()


def main_sync():
    """Synchronous main entry point for the MCP server."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error running server: {e}")
        sys.exit(1)


def main_mcp():
    """Main entry point for MCP stdio communication (used by Cursor)."""
    try:
        server = Neo4jMCPServer()
        server.run_mcp_server()
    except KeyboardInterrupt:
        # Don't print anything on KeyboardInterrupt to avoid I/O errors
        pass
    except Exception as e:
        # Log error but don't print to avoid I/O issues with stdio
        logger.error("MCP server error", error=str(e))
        sys.exit(1)


if __name__ == "__main__":
    main_mcp()
