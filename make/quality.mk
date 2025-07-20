# Code quality and testing commands

.PHONY: test test-coverage lint lint-fix lint-fix-unsafe format

# === Testing ===
test: ## Run all tests using uv
	uv run pytest tests/ -v

test-coverage: ## Run tests with coverage report
	uv run pytest tests/ --cov=. --cov-report=html --cov-report=term-missing -v

# === Code Quality ===
lint: ## Run linting checks
	uv run ruff check .

lint-fix: ## Automatically fix linting issues
	uv run ruff check --fix .

lint-fix-unsafe: ## Fix linting issues including unsafe fixes
	uv run ruff check --fix --unsafe-fixes .

format: ## Format code with ruff
	uv run ruff format .