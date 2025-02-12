"""Models for PostgreSQL MCP Server"""

from pydantic import BaseModel


class QueryInput(BaseModel):
    """Input schema for the query tool"""

    sql: str


class TableInput(BaseModel):
    """Input schema for table-specific tools"""

    table_name: str


class AnalyzeIndexInput(BaseModel):
    """Input schema for analyze_indexes tool"""

    table_name: str | None = None
