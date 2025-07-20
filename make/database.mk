# Database-related commands

.PHONY: db-schema

# Database schema check (usage: make db-schema [TABLE=tablename])
db-schema: ## Check database schema
	@if [ ! -f .env ]; then \
		echo "❌ Error: .env file not found"; \
		exit 1; \
	fi; \
	DB_URL=$$(grep CARV_DB_URL .env | cut -d '=' -f2- | tr -d '"'); \
	if [ -z "$$DB_URL" ]; then \
		echo "❌ Error: CARV_DB_URL not found in .env"; \
		exit 1; \
	fi; \
	if [ -n "$(TABLE)" ]; then \
		psql "$$DB_URL" -c "\d $(TABLE)"; \
	else \
		psql "$$DB_URL" -c "\dt"; \
	fi