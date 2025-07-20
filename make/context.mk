# Codebase context generation commands

.PHONY: generate-context-full generate-context-code generate-context-python generate-context-small generate-context-from-files claude-context

# === Codebase Context Generation ===
generate-context-full: ## Generate complete codebase context (everything)
	@echo "📦 Generating complete codebase context..."
	@git ls-files | repomix --stdin -o /tmp/codebase-context-full.txt
	@echo "✅ Complete context saved to: /tmp/codebase-context-full.txt"

generate-context-code: ## Generate code-only context (excludes docs and tests)
	@echo "📦 Generating code-only context..."
	@git ls-files | grep -v '^tests/' | grep -v '^docs/' | grep -v '\.md$$' | grep -v '\.txt$$' | repomix --stdin -o /tmp/codebase-context-code.txt
	@echo "✅ Code-only context saved to: /tmp/codebase-context-code.txt"

generate-context-python: ## Generate Python-only context (Python files, no tests/docs)
	@echo "📦 Generating Python-only context..."
	@git ls-files | grep '\.py$$' | grep -v '^tests/' | grep -v '^docs/' | repomix --stdin -o /tmp/codebase-context-python.txt
	@echo "✅ Python-only context saved to: /tmp/codebase-context-python.txt"

generate-context-small: ## Generate small compressed context (core code only, compressed)
	@echo "📦 Generating small compressed context..."
	@git ls-files | grep -v '^tests/' | grep -v '^docs/' | grep -v '\.md$$' | grep -v '\.txt$$' | repomix --stdin --compress -o /tmp/codebase-context-small.txt
	@echo "✅ Small compressed context saved to: /tmp/codebase-context-small.txt"

generate-context-from-files: ## Create context from specific files
	@if [ -z "$(FILES)" ]; then \
		echo "❌ Error: FILES parameter required"; \
		echo "Usage: make generate-context-from-files FILES=\"file1.py file2.py\""; \
		echo "Example: make generate-context-from-files FILES=\"api.py models.py\""; \
		exit 1; \
	fi; \
	echo "$(FILES)" | tr ' ' '\n' | repomix --stdin -o /tmp/codebase-context-files.txt; \
	echo "✅ Context saved to: /tmp/codebase-context-files.txt"

claude-context: ## Generate Claude setup context for configuration/debugging
	@echo "📦 Generating Claude setup context..."
	@# Generate user-level Claude context
	@if [ -d ~/.claude ]; then \
		echo "🏠 Creating user-level Claude context..."; \
		cd ~/.claude && repomix --include "CLAUDE.md,hooks/**,settings.json" --top-files-len 10 -o /tmp/context-claude-user.txt . || echo "⚠️  Failed to create user context"; \
	else \
		echo "⚠️  No user ~/.claude directory found"; \
		echo "# No user-level Claude configuration found" > /tmp/context-claude-user.txt; \
	fi
	@# Generate project-level Claude context  
	@echo "📁 Creating project-level Claude context..."
	@repomix --include ".claude/**,Makefile,make/**,CLAUDE.md" --top-files-len 15 -o /tmp/context-claude-project.txt .
	@# Combine both contexts into one file
	@echo "🔗 Combining contexts..."
	@echo "# User Level Claude Setup" > /tmp/context-claude-combined.txt
	@echo "" >> /tmp/context-claude-combined.txt
	@cat /tmp/context-claude-user.txt >> /tmp/context-claude-combined.txt
	@echo "" >> /tmp/context-claude-combined.txt
	@echo "" >> /tmp/context-claude-combined.txt
	@echo "# Project Level Claude Setup" >> /tmp/context-claude-combined.txt
	@echo "" >> /tmp/context-claude-combined.txt
	@cat /tmp/context-claude-project.txt >> /tmp/context-claude-combined.txt
	@# Clean up temporary files
	@rm /tmp/context-claude-user.txt /tmp/context-claude-project.txt
	@echo "✅ Combined Claude context saved to: /tmp/context-claude-combined.txt"