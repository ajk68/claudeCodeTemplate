# Development setup commands

# Path detection for shared vs complete mode
MAKE_TOOLS_DIR := $(if $(wildcard make/tools),make/tools,$(HOME)/ai_tools/make/tools)

.PHONY: setup install install-python install-node sync sync-all setup-mcp

# === Initial Setup ===
setup: ## Run initial project setup wizard
	@echo "🚀 Starting project setup wizard..."
	@uv run python $(MAKE_TOOLS_DIR)/setup_project.py

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
setup-mcp: ## Automatically configure MCP servers for Claude Code
	@echo "🤖 Setting up MCP servers for Claude Code..."
	@uv run python $(MAKE_TOOLS_DIR)/setup_mcp_servers.py --auto
	@echo ""
	@echo "✅ MCP servers configured! Please restart Claude Code to load them."