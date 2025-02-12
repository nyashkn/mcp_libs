"""Utility functions for PostgreSQL MCP Server"""

import psycopg2


def format_as_csv(data: list, include_headers: bool = True) -> str:
    """Format query results as CSV.

    Args:
        data: List of dictionaries containing query results
        include_headers: Whether to include column headers

    Returns:
        CSV formatted string
    """
    if not data:
        return ""

    # Get headers from first row
    headers = list(data[0].keys())

    # Build CSV string
    lines = []
    if include_headers:
        lines.append(",".join(headers))

    for row in data:
        # Handle special characters and escaping
        values = []
        for header in headers:
            value = str(row[header] if row[header] is not None else "")
            if "," in value or '"' in value or "\n" in value:
                value = f'"{value.replace("`", "``")}"'
            values.append(value)
        lines.append(",".join(values))

    return "\n".join(lines)


def get_connection(database_url: str):
    """Get a database connection with read-only transaction

    Args:
        database_url: PostgreSQL connection URL
    """
    conn = psycopg2.connect(database_url)
    conn.set_session(readonly=True)
    return conn
