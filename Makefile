.PHONY: help setup test deploy-infra deploy-functions run-app clean

help: ## Show this help message
	@echo "Coffeeverse - Azure ETL Pipeline"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Install dependencies and setup environment
	@echo "Setting up Coffeeverse..."
	python -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt
	. venv/bin/activate && pip install -r src/pipelines/requirements.txt
	@echo "✅ Setup complete. Activate with: source venv/bin/activate"

test: ## Run all tests
	@echo "Running tests..."
	. venv/bin/activate && python -m pytest tests/ -v
	@echo "✅ Tests passed"

test-unit: ## Run unit tests only
	@echo "Running unit tests..."
	. venv/bin/activate && python -m pytest tests/unit/ -v

test-integration: ## Run integration tests only
	@echo "Running integration tests..."
	. venv/bin/activate && python -m pytest tests/integration/ -v

lint: ## Run code linting
	@echo "Linting code..."
	. venv/bin/activate && flake8 src/ --max-line-length=120
	. venv/bin/activate && black src/ --check
	@echo "✅ Linting passed"

format: ## Format code with black
	@echo "Formatting code..."
	. venv/bin/activate && black src/
	@echo "✅ Code formatted"

deploy-infra: ## Deploy Azure infrastructure (requires Azure CLI)
	@echo "Deploying Azure infrastructure..."
	cd infrastructure/scripts && chmod +x deploy.sh && ./deploy.sh
	@echo "✅ Infrastructure deployed"

deploy-functions: ## Deploy Azure Functions
	@echo "Deploying Azure Functions..."
	cd src/pipelines && func azure functionapp publish $(FUNCTION_APP_NAME)
	@echo "✅ Functions deployed"

run-app: ## Run Streamlit app locally
	@echo "Starting Streamlit app..."
	. venv/bin/activate && streamlit run src/app/streamlit_app.py

run-functions: ## Run Azure Functions locally
	@echo "Starting Azure Functions locally..."
	cd src/pipelines && func start

dbt-run: ## Run dbt models
	@echo "Running dbt models..."
	cd dbt && dbt run --profiles-dir .
	@echo "✅ dbt models executed"

dbt-test: ## Run dbt tests
	@echo "Running dbt tests..."
	cd dbt && dbt test --profiles-dir .
	@echo "✅ dbt tests passed"

docker-build: ## Build Docker image
	@echo "Building Docker image..."
	docker build -f docker/Dockerfile -t coffeeverse:latest .
	@echo "✅ Docker image built"

docker-run: ## Run Docker container
	@echo "Running Docker container..."
	docker-compose -f docker/docker-compose.yml up
	@echo "✅ Container running"

clean: ## Clean up generated files
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf dbt/target dbt/logs
	@echo "✅ Cleanup complete"

destroy: ## Destroy all Azure resources (WARNING: destructive)
	@echo "⚠️  WARNING: This will delete all Azure resources"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		cd infrastructure/scripts && chmod +x destroy.sh && ./destroy.sh; \
		echo "✅ Resources destroyed"; \
	else \
		echo "❌ Cancelled"; \
	fi

logs-functions: ## Tail Azure Functions logs
	@echo "Tailing function logs..."
	az functionapp logs tail --name $(FUNCTION_APP_NAME) --resource-group $(RESOURCE_GROUP)

status: ## Check deployment status
	@echo "Checking deployment status..."
	@echo "Function App:"
	@az functionapp show --name $(FUNCTION_APP_NAME) --resource-group $(RESOURCE_GROUP) --query "state" -o tsv 2>/dev/null || echo "Not deployed"
	@echo "Cosmos DB:"
	@az cosmosdb show --name $(COSMOS_ACCOUNT) --resource-group $(RESOURCE_GROUP) --query "documentEndpoint" -o tsv 2>/dev/null || echo "Not deployed"
	@echo "Storage Account:"
	@az storage account show --name $(STORAGE_ACCOUNT) --resource-group $(RESOURCE_GROUP) --query "primaryEndpoints.blob" -o tsv 2>/dev/null || echo "Not deployed"

docs: ## Open documentation
	@echo "Opening documentation..."
	@open docs/ARCHITECTURE.md || xdg-open docs/ARCHITECTURE.md || start docs/ARCHITECTURE.md

.DEFAULT_GOAL := help
