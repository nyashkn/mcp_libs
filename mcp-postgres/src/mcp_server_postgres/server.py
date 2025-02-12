"""PostgreSQL MCP Server implementation"""

import os

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
)

from .tools import TOOL_IMPLEMENTATIONS, TOOLS


async def serve(database_url: str | None = None) -> None:
    """Run the PostgreSQL MCP server.

    Args:
        database_url: Optional database URL. If not provided, will use DATABASE_URL env var.
    """
    db_url = database_url or os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable is required")

    server = Server("postgres")

    @server.list_tools()
    async def list_tools():
        return TOOLS

    @server.list_prompts()
    async def list_prompts() -> list[Prompt]:
        return [
            Prompt(
                name="execute_query",
                description="Execute a SQL query against the PostgreSQL database",
                arguments=[
                    PromptArgument(
                        name="sql",
                        description="SQL query to execute",
                        required=True,
                    ),
                ],
            ),
            Prompt(
                name="describe_table",
                description="Get detailed schema information for a database table",
                arguments=[
                    PromptArgument(
                        name="table_name",
                        description="Name of the table to describe",
                        required=True,
                    ),
                ],
            ),
            Prompt(
                name="analyze_indexes",
                description="Analyze database index usage and get optimization recommendations",
                arguments=[
                    PromptArgument(
                        name="table_name",
                        description="Optional: Name of the table to analyze indexes for",
                        required=False,
                    ),
                ],
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        try:
            if name not in TOOL_IMPLEMENTATIONS:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]

            return await TOOL_IMPLEMENTATIONS[name](db_url, arguments)
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    @server.get_prompt()
    async def get_prompt(name: str, arguments: dict | None) -> GetPromptResult:
        try:
            if not arguments:
                return GetPromptResult(
                    description="Missing arguments",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(
                                type="text",
                                text="Please provide the required arguments",
                            ),
                        )
                    ],
                )

            result = await TOOL_IMPLEMENTATIONS[name](db_url, arguments)
            return GetPromptResult(
                description=f"Results for {name}",
                messages=[
                    PromptMessage(
                        role="user",
                        content=result[0],  # Take first TextContent from tool result
                    )
                ],
            )
        except Exception as e:
            return GetPromptResult(
                description=f"Error executing {name}",
                messages=[
                    PromptMessage(
                        role="user",
                        content=TextContent(type="text", text=f"Error: {str(e)}"),
                    )
                ],
            )

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)


if __name__ == "__main__":
    import asyncio

    asyncio.run(serve())
