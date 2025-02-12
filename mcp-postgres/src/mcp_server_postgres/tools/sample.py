"""Sample data tool implementation"""

from mcp.types import TextContent
from psycopg2.extras import RealDictCursor

from ..models import TableInput
from ..utils import format_as_csv, get_connection


async def get_table_sample(db_url: str, arguments: dict) -> list[TextContent]:
    """Get table schema and sample data.

    Args:
        db_url: Database connection URL
        arguments: Tool arguments containing table name

    Returns:
        List of TextContent with schema and sample data in CSV format
    """
    table = TableInput(**arguments)
    with get_connection(db_url) as conn:
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

            # Format schema as CSV
            schema_csv = format_as_csv(
                [
                    {
                        "column": s[0],
                        "type": s[1],
                        "nullable": s[2],
                        "default": s[3],
                    }
                    for s in schema
                ]
            )

            # Format sample data as CSV
            sample_csv = format_as_csv(sample_data)

            result = "SCHEMA:\n" + schema_csv + "\n\nSAMPLE DATA:\n" + sample_csv
            return [TextContent(type="text", text=result)]
