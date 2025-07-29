# Logging and Process Management Commands
# Attribution: Inspired by mitsuhiko's workflows and many others in the community

# Path detection for shared vs complete mode
MAKE_TOOLS_DIR := $(if $(wildcard make/tools),make/tools,$(HOME)/ai_tools/make/tools)
MAKE_DIR := $(if $(wildcard make),make,$(HOME)/ai_tools/make)

.PHONY: dev logs-start logs-watch logs-analyze logs-clean logs-tail

## Run all development processes with centralized logging
dev:
	@echo "🚀 Starting all development processes..."
	@if [ ! -f Procfile ]; then \
		echo "⚠️  No Procfile found. Creating from example..."; \
		cp Procfile.example Procfile; \
		echo "📝 Please edit Procfile to match your project setup"; \
	fi
	@$(MAKE_TOOLS_DIR)/shoreman.sh

## Start logging services in background
logs-start:
	@echo "🔄 Starting background logging..."
	@if [ ! -f Procfile ]; then \
		echo "❌ No Procfile found. Run 'make dev' first or create a Procfile"; \
		exit 1; \
	fi
	@nohup ./scripts/shoreman.sh > logs/combined/processes.log 2>&1 &
	@echo "✅ Logging started in background. PID saved to logs/shoreman.pid"
	@ps aux | grep shoreman | grep -v grep | awk '{print $$2}' > logs/shoreman.pid

## Watch combined logs in real-time
logs-watch:
	@echo "👀 Watching combined logs..."
	@tail -f logs/combined/*.log 2>/dev/null || echo "No logs found. Start services with 'make dev' first."

## Analyze logs with AI (last 1000 lines by default)
logs-analyze:
	@echo "🤖 Analyzing recent logs..."
	@if [ -z "$(PROMPT)" ]; then \
		tail -n 1000 logs/combined/*.log 2>/dev/null > /tmp/recent-logs.txt && $(MAKE) -f $(MAKE_DIR)/ai.mk ai-query FILE=/tmp/recent-logs.txt PROMPT="Analyze these logs for errors, warnings, and patterns. Summarize key issues."; \
	else \
		tail -n $(or $(LINES),1000) logs/combined/*.log 2>/dev/null > /tmp/recent-logs.txt && $(MAKE) -f $(MAKE_DIR)/ai.mk ai-query FILE=/tmp/recent-logs.txt PROMPT="$(PROMPT)"; \
	fi

## Clean all log files
logs-clean:
	@echo "🧹 Cleaning log files..."
	@find logs -name "*.log" -type f -delete
	@echo "✅ Log files cleaned"

## Tail specific log file
logs-tail:
	@if [ -z "$(FILE)" ]; then \
		echo "Usage: make logs-tail FILE=frontend|backend|combined/processes"; \
		exit 1; \
	fi
	@tail -f logs/$(FILE)*.log 2>/dev/null || echo "Log file not found: logs/$(FILE)*.log"

## Stop background logging processes
logs-stop:
	@echo "🛑 Stopping logging processes..."
	@if [ -f logs/shoreman.pid ]; then \
		kill $$(cat logs/shoreman.pid) 2>/dev/null && echo "✅ Stopped process $$(cat logs/shoreman.pid)" || echo "⚠️  Process already stopped"; \
		rm -f logs/shoreman.pid; \
	else \
		pkill -f shoreman.sh 2>/dev/null && echo "✅ Stopped shoreman processes" || echo "⚠️  No shoreman processes found"; \
	fi

## Show logging setup instructions
logs-help:
	@echo "📚 Centralized Logging Setup:"
	@echo ""
	@echo "1. Copy Procfile.example to Procfile and customize for your project"
	@echo "2. Run 'make dev' to start all services with unified logging"
	@echo "3. Logs are written to:"
	@echo "   - logs/frontend/ - Frontend console logs"
	@echo "   - logs/backend/ - Backend application logs"
	@echo "   - logs/combined/ - Combined process output"
	@echo ""
	@echo "Commands:"
	@echo "  make dev          - Start all services with logging"
	@echo "  make logs-watch   - Watch logs in real-time"
	@echo "  make logs-analyze - AI analysis of recent logs"
	@echo "  make logs-clean   - Remove all log files"
	@echo ""
	@echo "Frontend logging requires vite-console-forward-plugin setup in vite.config.ts"