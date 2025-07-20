# Development setup commands

.PHONY: setup install install-python install-node sync sync-all setup-mcp setup-mcp-auto

# === Initial Setup ===
setup: ## Run initial project setup wizard
	@echo "🚀 Starting project setup wizard..."
	@python make/tools/setup_project.py

# === Development Setup ===
install: ## Install all project dependencies (Python + Node.js)
	@echo "🔄 Installing Python dependencies..."
	uv sync --all-extras
	@echo "🔄 Installing Node.js dependencies..."
	npm install
	@echo "✅ All dependencies installed successfully!"
	@echo ""
	@echo "💡 Run 'make setup-mcp' to configure MCP servers for Claude Code"

install-python: ## Install Python dependencies only
	uv sync --all-extras

install-node: ## Install Node.js dependencies only
	npm install

sync: ## Sync Python dependencies with uv (update lock file)
	uv sync --all-extras --upgrade

sync-all: ## Sync all dependencies (Python + Node.js)
	@echo "🔄 Syncing Python dependencies..."
	uv sync --all-extras --upgrade
	@echo "🔄 Updating Node.js dependencies..."
	npm update
	@echo "✅ All dependencies synced!"

# === MCP Server Setup ===
setup-mcp: ## Display MCP server setup commands for Claude Code
	@echo "🤖 Generating MCP server setup commands..."
	@python make/tools/setup_mcp_servers.py

setup-mcp-auto: ## Automatically execute MCP server setup commands
	@echo "🤖 Setting up MCP servers for Claude Code..."
	@python make/tools/setup_mcp_servers.py --auto
	@echo ""
	@echo "✅ MCP servers configured! Please restart Claude Code to load them."