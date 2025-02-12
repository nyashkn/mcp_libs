"""Index analysis tool implementation"""

from mcp.types import TextContent

from ..models import AnalyzeIndexInput
from ..utils import format_as_csv, get_connection


async def analyze_indexes(db_url: str, arguments: dict) -> list[TextContent]:
    """Analyze database index usage and provide optimization recommendations.

    Args:
        db_url: Database connection URL
        arguments: Tool arguments containing optional table name

    Returns:
        List of TextContent with index analysis in CSV format
    """
    try:
        analyze_input = AnalyzeIndexInput(**arguments)
        table_filter = "AND t.relname = %s" if analyze_input.table_name else ""
        params = (analyze_input.table_name,) if analyze_input.table_name else ()

        with get_connection(db_url) as conn:
            with conn.cursor() as cur:
                # Get index usage statistics
                cur.execute(
                    f"""
                    SELECT n.nspname || '.' || t.relname as table_name,
                           i.relname as index_name,
                           pg_size_pretty(pg_relation_size(i.oid)) as index_size,
                           s.idx_scan as number_of_scans,
                           s.idx_tup_read as tuples_read,
                           s.idx_tup_fetch as tuples_fetched
                    FROM pg_stat_user_indexes s
                    JOIN pg_class i ON s.indexrelid = i.oid
                    JOIN pg_class t ON s.relid = t.oid
                    JOIN pg_namespace n ON t.relnamespace = n.oid
                    WHERE 1=1 {table_filter}
                    ORDER BY pg_relation_size(i.oid) DESC
                """,
                    params,
                )
                index_stats = cur.fetchall()

                # Get unused indexes
                cur.execute(
                    f"""
                    SELECT n.nspname || '.' || t.relname as table_name,
                           i.relname as index_name,
                           pg_size_pretty(pg_relation_size(i.oid)) as index_size
                    FROM pg_stat_user_indexes s
                    JOIN pg_class i ON s.indexrelid = i.oid
                    JOIN pg_class t ON s.relid = t.oid
                    JOIN pg_namespace n ON t.relnamespace = n.oid
                    JOIN pg_index idx ON i.oid = idx.indexrelid
                    WHERE s.idx_scan = 0
                    AND NOT idx.indisprimary
                    AND NOT idx.indisunique
                    {table_filter}
                    ORDER BY pg_relation_size(i.oid) DESC
                """,
                    params,
                )
                unused_indexes = cur.fetchall()

                # Get missing index recommendations
                cur.execute(
                    f"""
                    SELECT n.nspname || '.' || t.relname as table_name,
                           s.seq_scan,
                           s.seq_tup_read,
                           s.idx_scan,
                           s.idx_tup_fetch
                    FROM pg_stat_user_tables s
                    JOIN pg_class t ON s.relid = t.oid
                    JOIN pg_namespace n ON t.relnamespace = n.oid
                    WHERE s.seq_scan > 0
                    {table_filter}
                    ORDER BY s.seq_scan DESC
                """,
                    params,
                )
                missing_indexes = cur.fetchall()

                # Format each section as CSV
                stats_csv = format_as_csv(
                    [
                        {
                            "table": stat[0],
                            "index": stat[1],
                            "size": stat[2],
                            "scans": stat[3],
                            "reads": stat[4],
                            "fetches": stat[5],
                        }
                        for stat in index_stats
                    ]
                )

                unused_csv = format_as_csv(
                    [
                        {"table": idx[0], "index": idx[1], "size": idx[2]}
                        for idx in unused_indexes
                    ]
                )

                missing_csv = format_as_csv(
                    [
                        {
                            "table": idx[0],
                            "seq_scans": idx[1],
                            "seq_reads": idx[2],
                            "idx_scans": idx[3],
                            "idx_fetches": idx[4],
                        }
                        for idx in missing_indexes
                    ]
                )

                result = "INDEX STATISTICS:\n" + stats_csv + "\n\n"
                result += "UNUSED INDEXES:\n" + unused_csv + "\n\n"
                result += "POTENTIAL MISSING INDEXES:\n" + missing_csv

                return [TextContent(type="text", text=result)]
    except Exception as e:
        return [TextContent(type="text", text=f"Error analyzing indexes: {str(e)}")]
