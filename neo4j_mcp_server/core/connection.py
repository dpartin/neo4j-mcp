"""Neo4j connection management for MCP Server."""

import asyncio
from typing import Optional, Dict, Any, List
from contextlib import asynccontextmanager
from neo4j import AsyncGraphDatabase, AsyncDriver, AsyncSession
from neo4j.exceptions import ServiceUnavailable, AuthError, ClientError

from ..config.settings import settings
from ..config.neo4j_config import Neo4jConfig
from .errors import ConnectionError, AuthenticationError, QueryError
from .logging import get_logger


logger = get_logger(__name__)


class Neo4jConnectionManager:
    """Manages Neo4j database connections and provides connection pooling."""
    
    def __init__(self, config: Optional[Neo4jConfig] = None):
        """
        Initialize the connection manager.
        
        Args:
            config: Neo4j configuration settings
        """
        self.config = config or Neo4jConfig(
            uri=settings.neo4j_uri,
            user=settings.neo4j_user,
            password=settings.neo4j_password,
            database=settings.neo4j_database,
            max_connection_pool_size=settings.connection_pool_size,
            connection_timeout=settings.query_timeout,
        )
        
        self._driver: Optional[AsyncDriver] = None
        self._is_connected = False
        
    async def connect(self) -> None:
        """Establish connection to Neo4j database."""
        try:
            logger.info("Connecting to Neo4j database", uri=self.config.uri)
            
            self._driver = AsyncGraphDatabase.driver(
                self.config.uri,
                auth=(self.config.user, self.config.password),
                **self.config.get_connection_config()
            )
            
            # Verify connection
            await self._verify_connection()
            self._is_connected = True
            
            logger.info("Successfully connected to Neo4j database")
            
        except AuthError as e:
            logger.error("Authentication failed", error=str(e))
            raise AuthenticationError(f"Neo4j authentication failed: {str(e)}")
        except ServiceUnavailable as e:
            logger.error("Neo4j service unavailable", error=str(e))
            raise ConnectionError(f"Neo4j service unavailable: {str(e)}")
        except Exception as e:
            logger.error("Failed to connect to Neo4j", error=str(e))
            raise ConnectionError(f"Failed to connect to Neo4j: {str(e)}")
    
    async def disconnect(self) -> None:
        """Close the connection to Neo4j database."""
        if self._driver:
            try:
                await self._driver.close()
                self._is_connected = False
                logger.info("Disconnected from Neo4j database")
            except Exception as e:
                logger.error("Error disconnecting from Neo4j", error=str(e))
    
    async def _verify_connection(self) -> None:
        """Verify that the connection is working."""
        try:
            async with self._driver.session(database=self.config.database) as session:
                result = await session.run("RETURN 1 as test")
                record = await result.single()
                if not record or record["test"] != 1:
                    raise ConnectionError("Connection verification failed")
        except Exception as e:
            raise ConnectionError(f"Connection verification failed: {str(e)}")
    
    @property
    def is_connected(self) -> bool:
        """Check if connected to Neo4j."""
        return self._is_connected and self._driver is not None
    
    @asynccontextmanager
    async def get_session(self, database: Optional[str] = None) -> AsyncSession:
        """
        Get a Neo4j session with automatic cleanup.
        
        Args:
            database: Database name (uses config default if None)
            
        Yields:
            Neo4j session
        """
        if not self.is_connected:
            raise ConnectionError("Not connected to Neo4j")
        
        session = None
        try:
            session = self._driver.session(database=database or self.config.database)
            yield session
        except Exception as e:
            logger.error("Session error", error=str(e))
            raise QueryError(f"Session error: {str(e)}")
        finally:
            if session:
                await session.close()
    
    async def execute_query(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
        database: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query and return results.
        
        Args:
            query: Cypher query string
            parameters: Query parameters
            database: Database name
            
        Returns:
            List of result records as dictionaries
        """
        async with self.get_session(database) as session:
            try:
                result = await session.run(query, parameters or {})
                records = await result.data()
                return records
            except ClientError as e:
                logger.error("Query execution failed", query=query, error=str(e))
                raise QueryError(f"Query execution failed: {str(e)}")
            except Exception as e:
                logger.error("Unexpected error during query execution", error=str(e))
                raise QueryError(f"Unexpected error: {str(e)}")
    
    async def execute_write_query(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
        database: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a write query and return summary.
        
        Args:
            query: Cypher write query string
            parameters: Query parameters
            database: Database name
            
        Returns:
            Query execution summary
        """
        async with self.get_session(database) as session:
            try:
                async with session.begin_transaction() as tx:
                    result = await tx.run(query, parameters or {})
                    summary = await result.consume()
                    await tx.commit()
                    return {
                        "nodes_created": summary.counters.nodes_created,
                        "nodes_deleted": summary.counters.nodes_deleted,
                        "relationships_created": summary.counters.relationships_created,
                        "relationships_deleted": summary.counters.relationships_deleted,
                        "properties_set": summary.counters.properties_set,
                        "labels_added": summary.counters.labels_added,
                        "labels_removed": summary.counters.labels_removed,
                        "indexes_added": summary.counters.indexes_added,
                        "indexes_removed": summary.counters.indexes_removed,
                        "constraints_added": summary.counters.constraints_added,
                        "constraints_removed": summary.counters.constraints_removed,
                    }
            except ClientError as e:
                logger.error("Write query execution failed", query=query, error=str(e))
                raise QueryError(f"Write query execution failed: {str(e)}")
            except Exception as e:
                logger.error("Unexpected error during write query execution", error=str(e))
                raise QueryError(f"Unexpected error: {str(e)}")
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the Neo4j connection.
        
        Returns:
            Health check results
        """
        try:
            if not self.is_connected:
                return {"status": "disconnected", "error": "Not connected to Neo4j"}
            
            # Test basic query
            result = await self.execute_query("RETURN 1 as health_check")
            
            if result and result[0]["health_check"] == 1:
                return {"status": "healthy", "database": self.config.database}
            else:
                return {"status": "unhealthy", "error": "Health check query failed"}
                
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}


# Global connection manager instance
connection_manager = Neo4jConnectionManager()
