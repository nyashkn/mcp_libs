# MCP Server Collection

A collection of Model Context Protocol (MCP) servers with centralized configuration management.

## Repository Structure

```
MCP/
├── Configuration
│   ├── cline_mcp_settings.template.json  # Template for all MCP servers
│   ├── .env.example                      # Example environment variables
│   ├── generate_settings.sh              # Script to generate settings files
│   ├── MCP_SETTINGS_SETUP.md            # Settings management documentation
│   └── GIT_SETUP.md                     # Git submodules documentation
│
├── External MCP Servers (Git Submodules)
│   ├── mcp-git-ingest/                  # GitHub repository analysis tools
│   ├── mcp-tavily/                      # Tavily search integration
│   └── perplexity-server/               # Perplexity API integration
│
└── Local MCP Servers
    ├── github-mcp/                      # GitHub API integration
    ├── mcp-pdf/                         # PDF processing tools
    ├── mcp-postgres/                    # PostgreSQL integration
    └── mcp-server-github/               # Additional GitHub tools
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

## External MCP Servers (Submodules)

These servers are maintained in their own repositories and included as Git submodules:

1. mcp-git-ingest
   - Source: https://github.com/adhikasp/mcp-git-ingest
   - Purpose: GitHub repository analysis tools

2. mcp-tavily
   - Source: https://github.com/RamXX/mcp-tavily
   - Purpose: Tavily search integration

3. perplexity-server
   - Source: https://github.com/DaInfernalCoder/researcher-mcp
   - Purpose: Perplexity API integration

### Updating Submodules

```bash
# Update all submodules
git submodule update --remote --merge

# Update specific submodule
cd [submodule-directory]
git pull origin main
cd ..
git add [submodule-directory]
git commit -m "Update [submodule-name]"
```

## Local MCP Servers

These servers are developed and maintained within this repository:

1. github-mcp
   - Purpose: GitHub API integration
   - Stack: Node.js

2. mcp-pdf
   - Purpose: PDF processing tools
   - Stack: Python

3. mcp-postgres
   - Purpose: PostgreSQL integration
   - Stack: Python

4. mcp-server-github
   - Purpose: Additional GitHub tools
   - Stack: Python

### Managing Local Servers

- Make changes directly in their directories
- Commit changes to the main repository
- Consider converting to standalone repositories and submodules when they mature

## Development Workflow

### For Submodules
1. Create feature branches in submodule repositories
2. Submit PRs to their respective repositories
3. Update submodule references after changes are merged

### For Local Servers
1. Make changes directly in their directories
2. Test changes locally
3. Commit to the main repository

## Contributing

1. For submodules:
   - Submit changes to their respective repositories
   - Update submodule references in this repository

2. For local servers:
   - Make changes directly in their directories
   - Follow the repository's coding standards
   - Include tests for new features

## License

- External MCP servers (submodules) maintain their own licenses
- Local MCP servers are licensed under this repository's license