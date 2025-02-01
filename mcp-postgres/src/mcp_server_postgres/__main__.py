"""Entry point for the PostgreSQL MCP server"""

import asyncio
import os
import sys


def main():
    """Main entry point"""
    if not os.getenv("DATABASE_URL"):
        print("Error: DATABASE_URL environment variable is required", file=sys.stderr)
        print("Format: postgresql://user:password@host:port/dbname", file=sys.stderr)
        sys.exit(1)

    from .server import serve

    asyncio.run(serve())


if __name__ == "__main__":
    main()
