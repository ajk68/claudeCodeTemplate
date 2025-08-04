# Development setup commands

# Path detection for shared vs complete mode
MAKE_TOOLS_DIR := $(if $(wildcard make/tools),make/tools,$(HOME)/ai_tools/make/tools)

.PHONY: setup install install-python install-node sync sync-all setup-mcp mcp-list mcp-install

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
	@echo "💡 MCP server commands:"
	@echo "   make mcp-list     - List available MCP servers"
	@echo "   make setup-mcp    - Install all MCP servers"
	@echo "   make mcp-install SERVERS=\"server1 server2\" - Install specific servers"

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
setup-mcp: ## Install all available MCP servers for Claude Code
	@echo "🤖 Installing all MCP servers for Claude Code..."
	@uv run python $(MAKE_TOOLS_DIR)/setup_mcp_servers.py --install
	@echo ""
	@echo "✅ MCP servers configured! Please restart Claude Code to load them."

mcp-list: ## List all available MCP servers and their status
	@uv run python $(MAKE_TOOLS_DIR)/setup_mcp_servers.py --list

mcp-install: ## Install specific MCP servers (usage: make mcp-install SERVERS="perplexity context7")
	@if [ -z "$(SERVERS)" ]; then \
		echo "❌ Please specify servers to install:"; \
		echo "   make mcp-install SERVERS=\"perplexity context7\""; \
		echo ""; \
		echo "Available servers:"; \
		uv run python $(MAKE_TOOLS_DIR)/setup_mcp_servers.py --list; \
	else \
		echo "🤖 Installing MCP servers: $(SERVERS)"; \
		uv run python $(MAKE_TOOLS_DIR)/setup_mcp_servers.py --install $(SERVERS); \
		echo ""; \
		echo "✅ MCP servers configured! Please restart Claude Code to load them."; \
	fi