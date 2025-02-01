# MCP Server Collection Management

.PHONY: help setup generate-settings backup-settings validate check-env install-deps

help:
	@echo "MCP Server Collection Management Commands:"
	@echo "make setup              - Initial setup (clone submodules, create env)"
	@echo "make generate-settings  - Generate MCP settings files"
	@echo "make backup-settings    - Backup current settings"
	@echo "make validate          - Validate environment and settings"
	@echo "make check-env         - Check environment variables"
	@echo "make install-deps      - Install dependencies (envsubst, etc.)"

setup: install-deps
	git submodule update --init --recursive
	cp .env.example .env
	@echo "⚠️  Please edit .env with your values"
	@echo "Then run: make generate-settings"

generate-settings: check-env validate
	./generate_settings.sh

backup-settings:
	./generate_settings.sh --backup

validate:
	./generate_settings.sh --validate

check-env:
	@if [ ! -f .env ]; then \
		echo "❌ .env file not found"; \
		exit 1; \
	fi
	@echo "✅ .env file exists"

install-deps:
	@if ! command -v envsubst &> /dev/null; then \
		echo "Installing gettext for envsubst..."; \
		if [ "$(uname)" = "Darwin" ]; then \
			brew install gettext; \
		elif [ -f /etc/debian_version ]; then \
			sudo apt-get update && sudo apt-get install -y gettext; \
		elif [ -f /etc/redhat-release ]; then \
			sudo yum install -y gettext; \
		else \
			echo "❌ Please install gettext package manually"; \
			exit 1; \
		fi \
	fi
	@echo "✅ Dependencies installed"

# Add new MCP server as submodule
add-mcp-server:
	@if [ -z "$(url)" ]; then \
		echo "❌ Please provide repository URL:"; \
		echo "make add-mcp-server url=https://github.com/user/repo.git"; \
		exit 1; \
	fi
	@if [ -z "$(name)" ]; then \
		name=$$(basename "$(url)" .git); \
	fi
	git submodule add $(url) $(name)
	@echo "✅ Added $(name) as submodule"
	@echo "Don't forget to:"
	@echo "1. Update cline_mcp_settings.template.json"
	@echo "2. Add any required environment variables to .env.example"
	@echo "3. Run make generate-settings"