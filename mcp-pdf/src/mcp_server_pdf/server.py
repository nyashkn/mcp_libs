"""MCP server implementation for PDF processing using PyMuPDF4LLM."""

from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Annotated, Literal

import pymupdf4llm
import requests
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.shared.exceptions import McpError
from mcp.types import (
    INTERNAL_ERROR,
    INVALID_PARAMS,
    TextContent,
    Tool,
)
from pydantic import BaseModel, Field


class PDFProcessBase(BaseModel):
    """Base parameters for PDF processing."""

    output_format: Annotated[
        Literal["markdown", "llamaindex"],
        Field(
            default="markdown",
            description="Output format - 'markdown' or 'llamaindex'",
        ),
    ]


class PDFProcessFile(PDFProcessBase):
    """Parameters for processing PDF from file path."""

    file_path: Annotated[
        str,
        Field(description="Path to the PDF file to process"),
    ]


class PDFProcessURL(PDFProcessBase):
    """Parameters for processing PDF from URL."""

    url: Annotated[
        str,
        Field(description="URL of the PDF file to process"),
    ]


async def serve() -> None:
    """Run the PDF processing MCP server."""
    server = Server("mcp-pdf")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="process_pdf_file",
                description="""Process a PDF file from a local file path.
                Extracts content using PyMuPDF4LLM with support for:
                - Multi-column page layouts
                - Image and vector graphics extraction
                - Page chunking
                - Output in Markdown or LlamaIndex format
                
                Ideal for converting PDFs into formats suitable for LLMs and RAG systems.""",
                inputSchema=PDFProcessFile.model_json_schema(),
            ),
            Tool(
                name="process_pdf_url",
                description="""Process a PDF file from a URL.
                Downloads and extracts content using PyMuPDF4LLM with support for:
                - Multi-column page layouts
                - Image and vector graphics extraction
                - Page chunking
                - Output in Markdown or LlamaIndex format
                
                Ideal for converting PDFs into formats suitable for LLMs and RAG systems.""",
                inputSchema=PDFProcessURL.model_json_schema(),
            ),
        ]

    def process_pdf(file_path: str | Path, output_format: str) -> str:
        """Process a PDF file and return extracted content."""
        try:
            result = pymupdf4llm.to_markdown(str(file_path))
            return result
        except Exception as e:
            raise McpError(INTERNAL_ERROR, f"Failed to process PDF: {str(e)}")

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        try:
            if name == "process_pdf_file":
                args = PDFProcessFile(**arguments)
                if not Path(args.file_path).exists():
                    raise McpError(INVALID_PARAMS, f"File not found: {args.file_path}")
                result = process_pdf(args.file_path, args.output_format)

            elif name == "process_pdf_url":
                args = PDFProcessURL(**arguments)
                try:
                    response = requests.get(args.url)
                    response.raise_for_status()

                    # Save downloaded PDF to temporary file
                    with NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                        temp_file.write(response.content)
                        temp_path = temp_file.name

                    try:
                        result = process_pdf(temp_path, args.output_format)
                    finally:
                        # Clean up temporary file
                        Path(temp_path).unlink(missing_ok=True)

                except requests.RequestException as e:
                    raise McpError(INVALID_PARAMS, f"Failed to download PDF: {str(e)}")

            else:
                raise McpError(INVALID_PARAMS, f"Unknown tool: {name}")

            return [
                TextContent(
                    type="text",
                    text=result,
                )
            ]

        except Exception as e:
            if isinstance(e, McpError):
                raise
            raise McpError(INTERNAL_ERROR, str(e))

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
