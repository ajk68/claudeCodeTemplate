# Project-specific commands

.PHONY: run-pipeline clear-cache generate-summary

# === Project Commands ===
run-pipeline: ## Run the complete data pipeline
	uv run python 01_fetch_data.py && uv run python 02_build_features.py

clear-cache: ## Clear all caches (Redis and pickle files)
	uv run python clear_cache.py all

generate-summary: ## Generate executive summary
	uv run python generate_executive_summary.py