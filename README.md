# MCP Server Collection

A collection of Model Context Protocol (MCP) servers with centralized configuration management.

## Repository Structure

```
MCP/
├── cline_mcp_settings.template.json  # Template for all MCP servers
├── .env.example                      # Example environment variables
├── generate_settings.sh              # Script to generate settings files
├── MCP_SETTINGS_SETUP.md            # Settings management documentation
├── GIT_SETUP.md                     # Git submodules documentation
│
├── Submodules (Git-managed):
│   ├── mcp-git-ingest/             # GitHub repository analysis tools
│   ├── mcp-tavily/                 # Tavily search integration
│   └── perplexity-server/          # Perplexity API integration
│
└── Other MCP Servers (Local):
    ├── github-mcp/                 # GitHub API integration
    ├── mcp-pdf/                    # PDF processing tools
    ├── mcp-postgres/               # PostgreSQL integration
    └── mcp-server-github/          # Additional GitHub tools
```

## Setup

1. Clone the repository with submodules:
```bash
git clone --recurse-submodules [repository-url]
```

2. Set up environment:
```bash
cp .env.example .env
# Edit .env with your values
```

3. Generate MCP settings:
```bash
chmod +x generate_settings.sh
./generate_settings.sh
```

## Documentation

- [MCP Settings Setup](MCP_SETTINGS_SETUP.md) - How to manage MCP settings
- [Git Setup](GIT_SETUP.md) - Working with Git submodules

## Submodules

Currently managed as Git submodules:

1. mcp-git-ingest
   - Source: https://github.com/adhikasp/mcp-git-ingest
   - Purpose: GitHub repository analysis tools

2. mcp-tavily
   - Source: https://github.com/RamXX/mcp-tavily
   - Purpose: Tavily search integration

3. perplexity-server
   - Source: https://github.com/DaInfernalCoder/researcher-mcp
   - Purpose: Perplexity API integration

## Local MCP Servers

These servers are currently managed locally:

- github-mcp: GitHub API integration
- mcp-pdf: PDF processing tools
- mcp-postgres: PostgreSQL integration
- mcp-server-github: Additional GitHub tools

## Contributing

1. For submodules:
   - Submit changes to their respective repositories
   - Update submodule references in this repository

2. For local servers:
   - Make changes directly in their directories
   - Consider converting to submodules if they become standalone projects

## License

Each MCP server maintains its own license. Please refer to individual server directories for their respective licenses.