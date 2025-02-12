"""PostgreSQL MCP Server tools"""

from mcp.types import Tool

from ..models import AnalyzeIndexInput, QueryInput, TableInput
from .analyze import analyze_indexes
from .describe import describe_table
from .list_tables import list_tables
from .query import execute_query
from .sample import get_table_sample

# Tool definitions with their descriptions and input schemas
TOOLS = [
    Tool(
        name="execute_query",
        description="""Execute a read-only SQL query against the PostgreSQL database.
        
        This tool allows you to run SELECT queries to retrieve data. Results are returned in CSV format
        for efficient token usage and easy import into spreadsheets.

        Examples:
        - Basic query: SELECT * FROM users LIMIT 5
        - Filtered query: SELECT name, email FROM users WHERE active = true
        - Aggregation: SELECT department, COUNT(*) FROM employees GROUP BY department
        
        Notes:
        - Only SELECT queries are allowed for security
        - Results include headers by default
        - NULL values are shown as empty strings
        - Special characters are properly escaped""",
        inputSchema=QueryInput.model_json_schema(),
    ),
    Tool(
        name="describe_table",
        description="""Get detailed schema information for a database table.
        
        This tool provides comprehensive information about a table's structure including:
        - Column definitions (names, types, constraints)
        - Table constraints (primary keys, foreign keys, etc.)
        - Index definitions
        
        Example:
        - Get schema: describe_table users
        
        The output is formatted as CSV with sections for:
        1. Columns: name,type,nullable,default
        2. Constraints: name,type,definition
        3. Indexes: name,definition""",
        inputSchema=TableInput.model_json_schema(),
    ),
    Tool(
        name="list_tables",
        description="""List all tables in the database with their sizes and row counts.
        
        This tool provides an overview of all tables in the database, including:
        - Schema name
        - Table name 
        - Table size (human readable)
        - Approximate row count
        
        Output is in CSV format:
        schema,table,size,rows
        
        Example output:
        public,users,1.2 GB,50000
        public,orders,500 MB,100000""",
        inputSchema={},
    ),
    Tool(
        name="analyze_indexes",
        description="""Analyze database index usage and provide optimization recommendations.
        
        This tool performs a comprehensive analysis of index usage including:
        - Index usage statistics (scans, reads, fetches)
        - Identification of unused indexes
        - Missing index suggestions based on table scan patterns
        
        Optional: Specify a table name to analyze indexes for just that table.
        
        Output sections (CSV format):
        1. Index Statistics: table,index,size,scans,reads,fetches
        2. Unused Indexes: table,index,size
        3. Missing Index Suggestions: table,scans,reads""",
        inputSchema=AnalyzeIndexInput.model_json_schema(),
    ),
    Tool(
        name="get_table_sample",
        description="""Get table schema and sample data for analysis.
        
        This tool provides both the table structure and a random sample of data,
        which is useful for understanding the table's content and format.
        
        Output sections (CSV format):
        1. Schema: column,type,nullable,default
        2. Sample Data: [actual table columns]
           - Includes up to 10 random rows
           - Headers match table structure
           - Special characters are escaped
        
        Example:
        get_table_sample users
        
        Schema:
        column,type,nullable,default
        id,integer,NO,nextval('users_id_seq')
        name,text,NO,
        email,text,NO,
        
        Sample Data:
        id,name,email
        1,John Doe,john@example.com
        2,Jane Smith,jane@example.com""",
        inputSchema=TableInput.model_json_schema(),
    ),
]

# Map tool names to their implementation functions
TOOL_IMPLEMENTATIONS = {
    "execute_query": execute_query,
    "describe_table": describe_table,
    "list_tables": list_tables,
    "analyze_indexes": analyze_indexes,
    "get_table_sample": get_table_sample,
}
