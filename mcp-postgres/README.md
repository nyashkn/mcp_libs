# PostgreSQL MCP Server

A Model Context Protocol (MCP) server that provides read-only access to PostgreSQL databases. This server enables LLMs to inspect database schemas, execute read-only queries, and perform DBA activities like checking indexes.

## Features

### Tools

1. `query` - Execute read-only SQL queries against the connected database
   - Input: SQL query string
   - All queries are executed within a READ ONLY transaction
   - Returns formatted results with column headers

2. `describe_table` - Get detailed schema information for a specific table
   - Input: Table name
   - Returns: Column definitions, data types, constraints, and indexes

3. `list_tables` - List all tables in the database with their row counts
   - Returns: Table names and approximate row counts

4. `analyze_indexes` - Get index usage statistics and recommendations
   - Input: Optional table name to analyze specific table
   - Returns: Index statistics, unused indexes, and missing index suggestions

5. `schema_and_sample` - Get table schema and sample data
   - Input: Table name
   - Returns: Schema definition and up to 10 random rows
   - Helps LLMs understand both structure and content

## Installation

```bash
uv pip install mcp-postgres
```

## Configuration

The server requires PostgreSQL connection details which can be provided in two ways:

1. Environment variables:
```bash
export PG_HOST=hostname
export PG_PORT=5432
export PG_DATABASE=dbname
export PG_USER=username
export PG_PASSWORD=password
```

2. Connection URL:
```bash
export DATABASE_URL=postgresql://user:password@hostname:port/dbname
```

## Usage with Claude Desktop

Add to your Claude settings:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "mcp-postgres",
      "env": {
        "DATABASE_URL": "postgresql://user:password@hostname:port/dbname"
      }
    }
  }
}
```

## Example Usage

1. Get table schema:
```sql
Tell me about the structure of the users table
```

2. Query data:
```sql
Show me the top 5 most active users from last month
```

3. Analyze indexes:
```sql
What indexes should I add to optimize the orders table?
```

## Development

1. Clone the repository
2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv pip install -e .
```

4. Run the server:
```bash
python -m mcp_server_postgres
```

## Security

- All queries are executed in READ ONLY transactions
- No DDL or DML operations are allowed
- Connection parameters are validated
- Query timeout limits are enforced

## License

MIT License - see LICENSE file for details.