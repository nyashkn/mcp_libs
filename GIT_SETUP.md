# Git Repository Structure

This repository uses Git submodules to manage multiple MCP servers. This allows us to:
- Track specific versions of each MCP server
- Update servers independently
- Maintain our own configuration while keeping upstream changes separate

## Initial Setup

1. Initialize the parent repository:
```bash
# Initialize the main repository
git init
git add .gitignore .env.example cline_mcp_settings.template.json generate_settings.sh MCP_SETTINGS_SETUP.md GIT_SETUP.md
git commit -m "Initial commit: MCP management setup"
```

2. Add each MCP server as a submodule:
```bash
# Add each repository as a submodule
git submodule add https://github.com/adhikasp/mcp-git-ingest.git mcp-git-ingest
git submodule add [repository-url] mcp-pdf
git submodule add [repository-url] mcp-postgres
git submodule add [repository-url] mcp-server-github
git submodule add [repository-url] mcp-server-gitingest
git submodule add [repository-url] mcp-tavily
git submodule add [repository-url] perplexity-server
```

## Cloning the Repository

When cloning this repository, use one of these methods:

1. Clone with submodules in one command:
```bash
git clone --recurse-submodules [repository-url]
```

2. Or clone and initialize submodules separately:
```bash
git clone [repository-url]
git submodule init
git submodule update
```

## Updating Submodules

1. Update all submodules to their latest versions:
```bash
git submodule update --remote --merge
```

2. Update a specific submodule:
```bash
cd [submodule-directory]
git checkout main  # or master, depending on the default branch
git pull
cd ..
git add [submodule-directory]
git commit -m "Update [submodule-name] to latest version"
```

## Working with Submodules

1. Check submodule status:
```bash
git submodule status
```

2. Execute commands across all submodules:
```bash
git submodule foreach 'git status'
```

3. Switch to a specific version/tag in a submodule:
```bash
cd [submodule-directory]
git checkout [tag/commit]
cd ..
git add [submodule-directory]
git commit -m "Switch [submodule-name] to version [tag]"
```

## Best Practices

1. Always commit submodule changes:
```bash
# After updating a submodule
git add [submodule-directory]
git commit -m "Update [submodule-name] to [version/commit]"
```

2. Keep track of submodule versions:
- Document which versions of each MCP server are known to work together
- Test after updating submodules
- Consider creating tags for known-good combinations

3. Handling local changes:
- Avoid making direct changes in submodules
- If needed, fork the submodule repository and point to your fork
- Use the parent repository for configuration management

## Configuration Management

1. The parent repository manages:
- Environment configuration (.env.example)
- MCP settings template (cline_mcp_settings.template.json)
- Generation scripts (generate_settings.sh)
- Documentation (*.md files)

2. Each submodule maintains:
- Its own code and tests
- Submodule-specific documentation
- Submodule-specific configuration

## Troubleshooting

1. Submodule appears empty:
```bash
git submodule init
git submodule update
```

2. Submodule is in detached HEAD state:
```bash
cd [submodule-directory]
git checkout main
git pull
```

3. Conflicts during updates:
```bash
# Stash any local changes
git submodule foreach 'git stash'
# Update submodules
git submodule update --remote --merge
# Reapply changes if needed
git submodule foreach 'git stash pop'