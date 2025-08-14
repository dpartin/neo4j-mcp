#!/usr/bin/env python3
"""
Neo4j MCP Server - Corrected FastMCP implementation
"""

import os
import logging
from typing import Optional, Dict, Any, List
from fastmcp import FastMCP
from neo4j import GraphDatabase

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env file")
except ImportError:
    print("python-dotenv not available, using system environment variables")
except Exception as e:
    print(f"Could not load .env file: {e}")

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

# Create FastMCP server
mcp = FastMCP("neo4j-mcp-server")

def format_neo4j_result(record: Dict[str, Any]) -> str:
    """Format a Neo4j result record for display."""
    if not record:
        return "Empty result"
    
    formatted_parts = []
    for key, value in record.items():
        if isinstance(value, dict) and 'properties' in value:
            # Handle node/relationship objects
            props = value['properties']
            if props:
                prop_str = ", ".join([f"{k}: {v}" for k, v in props.items()])
                formatted_parts.append(f"{key}: {{{prop_str}}}")
            else:
                formatted_parts.append(f"{key}: {{}}")
        elif isinstance(value, dict):
            # Handle other dictionaries
            formatted_parts.append(f"{key}: {value}")
        else:
            # Handle simple values
            formatted_parts.append(f"{key}: {value}")
    
    return " | ".join(formatted_parts)

def execute_neo4j_query(query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Execute a Neo4j query using the same logic as test_neo4j_connection.py."""
    
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "C0wb0ys1!")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    # Debug: Print what we're using for connection
    logger.info(f"DEBUG: Connecting to Neo4j at {uri} as {user} to database {database}")
    
    try:
        # Create driver (same as test_neo4j_connection.py)
        driver = GraphDatabase.driver(uri, auth=(user, password))
        
        # Execute query (same as test_neo4j_connection.py)
        with driver.session(database=database) as session:
            result = session.run(query, parameters or {})
            return [dict(record) for record in result]
            
    except Exception as e:
        logger.error(f"Query failed: {e}")
        logger.error(f"DEBUG: Full error details: {type(e).__name__}: {str(e)}")
        return [{"error": str(e)}]
    finally:
        if 'driver' in locals():
            driver.close()

@mcp.tool
def echo(message: str) -> str:
    """Echo back the input message."""
    logger.info(f"Echo tool called with message: {message}")
    return f"Echo: {message}"

@mcp.tool
def create_node(labels: List[str], properties: Optional[Dict[str, Any]] = None) -> str:
    """Create a new Neo4j node with labels and properties."""
    logger.info(f"Create node tool called with labels: {labels}, properties: {properties}")
    
    if not properties:
        properties = {}
    
    try:
        # Build Cypher query
        label_string = ":".join(labels)
        property_string = ", ".join([f"{k}: ${k}" for k in properties.keys()])
        
        if property_string:
            query = f"CREATE (n:{label_string} {{{property_string}}}) RETURN n"
        else:
            query = f"CREATE (n:{label_string}) RETURN n"
        
        result = execute_neo4j_query(query, properties)
        
        if result and len(result) > 0 and "error" not in result[0]:
            return f"✅ Node created successfully with labels: {labels}, properties: {properties}"
        else:
            error_msg = result[0].get("error", "Unknown error") if result else "No result"
            return f"❌ Failed to create node: {error_msg}"
    except Exception as e:
        logger.error(f"Exception in create_node: {e}")
        return f"❌ Error creating node: {str(e)}"

@mcp.tool
def list_nodes(label: Optional[str] = None) -> str:
    """List nodes in the Neo4j database, optionally filtered by label."""
    logger.info(f"List nodes tool called with label: {label}")
    
    try:
        # Handle null/None values properly
        if label is None or label == "null" or label == "":
            query = "MATCH (n) RETURN n LIMIT 50"
            parameters = {}
        else:
            query = f"MATCH (n:{label}) RETURN n LIMIT 50"
            parameters = {}
        
        result = execute_neo4j_query(query, parameters)
        
        # Check if we got a real result (not an error)
        if result and len(result) > 0 and "error" not in result[0]:
            node_count = len(result)
            # Format the results for display
            formatted_results = []
            for i, record in enumerate(result, 1):
                formatted_results.append(f"Node {i}:\n{format_neo4j_result(record)}")
            
            if label and label != "null" and label != "":
                return f"✅ Found {node_count} nodes with label '{label}':\n\n" + "\n\n".join(formatted_results)
            else:
                return f"✅ Found {node_count} total nodes in database:\n\n" + "\n\n".join(formatted_results)
        else:
            error_msg = result[0].get("error", "Unknown error") if result else "No result"
            return f"❌ Failed to list nodes: {error_msg}"
    except Exception as e:
        logger.error(f"Exception in list_nodes: {e}")
        return f"❌ Error listing nodes: {str(e)}"

@mcp.tool
def create_relationship(from_node_id: str, to_node_id: str, relationship_type: str, properties: Optional[Dict[str, Any]] = None) -> str:
    """Create a relationship between two nodes."""
    logger.info(f"Create relationship tool called: {from_node_id} -[{relationship_type}]-> {to_node_id}")
    
    if not properties:
        properties = {}
    
    try:
        # Build Cypher query
        property_string = ", ".join([f"{k}: ${k}" for k in properties.keys()])
        
        if property_string:
            query = f"MATCH (a), (b) WHERE id(a) = {from_node_id} AND id(b) = {to_node_id} CREATE (a)-[r:{relationship_type} {{{property_string}}}]->(b) RETURN r"
        else:
            query = f"MATCH (a), (b) WHERE id(a) = {from_node_id} AND id(b) = {to_node_id} CREATE (a)-[r:{relationship_type}]->(b) RETURN r"
        
        result = execute_neo4j_query(query, properties)
        
        if result and len(result) > 0 and "error" not in result[0]:
            return f"✅ Relationship created: {from_node_id} -[{relationship_type}]-> {to_node_id} with properties: {properties}"
        else:
            error_msg = result[0].get("error", "Unknown error") if result else "No result"
            return f"❌ Failed to create relationship: {error_msg}"
    except Exception as e:
        logger.error(f"Exception in create_relationship: {e}")
        return f"❌ Error creating relationship: {str(e)}"

@mcp.tool
def execute_query(query: str, parameters: Optional[Dict[str, Any]] = None) -> str:
    """Execute a Cypher query and return results."""
    logger.info(f"Execute query tool called with query: {query}")
    
    try:
        result = execute_neo4j_query(query, parameters)
        
        if result and len(result) > 0 and "error" not in result[0]:
            # Format the results for display
            if len(result) == 1:
                return f"✅ Query executed successfully:\n{format_neo4j_result(result[0])}"
            else:
                formatted_results = []
                for i, record in enumerate(result, 1):
                    formatted_results.append(f"Result {i}:\n{format_neo4j_result(record)}")
                return f"✅ Query executed successfully ({len(result)} results):\n\n" + "\n\n".join(formatted_results)
        else:
            error_msg = result[0].get("error", "Unknown error") if result else "No result"
            return f"❌ Query failed: {error_msg}"
    except Exception as e:
        logger.error(f"Exception in execute_query: {e}")
        return f"❌ Query execution error: {str(e)}"

@mcp.tool
def get_node(node_id: Optional[int] = None, labels: Optional[List[str]] = None, properties: Optional[Dict[str, Any]] = None) -> str:
    """Get nodes by criteria."""
    logger.info(f"Get node tool called with node_id: {node_id}, labels: {labels}, properties: {properties}")
    
    try:
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
        
        result = execute_neo4j_query(query, parameters)
        
        if result and len(result) > 0 and "error" not in result[0]:
            return f"✅ Retrieved {len(result)} nodes successfully"
        else:
            error_msg = result[0].get("error", "Unknown error") if result else "No result"
            return f"❌ Failed to get nodes: {error_msg}"
    except Exception as e:
        logger.error(f"Exception in get_node: {e}")
        return f"❌ Error getting nodes: {str(e)}"

@mcp.tool
def update_node(node_id: int, properties: Optional[Dict[str, Any]] = None, labels: Optional[List[str]] = None) -> str:
    """Update a node."""
    logger.info(f"Update node tool called with node_id: {node_id}, properties: {properties}, labels: {labels}")
    
    try:
        # Build Cypher query
        set_clauses = []
        parameters = {"node_id": node_id}
        
        if properties:
            for key, value in properties.items():
                set_clauses.append(f"n.{key} = ${key}")
                parameters[key] = value
        
        if labels:
            # Remove existing labels and add new ones
            set_clauses.append("n = n")
            for label in labels:
                set_clauses.append(f"SET n:{label}")
        
        if set_clauses:
            query = f"MATCH (n) WHERE id(n) = $node_id SET {', '.join(set_clauses)} RETURN n"
        else:
            query = "MATCH (n) WHERE id(n) = $node_id RETURN n"
        
        result = execute_neo4j_query(query, parameters)
        
        if result and len(result) > 0 and "error" not in result[0]:
            return f"✅ Node {node_id} updated successfully"
        else:
            error_msg = result[0].get("error", "Unknown error") if result else "No result"
            return f"❌ Failed to update node: {error_msg}"
    except Exception as e:
        logger.error(f"Exception in update_node: {e}")
        return f"❌ Error updating node: {str(e)}"

@mcp.tool
def delete_node(node_id: int, cascade: bool = False) -> str:
    """Delete a node."""
    logger.info(f"Delete node tool called with node_id: {node_id}, cascade: {cascade}")
    
    try:
        if cascade:
            query = "MATCH (n) WHERE id(n) = $node_id DETACH DELETE n RETURN count(n) as deleted"
        else:
            query = "MATCH (n) WHERE id(n) = $node_id DELETE n RETURN count(n) as deleted"
        
        parameters = {"node_id": node_id}
        result = execute_neo4j_query(query, parameters)
        
        if result and len(result) > 0 and "error" not in result[0]:
            return f"✅ Node {node_id} deleted successfully"
        else:
            error_msg = result[0].get("error", "Unknown error") if result else "No result"
            return f"❌ Failed to delete node: {error_msg}"
    except Exception as e:
        logger.error(f"Exception in delete_node: {e}")
        return f"❌ Error deleting node: {str(e)}"

# ============================================================================
# ADVANCED ANALYTICS FUNCTIONS
# ============================================================================

@mcp.tool
def graph_analytics(analysis_type: str, node_label: Optional[str] = None, relationship_type: Optional[str] = None) -> str:
    """Perform advanced graph analytics on the Neo4j database."""
    logger.info(f"Graph analytics tool called with type: {analysis_type}, label: {node_label}, relationship: {relationship_type}")
    
    try:
        if analysis_type == "degree_centrality":
            if node_label:
                query = f"""
                MATCH (n:{node_label})
                OPTIONAL MATCH (n)-[r]-()
                RETURN n.name as node, size(collect(r)) as degree
                ORDER BY degree DESC
                LIMIT 10
                """
            else:
                query = """
                MATCH (n)
                OPTIONAL MATCH (n)-[r]-()
                RETURN labels(n)[0] as label, n.name as node, size(collect(r)) as degree
                ORDER BY degree DESC
                LIMIT 10
                """
        
        elif analysis_type == "betweenness_centrality":
            query = """
            MATCH (n)
            OPTIONAL MATCH path = shortestPath((start)-[*]-(end))
            WHERE start <> end AND n IN nodes(path)
            RETURN n.name as node, count(path) as betweenness
            ORDER BY betweenness DESC
            LIMIT 10
            """
        
        elif analysis_type == "community_detection":
            query = """
            CALL gds.louvain.stream('myGraph')
            YIELD nodeId, communityId
            RETURN gds.util.asNode(nodeId).name as node, communityId
            ORDER BY communityId
            """
        
        elif analysis_type == "path_analysis":
            if relationship_type:
                query = f"""
                MATCH path = (start)-[:{relationship_type}*1..5]-(end)
                WHERE start <> end
                RETURN start.name as start_node, end.name as end_node, length(path) as path_length
                ORDER BY path_length
                LIMIT 10
                """
            else:
                query = """
                MATCH path = (start)-[*1..5]-(end)
                WHERE start <> end
                RETURN start.name as start_node, end_node.name as end_node, length(path) as path_length
                ORDER BY path_length
                LIMIT 10
                """
        
        elif analysis_type == "node_similarity":
            query = """
            MATCH (n1), (n2)
            WHERE n1 <> n2
            WITH n1, n2, size([(n1)-[:SIMILAR_GENRE]-(n2) | 1]) as similarity
            WHERE similarity > 0
            RETURN n1.name as node1, n2.name as node2, similarity
            ORDER BY similarity DESC
            LIMIT 10
            """
        
        else:
            return f"❌ Unknown analysis type: {analysis_type}. Available types: degree_centrality, betweenness_centrality, community_detection, path_analysis, node_similarity"
        
        result = execute_neo4j_query(query)
        
        if result and len(result) > 0 and "error" not in result[0]:
            # Format the results for display
            formatted_results = []
            for i, record in enumerate(result, 1):
                formatted_results.append(f"Result {i}:\n{format_neo4j_result(record)}")
            
            return f"✅ {analysis_type.replace('_', ' ').title()} Analysis Results ({len(result)} results):\n\n" + "\n\n".join(formatted_results)
        else:
            error_msg = result[0].get("error", "Unknown error") if result else "No result"
            return f"❌ Failed to perform {analysis_type} analysis: {error_msg}"
    
    except Exception as e:
        logger.error(f"Exception in graph_analytics: {e}")
        return f"❌ Error performing graph analytics: {str(e)}"

@mcp.tool
def graph_statistics() -> str:
    """Get comprehensive statistics about the graph database."""
    logger.info("Graph statistics tool called")
    
    try:
        queries = {
            "node_count": "MATCH (n) RETURN count(n) as total_nodes",
            "relationship_count": "MATCH ()-[r]->() RETURN count(r) as total_relationships",
            "node_labels": "MATCH (n) RETURN labels(n) as labels, count(n) as count ORDER BY count DESC",
            "relationship_types": "MATCH ()-[r]->() RETURN type(r) as type, count(r) as count ORDER BY count DESC",
            "avg_degree": "MATCH (n) OPTIONAL MATCH (n)-[r]-() RETURN avg(size(collect(r))) as avg_degree",
            "density": """
            MATCH (n)
            MATCH ()-[r]->()
            RETURN toFloat(count(r)) / (count(n) * (count(n) - 1)) as density
            """
        }
        
        results = {}
        for stat_name, query in queries.items():
            result = execute_neo4j_query(query)
            if result and len(result) > 0 and "error" not in result[0]:
                results[stat_name] = result[0]
            else:
                results[stat_name] = {"error": "Failed to compute"}
        
        # Format the statistics
        formatted_stats = []
        for stat_name, result in results.items():
            if "error" not in result:
                formatted_stats.append(f"{stat_name.replace('_', ' ').title()}: {format_neo4j_result(result)}")
            else:
                formatted_stats.append(f"{stat_name.replace('_', ' ').title()}: {result['error']}")
        
        return f"✅ Graph Statistics:\n\n" + "\n".join(formatted_stats)
    
    except Exception as e:
        logger.error(f"Exception in graph_statistics: {e}")
        return f"❌ Error getting graph statistics: {str(e)}"

# ============================================================================
# RAG (RETRIEVAL-AUGMENTED GENERATION) FUNCTIONS
# ============================================================================

@mcp.tool
def create_vector_index(index_name: str, node_label: str, property_name: str, dimensions: int = 1536) -> str:
    """Create a vector index for RAG operations."""
    logger.info(f"Create vector index tool called with name: {index_name}, label: {node_label}, property: {property_name}")
    
    try:
        # Check if Neo4j Graph Data Science library is available
        check_query = "CALL dbms.procedures() YIELD name WHERE name CONTAINS 'gds' RETURN count(name) as gds_available"
        check_result = execute_neo4j_query(check_query)
        
        if not check_result or "error" in check_result[0] or check_result[0].get("gds_available", 0) == 0:
            return "❌ Neo4j Graph Data Science library not available. Please install GDS library for vector operations."
        
        # Create vector index
        query = f"""
        CALL db.index.vector.createNodeIndex(
            '{index_name}',
            '{node_label}',
            '{property_name}',
            {dimensions},
            'cosine'
        )
        """
        
        result = execute_neo4j_query(query)
        
        if result and len(result) > 0 and "error" not in result[0]:
            return f"✅ Vector index '{index_name}' created successfully for {node_label}.{property_name}"
        else:
            error_msg = result[0].get("error", "Unknown error") if result else "No result"
            return f"❌ Failed to create vector index: {error_msg}"
    
    except Exception as e:
        logger.error(f"Exception in create_vector_index: {e}")
        return f"❌ Error creating vector index: {str(e)}"

@mcp.tool
def semantic_search(query_vector: List[float], index_name: str, limit: int = 5) -> str:
    """Perform semantic search using vector similarity."""
    logger.info(f"Semantic search tool called with index: {index_name}, limit: {limit}")
    
    try:
        # Convert query vector to string format for Cypher
        vector_str = "[" + ", ".join(map(str, query_vector)) + "]"
        
        query = f"""
        CALL db.index.vector.queryNodes('{index_name}', {limit}, {vector_str})
        YIELD node, score
        RETURN node.name as name, node.description as description, score
        ORDER BY score DESC
        """
        
        result = execute_neo4j_query(query)
        
        if result and len(result) > 0 and "error" not in result[0]:
            # Format the results for display
            formatted_results = []
            for i, record in enumerate(result, 1):
                formatted_results.append(f"Result {i}:\n{format_neo4j_result(record)}")
            
            return f"✅ Semantic Search Results ({len(result)} results):\n\n" + "\n\n".join(formatted_results)
        else:
            error_msg = result[0].get("error", "Unknown error") if result else "No result"
            return f"❌ Failed to perform semantic search: {error_msg}"
    
    except Exception as e:
        logger.error(f"Exception in semantic_search: {e}")
        return f"❌ Error performing semantic search: {str(e)}"

@mcp.tool
def hybrid_search(text_query: str, node_label: str, vector_property: str, text_properties: List[str], limit: int = 5) -> str:
    """Perform hybrid search combining text and vector similarity."""
    logger.info(f"Hybrid search tool called with query: {text_query}, label: {node_label}")
    
    try:
        # Build text search conditions
        text_conditions = []
        for prop in text_properties:
            text_conditions.append(f"n.{prop} CONTAINS '{text_query}'")
        
        text_condition = " OR ".join(text_conditions) if text_conditions else "1=1"
        
        query = f"""
        MATCH (n:{node_label})
        WHERE {text_condition}
        RETURN n.name as name, n.{vector_property} as vector, n.description as description
        ORDER BY n.name
        LIMIT {limit}
        """
        
        result = execute_neo4j_query(query)
        
        if result and len(result) > 0 and "error" not in result[0]:
            # Format the results for display
            formatted_results = []
            for i, record in enumerate(result, 1):
                # Remove vector from display for readability
                if "vector" in record:
                    record["vector"] = f"[{len(record['vector'])} dimensions]"
                formatted_results.append(f"Result {i}:\n{format_neo4j_result(record)}")
            
            return f"✅ Hybrid Search Results ({len(result)} results):\n\n" + "\n\n".join(formatted_results)
        else:
            error_msg = result[0].get("error", "Unknown error") if result else "No result"
            return f"❌ Failed to perform hybrid search: {error_msg}"
    
    except Exception as e:
        logger.error(f"Exception in hybrid_search: {e}")
        return f"❌ Error performing hybrid search: {str(e)}"

@mcp.tool
def create_embedding_node(node_label: str, name: str, description: str, embedding: List[float]) -> str:
    """Create a node with embedding for RAG operations."""
    logger.info(f"Create embedding node tool called with label: {node_label}, name: {name}")
    
    try:
        # Convert embedding to string format for Cypher
        embedding_str = "[" + ", ".join(map(str, embedding)) + "]"
        
        query = f"""
        CREATE (n:{node_label} {{
            name: $name,
            description: $description,
            embedding: $embedding
        }})
        RETURN n
        """
        
        parameters = {
            "name": name,
            "description": description,
            "embedding": embedding
        }
        
        result = execute_neo4j_query(query, parameters)
        
        if result and len(result) > 0 and "error" not in result[0]:
            return f"✅ Embedding node created successfully: {name}"
        else:
            error_msg = result[0].get("error", "Unknown error") if result else "No result"
            return f"❌ Failed to create embedding node: {error_msg}"
    
    except Exception as e:
        logger.error(f"Exception in create_embedding_node: {e}")
        return f"❌ Error creating embedding node: {str(e)}"

@mcp.tool
def rag_context_retrieval(query: str, node_label: str, context_properties: List[str], limit: int = 3) -> str:
    """Retrieve relevant context for RAG operations based on text similarity."""
    logger.info(f"RAG context retrieval tool called with query: {query}, label: {node_label}")
    
    try:
        # Build context search conditions
        context_conditions = []
        for prop in context_properties:
            context_conditions.append(f"n.{prop} CONTAINS '{query}'")
        
        context_condition = " OR ".join(context_conditions) if context_conditions else "1=1"
        
        # Build return properties
        return_props = ", ".join([f"n.{prop} as {prop}" for prop in context_properties])
        
        query_cypher = f"""
        MATCH (n:{node_label})
        WHERE {context_condition}
        RETURN {return_props}
        ORDER BY n.name
        LIMIT {limit}
        """
        
        result = execute_neo4j_query(query_cypher)
        
        if result and len(result) > 0 and "error" not in result[0]:
            # Format the results for display
            formatted_results = []
            for i, record in enumerate(result, 1):
                formatted_results.append(f"Context {i}:\n{format_neo4j_result(record)}")
            
            return f"✅ RAG Context Retrieved ({len(result)} contexts):\n\n" + "\n\n".join(formatted_results)
        else:
            error_msg = result[0].get("error", "Unknown error") if result else "No result"
            return f"❌ Failed to retrieve RAG context: {error_msg}"
    
    except Exception as e:
        logger.error(f"Exception in rag_context_retrieval: {e}")
        return f"❌ Error retrieving RAG context: {str(e)}"

if __name__ == "__main__":
    # print("🚀 Neo4j MCP Server v2 Starting...")
    
    # print("Environment variables set:")
    # print(f"  NEO4J_URI: {os.environ['NEO4J_URI']}")
    # print(f"  NEO4J_USER: {os.environ['NEO4J_USER']}")
    # print(f"  NEO4J_DATABASE: {os.environ['NEO4J_DATABASE']}")
    # print(f"  NEO4J_PASSWORD: {'*' * len(os.environ['NEO4J_PASSWORD'])}")
    
    # # Test connection immediately using the same logic as test_neo4j_connection.py
    # print("Testing Neo4j connection...")
    # try:
    #     uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    #     user = os.getenv("NEO4J_USER", "neo4j")
    #     password = os.getenv("NEO4J_PASSWORD", "C0wb0ys1!")
    #     database = os.getenv("NEO4J_DATABASE", "neo4j")
        
    #     driver = GraphDatabase.driver(uri, auth=(user, password))
    #     with driver.session(database=database) as session:
    #         result = session.run("RETURN 1 as test")
    #         test_value = result.single()
    #         print(f"✅ Neo4j connection successful! Test value: {test_value['test']}")
    #     driver.close()
    # except Exception as e:
    #     print(f"❌ Neo4j connection failed: {e}")
    
    # Run the MCP server
    mcp.run()
