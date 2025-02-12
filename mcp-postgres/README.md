# PostgreSQL MCP Server Tools

## Available Tools

1. `execute_query` - Execute read-only SQL queries against the connected database
   ```json
   {
     "sql": "SELECT * FROM table_name LIMIT 10"
   }
   ```
   Example:
   ```json
   {
     "sql": "SELECT * FROM md_subs_revenue_monthly_ppl LIMIT 10"
   }
   ```

2. `describe_table` - Get detailed schema information for a specific table
   ```json
   {
     "table_name": "your_table_name"
   }
   ```

3. `list_tables` - List all tables in the database with their sizes and row counts
   - No input parameters required
   - Returns CSV format: schema,table,size,rows

4. `analyze_indexes` - Get index usage statistics and recommendations
   ```json
   {
     "table_name": "optional_table_name"  // Optional parameter
   }
   ```
   - Returns three sections in CSV format:
     1. Index Statistics
     2. Unused Indexes
     3. Potential Missing Indexes

5. `get_table_sample` - Get table schema and sample data (up to 10 random rows)
   ```json
   {
     "table_name": "your_table_name"
   }
   ```
   - Returns two sections:
     1. Schema (column definitions)
     2. Sample Data (up to 10 random rows)

## Configuration

The server requires PostgreSQL connection details via environment variables:

```bash
export DATABASE_URL=postgresql://user:password@hostname:port/dbname
```

OR

```bash
export PG_HOST=hostname
export PG_PORT=5432
export PG_DATABASE=dbname
export PG_USER=username
export PG_PASSWORD=password