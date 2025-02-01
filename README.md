# MCP Server Collection

A collection of Model Context Protocol (MCP) servers with centralized configuration management.

## Table of Contents
- [MCP Server Collection](#mcp-server-collection)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Repository Structure](#repository-structure)
  - [Quick Start](#quick-start)
  - [Configuration Management](#configuration-management)
    - [Environment Variables](#environment-variables)
    - [Settings Management](#settings-management)
  - [Managing MCP Servers](#managing-mcp-servers)
    - [Adding a New External MCP Server](#adding-a-new-external-mcp-server)
    - [Updating External Servers](#updating-external-servers)
    - [Creating a New Local MCP Server](#creating-a-new-local-mcp-server)
  - [Development Guidelines](#development-guidelines)
  - [Security](#security)
    - [Sensitive Data Management](#sensitive-data-management)
    - [Backup Management](#backup-management)
  - [Make Commands](#make-commands)
  - [Contributing](#contributing)
  - [License](#license)

## Overview

This repository manages multiple MCP servers, both as Git submodules (external servers) and regular directories (local development servers). It provides centralized configuration management and development guidelines.

## Repository Structure

```
MCP/
├── Configuration
│   ├── cline_mcp_settings.template.json  # Template for all MCP servers
│   ├── .env.example                      # Example environment variables
│   └── Makefile                          # Build and management commands
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

## Quick Start

1. Clone the repository with submodules:
```bash
git clone --recurse-submodules [repository-url]
cd mcp-collection
```

2. Initial setup:
```bash
make setup              # Installs dependencies and creates .env
make generate-settings  # Generates MCP settings files
```

## Configuration Management

### Environment Variables

1. Copy the example file:
```bash
cp .env.example .env
```

2. Edit `.env` with your values:
```bash
# Base paths
PROJECT_PATH=/path/to/project
VENV_PATH=/path/to/venv

# API Keys
GITHUB_TOKEN=your_token
PERPLEXITY_API_KEY=your_key
TAVILY_API_KEY=your_key
```

### Settings Management

The `generate_settings.sh` script handles MCP settings:

```bash
# Generate settings with backup
make backup-settings

# Validate environment and settings
make validate

# Generate new settings
make generate-settings
```

Settings are generated in:
- `/Users/username/Library/Application Support/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json`
- `/Users/username/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

## Managing MCP Servers

### Adding a New External MCP Server

1. Using Make:
```bash
make add-mcp-server url=https://github.com/user/repo.git name=server-name
```

2. Manual process:
```bash
# Add the submodule
git submodule add https://github.com/user/repo.git server-name

# Update configuration
vim cline_mcp_settings.template.json  # Add server configuration
vim .env.example                      # Add required environment variables

# Generate new settings
make generate-settings
```

### Updating External Servers

1. Update all submodules:
```bash
git submodule update --remote --merge
```

2. Update specific server:
```bash
cd server-name
git checkout main
git pull
cd ..
git add server-name
git commit -m "Update server-name to latest version"
```

### Creating a New Local MCP Server

1. Create the server directory:
```bash
mkdir new-server
cd new-server
```

2. Initialize with required files:
- `pyproject.toml` or `package.json`
- Source code directory
- Tests directory
- README.md

3. Add to configuration:
- Update `cline_mcp_settings.template.json`
- Add any required environment variables to `.env.example`
- Run `make generate-settings`

## Development Guidelines

See [.clinerules](.clinerules) for detailed development guidelines, including:
- MCP server design principles
- Configuration management
- Tool and resource design
- Error handling
- Testing requirements
- Security practices

## Security

### Sensitive Data Management

- Never commit `.env` files
- Use environment variables for all sensitive data
- Keep API keys and tokens out of code and logs
- Use the backup system for settings files

### Backup Management

Settings backups are stored in `backups/` directory:
- Automatically created when using `make backup-settings`
- Named with timestamps for easy reference
- Not committed to Git (except .gitkeep)

## Make Commands

```bash
make help              # Show available commands
make setup             # Initial setup
make generate-settings # Generate MCP settings
make backup-settings   # Backup current settings
make validate         # Validate environment and settings
make check-env        # Check environment variables
make install-deps     # Install dependencies
```

## Contributing

1. For external servers (submodules):
   - Submit changes to their respective repositories
   - Update submodule references in this repository

2. For local servers:
   - Follow the [.clinerules](.clinerules) guidelines
   - Include tests for new features
   - Update documentation as needed

## License

- External MCP servers maintain their own licenses
- Local MCP servers are licensed under this repository's license