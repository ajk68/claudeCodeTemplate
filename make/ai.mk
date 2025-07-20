# AI delegation and analysis commands

.PHONY: ai-query ai-analyze-project review-diff analyze-files analyze-file project-status code-search analyze-logs _tail-to-temp

# === AI Delegation ===
ai-query: ## Query AI with smart model selection based on content size
	@if [ -z "$(PROMPT)" ]; then \
		echo "❌ Error: PROMPT parameter required"; \
		echo "Usage: make ai-query PROMPT=\"your question\" [FILE=filename]"; \
		echo "Purpose: Ask AI about specific files or general questions"; \
		echo "Example: make ai-query PROMPT=\"Explain this code\" FILE=\"script.py\""; \
		echo "Example: make ai-query PROMPT=\"What is a good pattern for error handling?\""; \
		exit 1; \
	fi; \
	if [ -n "$(FILE)" ]; then \
		if [ ! -f "$(FILE)" ]; then \
			echo "❌ Error: File '$(FILE)' not found"; \
			echo "Usage: make ai-query PROMPT=\"your question\" FILE=\"existing_file.py\""; \
			echo "Available files: $$(find . -name '*.py' -not -path './.*' | head -5 | xargs)..."; \
			exit 1; \
		fi; \
		CONTENT_SIZE=$$(wc -c < "$(FILE)"); \
		PROMPT_SIZE=$$(echo "$(PROMPT)" | wc -c); \
		TOTAL_SIZE=$$((CONTENT_SIZE + PROMPT_SIZE)); \
		if [ $$TOTAL_SIZE -gt 70000 ]; then \
			echo "🤖 Using Gemini (large context: $$TOTAL_SIZE chars)"; \
			llm -m gemini-2.5-flash -a "$(FILE)" "$(PROMPT)"; \
		else \
			echo "🤖 Using Claude (small context: $$TOTAL_SIZE chars)"; \
			cat "$(FILE)" | claude -p "$(PROMPT)"; \
		fi; \
	else \
		PROMPT_SIZE=$$(echo "$(PROMPT)" | wc -c); \
		if [ $$PROMPT_SIZE -gt 70000 ]; then \
			echo "❌ Error: Prompt too large ($$PROMPT_SIZE chars) without file attachment"; \
			echo "Consider using ai-analyze-project for codebase questions"; \
			echo "Example: make ai-analyze-project PROMPT=\"your question\" SCOPE=python"; \
			exit 1; \
		fi; \
		echo "🤖 Using Claude (prompt only: $$PROMPT_SIZE chars)"; \
		claude -p "$(PROMPT)"; \
	fi

ai-analyze-project: ## Analyze entire project with AI using codebase context
	@if [ -z "$(PROMPT)" ]; then \
		echo "❌ Error: PROMPT parameter required"; \
		echo "Usage: make ai-analyze-project PROMPT=\"your question\" [SCOPE=python]"; \
		echo "Purpose: Ask AI about entire codebase with full context"; \
		echo "SCOPE options: full, code, python, small (default: python)"; \
		echo "Example: make ai-analyze-project PROMPT=\"Find all TODO comments\" SCOPE=full"; \
		echo "Example: make ai-analyze-project PROMPT=\"Explain the architecture\""; \
		exit 1; \
	fi; \
	SCOPE_TYPE=$${SCOPE:-python}; \
	case $$SCOPE_TYPE in \
		full) CONTEXT_COMMAND="generate-context-full"; CONTEXT_FILE="/tmp/codebase-context-full.txt" ;; \
		code) CONTEXT_COMMAND="generate-context-code"; CONTEXT_FILE="/tmp/codebase-context-code.txt" ;; \
		python) CONTEXT_COMMAND="generate-context-python"; CONTEXT_FILE="/tmp/codebase-context-python.txt" ;; \
		small) CONTEXT_COMMAND="generate-context-small"; CONTEXT_FILE="/tmp/codebase-context-small.txt" ;; \
		*) echo "❌ Error: Invalid SCOPE '$$SCOPE_TYPE'. Use: full, code, python, or small"; \
			echo "Example: make ai-analyze-project PROMPT=\"your question\" SCOPE=code"; \
			exit 1 ;; \
	esac; \
	echo "📦 Generating $$SCOPE_TYPE codebase context..."; \
	make $$CONTEXT_COMMAND > /dev/null 2>&1; \
	if [ ! -f "$$CONTEXT_FILE" ]; then \
		echo "❌ Error: Failed to generate context file $$CONTEXT_FILE"; \
		echo "Try: make $$CONTEXT_COMMAND"; \
		exit 1; \
	fi; \
	make ai-query FILE="$$CONTEXT_FILE" PROMPT="$(PROMPT)"

# Quick code review (usage: make review-diff)
review-diff: ## Review current git diff for issues
	@git diff | claude -p "Review these changes for critical issues that would break production. Be pragmatic - we're a startup, not NASA."

analyze-files: ## Get architectural analysis and guidance for specific files
	@if [ -z "$(FILES)" ]; then \
		echo "❌ Error: FILES parameter required"; \
		echo "Usage: make analyze-files FILES=\"file1.py file2.py\""; \
		echo "Purpose: Get architectural analysis of specific files"; \
		echo "Example: make analyze-files FILES=\"api.py models.py\""; \
		echo "Example: make analyze-files FILES=\"src/main.py\""; \
		exit 1; \
	fi; \
	echo "🔍 Analyzing files: $(FILES)"; \
	for file in $(FILES); do \
		if [ -f "$$file" ]; then \
			echo "🏗️ Analyzing $$file..."; \
			make ai-query FILE="$$file" PROMPT="Provide architectural guidance for this file. Focus on: 1) Design patterns used, 2) Code organization and structure, 3) Potential issues or improvements, 4) Dependencies and coupling, 5) Overall code quality and maintainability."; \
		else \
			echo "❌ File not found: '$$file'"; \
			echo "Available Python files: $$(find . -name '*.py' -not -path './.*' | head -5 | xargs)..."; \
		fi; \
	done

# File analysis
analyze-file: ## Analyze a single file with AI
	@if [ -z "$(FILE)" ]; then \
		echo "❌ Error: FILE parameter required"; \
		echo "Usage: make analyze-file FILE=\"filename.py\""; \
		echo "Example: make analyze-file FILE=\"api.py\""; \
		exit 1; \
	fi; \
	make ai-query FILE="$(FILE)" PROMPT="Provide architectural guidance for this file. Focus on: 1) Design patterns used, 2) Code organization and structure, 3) Potential issues or improvements, 4) Dependencies and coupling, 5) Overall code quality and maintainability."

project-status: ## Get current project status and recent work summary
	@echo "🔍 Analyzing project state..."
	@( \
		echo "=== GIT STATUS ===" && git status --porcelain; \
		echo -e "\n=== GIT DIFF STATS ===" && git diff --stat; \
		echo -e "\n=== RECENT COMMITS ===" && git log --oneline -5; \
		echo -e "\n=== CURRENT BRANCH ===" && git branch --show-current; \
		echo -e "\n=== TRACKED FILES ===" && git ls-files | wc -l && echo "files tracked"; \
		echo -e "\n=== ENV FILE CHECK ===" && if [ -f '.env' ]; then echo '.env file found.'; else echo '⚠️ Warning: .env file not found.'; fi; \
	) | claude --model sonnet -p "Analyze this project status output and provide a clear, actionable summary: \
\
## 📊 Current Status \
- **Branch**: [name] \
- **Working Tree**: [clean/X uncommitted changes - list key files] \
- **Staged Changes**: [if any] \
\
## 🗝️ .env Environment Variables \
[Status of .env file] \
\
## 🕐 Recent Work (last 5 commits) \
[Summarize the theme/progress from commits] \
\
## 🚧 Work in Progress \
[What appears to be partially done based on uncommitted changes] \
\
Keep it concise and actionable."

code-search: ## Fast code search with ripgrep
	@if [ -z "$(PATTERN)" ]; then \
		echo "❌ Error: PATTERN parameter required"; \
		echo "Usage: make code-search PATTERN=\"your pattern\" [FILETYPE=py]"; \
		echo "Purpose: Fast code search across the entire codebase"; \
		echo "Example: make code-search PATTERN=\"TODO\" FILETYPE=py"; \
		echo "Example: make code-search PATTERN=\"class.*Model\""; \
		exit 1; \
	fi; \
	if echo "$(PATTERN)" | grep -q "[;&|]"; then \
		echo "❌ Error: Invalid characters in pattern"; \
		echo "Pattern cannot contain shell metacharacters: ; & |"; \
		exit 1; \
	fi; \
	TYPE_FLAG=""; \
	if [ -n "$(FILETYPE)" ]; then \
		TYPE_FLAG="--type $(FILETYPE)"; \
	fi; \
	echo "🔍 Searching for pattern: $(PATTERN)"; \
	rg "$(PATTERN)" $$TYPE_FLAG -C 3

# Internal helper for extracting log tail (not for direct use)
_tail-to-temp:
	@tail -n $(LINES) $(FILE) > /tmp/tail-excerpt.txt

analyze-logs: ## AI-friendly log analysis with debugging insights (default: last 100 lines of logs/error.log)
	@# Set defaults for AI agents
	@LOG_FILE=$${LOG_FILE:-logs/error.log}; \
	LOG_LINES=$${LINES:-100}; \
	if [ ! -f "$$LOG_FILE" ]; then \
		echo "⚠️  Log file '$$LOG_FILE' not found"; \
		echo ""; \
		echo "🔍 Searching for available log files..."; \
		FOUND_LOGS=$$(find . -name "*.log" -type f 2>/dev/null | grep -v node_modules | head -10); \
		if [ -n "$$FOUND_LOGS" ]; then \
			echo "Available log files:"; \
			echo "$$FOUND_LOGS" | sed 's/^/  /'; \
			echo ""; \
			echo "💡 Suggestion: Try one of these:"; \
			FIRST_LOG=$$(echo "$$FOUND_LOGS" | head -1); \
			echo "  make analyze-logs LOG_FILE=$$FIRST_LOG"; \
		else \
			echo "No .log files found in the project."; \
			echo ""; \
			echo "💡 Common log locations:"; \
			echo "  - logs/error.log"; \
			echo "  - logs/app.log"; \
			echo "  - application.log"; \
		fi; \
		echo ""; \
		echo "Usage: make analyze-logs [LOG_FILE=path/to/log] [LINES=100]"; \
		exit 0; \
	fi; \
	echo "📋 Extracting last $$LOG_LINES lines from $$LOG_FILE..."; \
	if ! $(MAKE) _tail-to-temp FILE="$$LOG_FILE" LINES="$$LOG_LINES" 2>/dev/null; then \
		echo "❌ Failed to extract log lines. Check file permissions."; \
		exit 1; \
	fi; \
	if [ ! -s "/tmp/tail-excerpt.txt" ]; then \
		echo "⚠️  Log file appears to be empty or extraction failed."; \
		echo "Checking file size..."; \
		ls -lh "$$LOG_FILE" 2>/dev/null || echo "Cannot access file stats."; \
		exit 0; \
	fi; \
	echo "🤖 Analyzing log entries for debugging insights..."; \
	$(MAKE) ai-query FILE="/tmp/tail-excerpt.txt" PROMPT="Analyze these log entries for debugging purposes. Provide: \
\
1. **Recent Activity Summary**: What operations/requests were successful? List the last few successful operations with timestamps if available. \
\
2. **Error Analysis**: \
   - Critical errors or exceptions (with timestamps and frequency) \
   - Error patterns or recurring issues \
   - Root cause hints based on error sequences \
\
3. **System Health Indicators**: \
   - Performance metrics (response times, throughput) \
   - Resource usage warnings (memory, CPU, connections) \
   - Queue depths or backlogs \
\
4. **Debugging Clues**: \
   - Correlation between events (what happened before errors?) \
   - Unusual patterns or anomalies \
   - Missing expected log entries \
\
5. **Actionable Next Steps**: \
   - Immediate debugging commands to run \
   - What to investigate next \
   - Which logs or metrics to check \
\
Keep the response concise but include specific timestamps and values that would help with debugging."