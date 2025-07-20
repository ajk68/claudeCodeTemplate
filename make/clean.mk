# Cleanup commands

.PHONY: clean clean-all

# === Cleanup ===
clean: ## Clean up generated files and caches
	@echo "🧹 Cleaning Python caches..."
	rm -rf .pytest_cache
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf __pycache__/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	@echo "🧹 Cleaning Node.js caches..."
	rm -rf node_modules/.cache
	@echo "🧹 Cleaning temporary files..."
	rm -f /tmp/context-*.txt /tmp/codebase-context-*.txt /tmp/tail-excerpt.txt
	@echo "✅ Cleanup completed!"

clean-all: ## Clean everything including node_modules
	@echo "🧹 Cleaning all caches and dependencies..."
	rm -rf .pytest_cache
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf __pycache__/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	rm -rf node_modules/
	rm -f /tmp/context-*.txt /tmp/codebase-context-*.txt /tmp/tail-excerpt.txt
	@echo "✅ Deep cleanup completed!"