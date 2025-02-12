"""Table description tool implementation"""

from mcp.types import TextContent

from ..models import TableInput
from ..utils import format_as_csv, get_connection


async def describe_table(db_url: str, arguments: dict) -> list[TextContent]:
    """Get detailed schema information for a database table.

    Args:
        db_url: Database connection URL
        arguments: Tool arguments containing table name

    Returns:
        List of TextContent with table schema information in CSV format
    """
    table = TableInput(**arguments)
    with get_connection(db_url) as conn:
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

            # Format columns as CSV
            column_csv = format_as_csv(
                [
                    {
                        "column": col[0],
                        "type": col[1],
                        "max_length": col[2],
                        "default": col[3],
                        "nullable": col[4],
                    }
                    for col in columns
                ]
            )

            # Format constraints as CSV
            constraint_csv = format_as_csv(
                [
                    {"name": con[0], "type": con[1], "definition": con[2]}
                    for con in constraints
                ]
            )

            # Format indexes as CSV
            index_csv = format_as_csv(
                [{"name": idx[0], "definition": idx[1]} for idx in indexes]
            )

            result = "COLUMNS:\n" + column_csv + "\n\n"
            result += "CONSTRAINTS:\n" + constraint_csv + "\n\n"
            result += "INDEXES:\n" + index_csv

            return [TextContent(type="text", text=result)]
