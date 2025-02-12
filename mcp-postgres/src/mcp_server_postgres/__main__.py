"""Entry point for the PostgreSQL MCP server"""

import asyncio
import os
import sys


def main():
    """Main entry point"""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("Error: DATABASE_URL environment variable is required", file=sys.stderr)
        print("Format: postgresql://user:password@host:port/dbname", file=sys.stderr)
        sys.exit(1)

    from .server import serve

    asyncio.run(serve(database_url))


if __name__ == "__main__":
    main()
