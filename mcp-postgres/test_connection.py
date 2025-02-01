#!/usr/bin/env python3
"""Test script for PostgreSQL MCP server"""

import asyncio
import os

from mcp_server_postgres.server import serve

# Set PostgreSQL connection details
os.environ["DATABASE_URL"] = (
    "postgresql://mdundo_looker_analytics:rf@KT24deiY!Um@IYtPx@89.58.17.141:5030/mdundo_analytics"
)


async def test_query():
    """Test the execute_query tool"""
    server = await serve()
    result = await server.call_tool(
        "execute_query", {"sql": "SELECT * FROM md_payment_opera_daily_ppl_1 LIMIT 10"}
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(test_query())
