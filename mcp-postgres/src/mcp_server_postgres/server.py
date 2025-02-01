"""PostgreSQL MCP Server implementation"""

import json
import os

import psycopg2
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.shared.exceptions import McpError
from mcp.types import (
    INTERNAL_ERROR,
    INVALID_PARAMS,
    TextContent,
    Tool,
)
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel


class QueryInput(BaseModel):
    """Input schema for the query tool"""

    sql: str


class TableInput(BaseModel):
    """Input schema for table-specific tools"""

    table_name: str


def get_connection():
    """Get a database connection with read-only transaction"""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is required")

    conn = psycopg2.connect(database_url)
    conn.set_session(readonly=True)
    return conn


async def serve() -> None:
    """Run the PostgreSQL MCP server."""
    server = Server("postgres-mcp")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="execute_query",
                description="""Execute a read-only SQL query against the PostgreSQL database.
                This tool allows you to run SELECT queries to retrieve data. For security,
                only read operations are allowed - no modifications can be made to the database.""",
                inputSchema=QueryInput.model_json_schema(),
            ),
            Tool(
                name="describe_table",
                description="""Get detailed schema information for a database table.
                This tool provides comprehensive information about a table's structure including:
                - Column definitions (names, types, constraints)
                - Table constraints (primary keys, foreign keys, etc.)
                - Index definitions""",
                inputSchema=TableInput.model_json_schema(),
            ),
            Tool(
                name="list_tables",
                description="""List all tables in the database with their sizes and row counts.
                This tool provides an overview of all tables in the database, including:
                - Schema name
                - Table name
                - Table size (human readable)
                - Approximate row count""",
                inputSchema={},
            ),
            Tool(
                name="analyze_indexes",
                description="""Analyze database index usage and provide optimization recommendations.
                This tool performs a comprehensive analysis of index usage including:
                - Index usage statistics (scans, reads, fetches)
                - Identification of unused indexes
                - Potential missing index recommendations based on table scan patterns""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table_name": {
                            "type": "string",
                            "description": "Optional table name to analyze",
                        }
                    },
                },
            ),
            Tool(
                name="get_table_sample",
                description="""Get table schema and sample data for analysis.
                This tool provides both the table structure and a random sample of data,
                which is useful for understanding the table's content and format.""",
                inputSchema=TableInput.model_json_schema(),
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        try:
            if name == "execute_query":
                query = QueryInput(**arguments)
                with get_connection() as conn:
                    with conn.cursor(cursor_factory=RealDictCursor) as cur:
                        cur.execute(query.sql)
                        results = cur.fetchall()
                        return [
                            TextContent(type="text", text=json.dumps(results, indent=2))
                        ]

            elif name == "describe_table":
                table = TableInput(**arguments)
                with get_connection() as conn:
                    with conn.cursor() as cur:
                        # Get column information
                        cur.execute(
                            """
                            SELECT column_name, data_type, character_maximum_length, 
                                   column_default, is_nullable
                            FROM information_schema.columns 
                            WHERE table_name = %s
                            ORDER BY ordinal_position
                        """,
                            (table.table_name,),
                        )
                        columns = cur.fetchall()

                        # Get constraint information
                        cur.execute(
                            """
                            SELECT c.conname as constraint_name,
                                   c.contype as constraint_type,
                                   pg_get_constraintdef(c.oid) as definition
                            FROM pg_constraint c
                            JOIN pg_class t ON c.conrelid = t.oid
                            WHERE t.relname = %s
                        """,
                            (table.table_name,),
                        )
                        constraints = cur.fetchall()

                        # Get index information
                        cur.execute(
                            """
                            SELECT indexname, indexdef
                            FROM pg_indexes
                            WHERE tablename = %s
                        """,
                            (table.table_name,),
                        )
                        indexes = cur.fetchall()

                        return [
                            TextContent(
                                type="text",
                                text=json.dumps(
                                    {
                                        "columns": columns,
                                        "constraints": constraints,
                                        "indexes": indexes,
                                    },
                                    indent=2,
                                ),
                            )
                        ]

            elif name == "list_tables":
                with get_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            SELECT schemaname, tablename, 
                                   pg_size_pretty(pg_total_relation_size(quote_ident(schemaname) || '.' || quote_ident(tablename))) as size,
                                   pg_stat_get_live_tuples(c.oid) as row_count
                            FROM pg_tables t
                            JOIN pg_class c ON c.relname = t.tablename
                            WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
                            ORDER BY pg_total_relation_size(quote_ident(schemaname) || '.' || quote_ident(tablename)) DESC
                        """)
                        tables = cur.fetchall()
                        return [
                            TextContent(type="text", text=json.dumps(tables, indent=2))
                        ]

            elif name == "analyze_indexes":
                table_name = arguments.get("table_name")
                table_filter = (
                    "AND schemaname || '.' || tablename = %s" if table_name else ""
                )
                params = (table_name,) if table_name else ()

                with get_connection() as conn:
                    with conn.cursor() as cur:
                        # Get index usage statistics
                        cur.execute(
                            f"""
                            SELECT schemaname || '.' || tablename as table_name,
                                   indexrelname as index_name,
                                   pg_size_pretty(pg_relation_size(i.indexrelid)) as index_size,
                                   idx_scan as number_of_scans,
                                   idx_tup_read as tuples_read,
                                   idx_tup_fetch as tuples_fetched
                            FROM pg_stat_user_indexes ui
                            JOIN pg_index i ON ui.indexrelid = i.indexrelid
                            WHERE 1=1 {table_filter}
                            ORDER BY pg_relation_size(i.indexrelid) DESC
                        """,
                            params,
                        )
                        index_stats = cur.fetchall()

                        # Get unused indexes
                        cur.execute(
                            f"""
                            SELECT schemaname || '.' || tablename as table_name,
                                   indexrelname as index_name,
                                   pg_size_pretty(pg_relation_size(i.indexrelid)) as index_size
                            FROM pg_stat_user_indexes ui
                            JOIN pg_index i ON ui.indexrelid = i.indexrelid
                            WHERE idx_scan = 0
                            AND NOT indisprimary
                            AND NOT indisunique
                            {table_filter}
                            ORDER BY pg_relation_size(i.indexrelid) DESC
                        """,
                            params,
                        )
                        unused_indexes = cur.fetchall()

                        # Get missing index recommendations
                        cur.execute(
                            f"""
                            SELECT schemaname || '.' || tablename as table_name,
                                   seq_scan,
                                   seq_tup_read,
                                   idx_scan,
                                   idx_tup_fetch
                            FROM pg_stat_user_tables
                            WHERE seq_scan > 0
                            {table_filter}
                            ORDER BY seq_scan DESC
                        """,
                            params,
                        )
                        missing_indexes = cur.fetchall()

                        return [
                            TextContent(
                                type="text",
                                text=json.dumps(
                                    {
                                        "index_statistics": index_stats,
                                        "unused_indexes": unused_indexes,
                                        "potential_missing_indexes": missing_indexes,
                                    },
                                    indent=2,
                                ),
                            )
                        ]

            elif name == "get_table_sample":
                table = TableInput(**arguments)
                with get_connection() as conn:
                    with conn.cursor(cursor_factory=RealDictCursor) as cur:
                        # Get schema
                        cur.execute(
                            """
                            SELECT column_name, data_type, is_nullable, column_default
                            FROM information_schema.columns
                            WHERE table_name = %s
                            ORDER BY ordinal_position
                        """,
                            (table.table_name,),
                        )
                        schema = cur.fetchall()

                        # Get sample data
                        cur.execute(f"""
                            SELECT *
                            FROM {table.table_name}
                            ORDER BY random()
                            LIMIT 10
                        """)
                        sample_data = cur.fetchall()

                        return [
                            TextContent(
                                type="text",
                                text=json.dumps(
                                    {"schema": schema, "sample_data": sample_data},
                                    indent=2,
                                ),
                            )
                        ]

            else:
                raise McpError(INVALID_PARAMS, f"Unknown tool: {name}")

        except psycopg2.Error as e:
            raise McpError(INTERNAL_ERROR, f"Database error: {str(e)}")
        except Exception as e:
            raise McpError(INTERNAL_ERROR, f"Error: {str(e)}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)


if __name__ == "__main__":
    import asyncio

    asyncio.run(serve())
