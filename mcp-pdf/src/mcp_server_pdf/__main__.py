"""Main entry point for the PDF processing MCP server."""

import asyncio

from .server import serve


def main() -> None:
    """Run the PDF processing MCP server."""
    asyncio.run(serve())


if __name__ == "__main__":
    main()
