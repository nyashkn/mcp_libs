#!/bin/bash

# Check if envsubst is installed
if ! command -v envsubst &> /dev/null; then
    echo "Error: envsubst is not installed. Please install gettext package."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found. Please copy .env.example to .env and fill in your values."
    exit 1
fi

# Source the .env file
set -a
source .env
set +a

# Create the settings directories if they don't exist
mkdir -p "$(dirname "$VSCODE_SETTINGS_PATH_1")"
mkdir -p "$(dirname "$VSCODE_SETTINGS_PATH_2")"

# Generate the settings files using envsubst
envsubst < cline_mcp_settings.template.json > "$VSCODE_SETTINGS_PATH_1"
envsubst < cline_mcp_settings.template.json > "$VSCODE_SETTINGS_PATH_2"

# Set proper permissions
chmod 600 "$VSCODE_SETTINGS_PATH_1"
chmod 600 "$VSCODE_SETTINGS_PATH_2"

echo "MCP settings files generated successfully:"
echo "1. $VSCODE_SETTINGS_PATH_1"
echo "2. $VSCODE_SETTINGS_PATH_2"

# Verify the files exist and have content
if [ -s "$VSCODE_SETTINGS_PATH_1" ] && [ -s "$VSCODE_SETTINGS_PATH_2" ]; then
    echo "✅ Settings files created and populated successfully"
else
    echo "⚠️  Warning: One or both settings files may be empty"
    exit 1
fi