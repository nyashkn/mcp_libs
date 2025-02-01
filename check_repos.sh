#!/bin/bash

# Function to check if a directory is a git repo and has submodules
check_repo() {
    local dir=$1
    echo "Checking $dir..."
    
    if [ -d "$dir/.git" ]; then
        echo "✓ Is a Git repository"
        
        # Check for submodules
        if [ -f "$dir/.gitmodules" ]; then
            echo "✓ Has submodules:"
            cat "$dir/.gitmodules"
        else
            echo "✗ No submodules"
        fi
        
        # Show remote URL
        echo "Remote URL:"
        (cd "$dir" && git remote -v)
        
        echo "-------------------"
    else
        echo "✗ Not a Git repository"
        echo "-------------------"
    fi
}

# Check each MCP directory
for dir in */; do
    check_repo "${dir%/}"
done