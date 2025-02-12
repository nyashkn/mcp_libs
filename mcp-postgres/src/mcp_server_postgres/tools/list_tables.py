"""List tables tool implementation"""

from mcp.types import TextContent

from ..utils import format_as_csv, get_connection


async def list_tables(db_url: str, arguments: dict) -> list[TextContent]:
    """List all tables in the database with their sizes and row counts.

    Args:
        db_url: Database connection URL
        arguments: Empty dict (no arguments needed)

    Returns:
        List of TextContent with table list in CSV format
    """
    with get_connection(db_url) as conn:
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
            csv_data = format_as_csv(
                [
                    {
                        "schema": t[0],
                        "table": t[1],
                        "size": t[2],
                        "rows": t[3],
                    }
                    for t in tables
                ]
            )
            return [TextContent(type="text", text=csv_data)]
