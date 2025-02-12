"""Query tool implementation"""

from mcp.types import TextContent
from psycopg2.extras import RealDictCursor

from ..models import QueryInput
from ..utils import format_as_csv, get_connection


async def execute_query(db_url: str, arguments: dict) -> list[TextContent]:
    """Execute a read-only SQL query.

    Args:
        db_url: Database connection URL
        arguments: Tool arguments containing SQL query

    Returns:
        List of TextContent with query results in CSV format
    """
    query = QueryInput(**arguments)
    with get_connection(db_url) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query.sql)
            results = cur.fetchall()
            csv_data = format_as_csv(results)
            return [TextContent(type="text", text=csv_data)]
