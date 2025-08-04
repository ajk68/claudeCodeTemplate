# Project-specific commands
# Add your project-specific make targets here

# Example:
# .PHONY: dev-server
# dev-server: ## Start development server
# 	uv run python manage.py runserver

# Example:
# .PHONY: migrate
# migrate: ## Run database migrations
# 	uv run python manage.py migrate

.PHONY: claude-code-documentation
claude-code-documentation: ## Download and combine all Claude Code documentation into a single markdown file
	@if [ -f /tmp/claude-code-complete-docs.md ]; then \
		echo "✅ Claude Code documentation already exists at: /tmp/claude-code-complete-docs.md"; \
		echo "   File size: $$(ls -lh /tmp/claude-code-complete-docs.md | awk '{print $$5}')"; \
		echo "   Total lines: $$(wc -l /tmp/claude-code-complete-docs.md | awk '{print $$1}')"; \
		echo ""; \
		echo "   To regenerate, first remove the existing file:"; \
		echo "   rm /tmp/claude-code-complete-docs.md"; \
	else \
		echo "Downloading Claude Code documentation..."; \
		docs="overview quickstart common-workflows sdk sub-agents hooks-guide github-actions mcp troubleshooting third-party-integrations amazon-bedrock google-vertex-ai corporate-proxy llm-gateway devcontainer setup iam security monitoring-usage costs analytics settings ide-integrations terminal-config memory cli-reference interactive-mode slash-commands hooks data-usage legal-and-compliance"; \
		for doc in $$docs; do \
			echo "Downloading $$doc.md..."; \
			curl -s "https://docs.anthropic.com/en/docs/claude-code/$$doc.md" -o "/tmp/$$doc.md"; \
		done; \
		echo "# Claude Code Complete Documentation" > /tmp/claude-code-complete-docs.md; \
		echo "" >> /tmp/claude-code-complete-docs.md; \
		echo "This document contains all Claude Code documentation pages combined into a single file." >> /tmp/claude-code-complete-docs.md; \
		echo "" >> /tmp/claude-code-complete-docs.md; \
		echo "Generated on: $$(date)" >> /tmp/claude-code-complete-docs.md; \
		echo "" >> /tmp/claude-code-complete-docs.md; \
		echo "## Table of Contents" >> /tmp/claude-code-complete-docs.md; \
		echo "" >> /tmp/claude-code-complete-docs.md; \
		echo "1. [Overview](#section-overview)" >> /tmp/claude-code-complete-docs.md; \
		echo "2. [Quickstart](#section-quickstart)" >> /tmp/claude-code-complete-docs.md; \
		echo "3. [Common Workflows](#section-common-workflows)" >> /tmp/claude-code-complete-docs.md; \
		echo "4. [Memory](#section-memory)" >> /tmp/claude-code-complete-docs.md; \
		echo "5. [SDK](#section-sdk)" >> /tmp/claude-code-complete-docs.md; \
		echo "6. [Sub-agents](#section-sub-agents)" >> /tmp/claude-code-complete-docs.md; \
		echo "7. [Hooks Guide](#section-hooks-guide)" >> /tmp/claude-code-complete-docs.md; \
		echo "8. [Hooks](#section-hooks)" >> /tmp/claude-code-complete-docs.md; \
		echo "9. [GitHub Actions](#section-github-actions)" >> /tmp/claude-code-complete-docs.md; \
		echo "10. [MCP](#section-mcp)" >> /tmp/claude-code-complete-docs.md; \
		echo "11. [IDE Integrations](#section-ide-integrations)" >> /tmp/claude-code-complete-docs.md; \
		echo "12. [Terminal Config](#section-terminal-config)" >> /tmp/claude-code-complete-docs.md; \
		echo "13. [CLI Reference](#section-cli-reference)" >> /tmp/claude-code-complete-docs.md; \
		echo "14. [Interactive Mode](#section-interactive-mode)" >> /tmp/claude-code-complete-docs.md; \
		echo "15. [Slash Commands](#section-slash-commands)" >> /tmp/claude-code-complete-docs.md; \
		echo "16. [Settings](#section-settings)" >> /tmp/claude-code-complete-docs.md; \
		echo "17. [Setup](#section-setup)" >> /tmp/claude-code-complete-docs.md; \
		echo "18. [Devcontainer](#section-devcontainer)" >> /tmp/claude-code-complete-docs.md; \
		echo "19. [Third Party Integrations](#section-third-party-integrations)" >> /tmp/claude-code-complete-docs.md; \
		echo "20. [Amazon Bedrock](#section-amazon-bedrock)" >> /tmp/claude-code-complete-docs.md; \
		echo "21. [Google Vertex AI](#section-google-vertex-ai)" >> /tmp/claude-code-complete-docs.md; \
		echo "22. [Corporate Proxy](#section-corporate-proxy)" >> /tmp/claude-code-complete-docs.md; \
		echo "23. [LLM Gateway](#section-llm-gateway)" >> /tmp/claude-code-complete-docs.md; \
		echo "24. [IAM](#section-iam)" >> /tmp/claude-code-complete-docs.md; \
		echo "25. [Security](#section-security)" >> /tmp/claude-code-complete-docs.md; \
		echo "26. [Monitoring Usage](#section-monitoring-usage)" >> /tmp/claude-code-complete-docs.md; \
		echo "27. [Costs](#section-costs)" >> /tmp/claude-code-complete-docs.md; \
		echo "28. [Analytics](#section-analytics)" >> /tmp/claude-code-complete-docs.md; \
		echo "29. [Data Usage](#section-data-usage)" >> /tmp/claude-code-complete-docs.md; \
		echo "30. [Legal and Compliance](#section-legal-and-compliance)" >> /tmp/claude-code-complete-docs.md; \
		echo "31. [Troubleshooting](#section-troubleshooting)" >> /tmp/claude-code-complete-docs.md; \
		echo "" >> /tmp/claude-code-complete-docs.md; \
		echo "---" >> /tmp/claude-code-complete-docs.md; \
		echo "" >> /tmp/claude-code-complete-docs.md; \
		ordered_docs="overview quickstart common-workflows memory sdk sub-agents hooks-guide hooks github-actions mcp ide-integrations terminal-config cli-reference interactive-mode slash-commands settings setup devcontainer third-party-integrations amazon-bedrock google-vertex-ai corporate-proxy llm-gateway iam security monitoring-usage costs analytics data-usage legal-and-compliance troubleshooting"; \
		for doc in $$ordered_docs; do \
			echo "" >> /tmp/claude-code-complete-docs.md; \
			echo "---" >> /tmp/claude-code-complete-docs.md; \
			echo "" >> /tmp/claude-code-complete-docs.md; \
			echo "# Section: $$doc" >> /tmp/claude-code-complete-docs.md; \
			echo "" >> /tmp/claude-code-complete-docs.md; \
			cat "/tmp/$$doc.md" >> /tmp/claude-code-complete-docs.md; \
		done; \
		rm -f /tmp/overview.md /tmp/quickstart.md /tmp/common-workflows.md /tmp/sdk.md /tmp/sub-agents.md /tmp/hooks-guide.md /tmp/github-actions.md /tmp/mcp.md /tmp/troubleshooting.md /tmp/third-party-integrations.md /tmp/amazon-bedrock.md /tmp/google-vertex-ai.md /tmp/corporate-proxy.md /tmp/llm-gateway.md /tmp/devcontainer.md /tmp/setup.md /tmp/iam.md /tmp/security.md /tmp/monitoring-usage.md /tmp/costs.md /tmp/analytics.md /tmp/settings.md /tmp/ide-integrations.md /tmp/terminal-config.md /tmp/memory.md /tmp/cli-reference.md /tmp/interactive-mode.md /tmp/slash-commands.md /tmp/hooks.md /tmp/data-usage.md /tmp/legal-and-compliance.md; \
		echo ""; \
		echo "✅ Claude Code documentation successfully compiled to: /tmp/claude-code-complete-docs.md"; \
		echo "   File size: $$(ls -lh /tmp/claude-code-complete-docs.md | awk '{print $$5}')"; \
		echo "   Total lines: $$(wc -l /tmp/claude-code-complete-docs.md | awk '{print $$1}')"; \
	fi