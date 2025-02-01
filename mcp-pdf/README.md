# MCP PDF Server

An MCP server that provides PDF processing capabilities using PyMuPDF4LLM. This server enables extraction of content from PDFs in formats suitable for LLMs and RAG systems.

## Features

- Process PDFs from local files or URLs
- Support for multi-column page layouts
- Image and vector graphics extraction
- Page chunking for better context handling
- Output in Markdown or LlamaIndex format
- Handles complex PDF structures

## Installation

1. Install dependencies using uv:
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
.venv\Scripts\activate     # On Windows
uv pip install -e .
```

## Usage

The server provides two main tools:

### 1. process_pdf_file

Process a PDF from a local file path:

```python
result = await mcp.use_tool("mcp-pdf", "process_pdf_file", {
    "file_path": "/path/to/document.pdf",
    "output_format": "markdown"  # or "llamaindex"
})
```

### 2. process_pdf_url

Process a PDF from a URL:

```python
result = await mcp.use_tool("mcp-pdf", "process_pdf_url", {
    "url": "https://example.com/document.pdf",
    "output_format": "markdown"  # or "llamaindex"
})
```

## Output Formats

1. **Markdown**: Structured text with headers, lists, and basic formatting
2. **LlamaIndex**: Optimized format for LlamaIndex document processing

## Error Handling

The server handles various error cases:
- Invalid file paths
- Failed URL downloads
- PDF processing errors
- Invalid output format specifications

## Dependencies

- pymupdf4llm: PDF processing and content extraction
- requests: URL downloads
- mcp-python-sdk: MCP server implementation
