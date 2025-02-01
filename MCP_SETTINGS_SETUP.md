# MCP Settings Management Guide

This guide explains how to securely manage MCP settings for all MCP servers while protecting sensitive information.

## File Structure

```
MCP/
├── cline_mcp_settings.template.json  # Template for all MCP servers
├── .env.example                      # Example environment variables
├── .env                              # Your actual environment variables (not committed)
└── generate_settings.sh              # Script to generate settings files
```

## Setup Instructions

1. Create your local environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your actual values:
```bash
# Edit paths to match your system
PROJECT_PATH=/your/actual/path/to/MCP
VENV_PATH=/your/actual/path/to/MCP
# Add your actual API tokens
GITHUB_TOKEN=your_actual_token
PERPLEXITY_API_KEY=your_actual_key
# etc...
```

3. Generate MCP settings files:
```bash
# Make the script executable
chmod +x generate_settings.sh
# Run the script
./generate_settings.sh
```

This will create the settings files in both required locations:
- /Users/username/Library/Application Support/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json
- /Users/username/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json

## Git Configuration

1. Add to `.gitignore`:
```
.env
**/cline_mcp_settings.json
```

2. Commit these files:
```
cline_mcp_settings.template.json
.env.example
generate_settings.sh
MCP_SETTINGS_SETUP.md
```

## Security Best Practices

1. Environment Variables:
   - Never commit .env files
   - Use different tokens for development/production
   - Regularly rotate API tokens
   - Keep .env file secure and local-only

2. Template Management:
   - Only update template when adding new servers or changing structure
   - Keep template up to date with all required variables
   - Document any new variables in .env.example

3. Settings Files:
   - Never commit actual settings files
   - Use generate_settings.sh to maintain consistency
   - Verify paths and permissions after generation

## Updating Settings

When you need to update MCP settings:

1. If adding new servers or changing structure:
   - Update cline_mcp_settings.template.json
   - Update .env.example with any new variables
   - Document changes in this file

2. If updating existing values:
   - Edit your local .env file
   - Run generate_settings.sh to update settings files

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| PROJECT_PATH | Path to MCP project root | /Users/username/Documents/Cline/MCP |
| VENV_PATH | Path to virtual environments | /Users/username/Documents/Cline/MCP |
| ASDF_PATH | Path to asdf installation | /Users/username/.asdf |
| PYENV_PATH | Path to pyenv python | /Users/username/.pyenv/shims |
| GITHUB_TOKEN | GitHub API token | ghp_xxxxxxxxxxxx |
| PERPLEXITY_API_KEY | Perplexity API key | pplx-xxxxxxxxxx |
| TAVILY_API_KEY | Tavily API key | tvly-xxxxxxxxxx |

## Troubleshooting

1. Settings not loading:
   - Check file permissions on settings files
   - Verify paths in .env are correct
   - Ensure all required variables are set

2. Generation script issues:
   - Check execute permissions on script
   - Verify envsubst is installed
   - Check for syntax errors in template

3. Missing values:
   - Compare .env with .env.example
   - Check template for new variables
   - Verify variable names match exactly

## Support

For issues or questions:
1. Check this documentation first
2. Review your .env file
3. Verify template syntax
4. Check file permissions and paths