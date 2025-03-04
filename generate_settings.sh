#!/bin/bash

# Directory for backups
BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Function to show usage
usage() {
    echo "Usage: $0 [--backup|--validate]"
    echo
    echo "Options:"
    echo "  --backup    Create backup of existing settings before generating new ones"
    echo "  --validate  Only validate environment and settings without making changes"
    exit 1
}

# Function to validate environment variables
validate_env() {
    local missing_vars=()
    
    # Required environment variables
    required_vars=(
        "VENV_PATH"
        "PROJECT_PATH"
        "ASDF_PATH"
        "ASDF_DIR"
        "ASDF_DATA_DIR"
        "NODEJS_VERSION"
        "GITHUB_TOKEN"
        "PERPLEXITY_API_KEY"
        "TAVILY_API_KEY"
        "VSCODE_SETTINGS_PATH_1"
        "VSCODE_SETTINGS_PATH_2"
        "CLAUDE_DESKTOP_CONFIG_PATH"
    )
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -ne 0 ]; then
        echo "❌ Missing required environment variables:"
        printf '%s\n' "${missing_vars[@]}"
        return 1
    fi
    
    echo "✅ All required environment variables are set"
    return 0
}

# Function to backup existing settings
backup_settings() {
    mkdir -p "$BACKUP_DIR"
    
    for settings_path in "$VSCODE_SETTINGS_PATH_1" "$VSCODE_SETTINGS_PATH_2" "$CLAUDE_DESKTOP_CONFIG_PATH"; do
        if [ -f "$settings_path" ]; then
            backup_file="$BACKUP_DIR/$(basename "$settings_path")_$TIMESTAMP.bak"
            cp "$settings_path" "$backup_file"
            echo "✅ Backed up $settings_path to $backup_file"
        fi
    done
}

# Function to validate JSON files
validate_json() {
    local file=$1
    if ! jq empty "$file" 2>/dev/null; then
        echo "❌ Invalid JSON in $file"
        return 1
    fi
    return 0
}

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --backup) DO_BACKUP=1 ;;
        --validate) VALIDATE_ONLY=1 ;;
        --help) usage ;;
        *) echo "Unknown parameter: $1"; usage ;;
    esac
    shift
done

# Check if envsubst is installed
if ! command -v envsubst &> /dev/null; then
    echo "❌ Error: envsubst is not installed. Please install gettext package."
    exit 1
fi

# Check if jq is installed (for JSON validation)
if ! command -v jq &> /dev/null; then
    echo "❌ Error: jq is not installed. Please install jq package."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found. Please copy .env.example to .env and fill in your values."
    exit 1
fi

# Source the .env file
set -a
source .env
set +a

# Validate environment variables
if ! validate_env; then
    exit 1
fi

# Validate template JSON
if ! validate_json "cline_mcp_settings.template.json"; then
    exit 1
fi

# Exit if only validating
if [ -n "$VALIDATE_ONLY" ]; then
    echo "✅ All validations passed"
    exit 0
fi

# Backup existing settings if requested
if [ -n "$DO_BACKUP" ]; then
    backup_settings
fi

# Create the settings directories if they don't exist
mkdir -p "$(dirname "$VSCODE_SETTINGS_PATH_1")"
mkdir -p "$(dirname "$VSCODE_SETTINGS_PATH_2")"
mkdir -p "$(dirname "$CLAUDE_DESKTOP_CONFIG_PATH")"

# Generate the settings files using envsubst
echo "Generating settings files..."
envsubst < cline_mcp_settings.template.json > "$VSCODE_SETTINGS_PATH_1"
envsubst < cline_mcp_settings.template.json > "$VSCODE_SETTINGS_PATH_2"
envsubst < cline_mcp_settings.template.json > "$CLAUDE_DESKTOP_CONFIG_PATH"

# Set proper permissions
chmod 600 "$VSCODE_SETTINGS_PATH_1"
chmod 600 "$VSCODE_SETTINGS_PATH_2"
chmod 600 "$CLAUDE_DESKTOP_CONFIG_PATH"

echo "MCP settings files generated successfully:"
echo "1. $VSCODE_SETTINGS_PATH_1"
echo "2. $VSCODE_SETTINGS_PATH_2"
echo "3. $CLAUDE_DESKTOP_CONFIG_PATH"

# Verify the files exist and have content
if [ -s "$VSCODE_SETTINGS_PATH_1" ] && [ -s "$VSCODE_SETTINGS_PATH_2" ] && [ -s "$CLAUDE_DESKTOP_CONFIG_PATH" ]; then
    # Validate generated JSON files
    if validate_json "$VSCODE_SETTINGS_PATH_1" && validate_json "$VSCODE_SETTINGS_PATH_2" && validate_json "$CLAUDE_DESKTOP_CONFIG_PATH"; then
        echo "✅ Settings files created and validated successfully"
    else
        echo "⚠️  Warning: Generated files contain invalid JSON"
        exit 1
    fi
else
    echo "⚠️  Warning: One or more settings files may be empty"
    exit 1
fi
