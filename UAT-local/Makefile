# Airflow Local Development Makefile

.PHONY: help init up down logs clean restart status

# Colors for output
GREEN=\033[0;32m
YELLOW=\033[1;33m
RED=\033[0;31m
NC=\033[0m # No Color

help: ## Show this help message
	@echo "$(GREEN)Available commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

init: ## Initialize Airflow (run this first time)
	@echo "$(GREEN)Initializing Airflow...$(NC)"
	@echo "AIRFLOW_UID=50000" > .env
	@echo "_AIRFLOW_WWW_USER_USERNAME=admin" >> .env
	@echo "_AIRFLOW_WWW_USER_PASSWORD=admin123" >> .env
	docker-compose up airflow-init
	@echo "$(GREEN)Airflow initialized successfully!$(NC)"

up: ## Start Airflow services
	@echo "$(GREEN)Starting Airflow services...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)Airflow is running at http://localhost:8080$(NC)"
	@echo "$(YELLOW)Username: admin$(NC)"
	@echo "$(YELLOW)Password: admin123$(NC)"

down: ## Stop Airflow services
	@echo "$(YELLOW)Stopping Airflow services...$(NC)"
	docker-compose down

logs: ## Show logs from all services
	docker-compose logs -f

logs-scheduler: ## Show scheduler logs
	docker-compose logs -f airflow-scheduler

logs-webserver: ## Show webserver logs  
	docker-compose logs -f airflow-webserver

status: ## Show status of all services
	docker-compose ps

restart: ## Restart all services
	@echo "$(YELLOW)Restarting Airflow services...$(NC)"
	docker-compose restart

clean: ## Stop and remove all containers, networks, volumes
	@echo "$(RED)This will remove all data! Press Ctrl+C to cancel...$(NC)"
	@sleep 5
	docker-compose down -v
	docker system prune -f

shell: ## Open shell in airflow-webserver container
	docker-compose exec airflow-webserver bash

cli: ## Run airflow CLI commands (usage: make cli CMD="dags list")
	docker-compose exec airflow-webserver airflow $(CMD)

test-dag: ## Test the quote_and_hello_dag
	docker-compose exec airflow-webserver airflow dags test quote_and_hello_dag

list-dags: ## List all available DAGs
	docker-compose exec airflow-webserver airflow dags list

# Development helpers
dev-setup: init up ## Complete development setup (init + start)
	@echo "$(GREEN)Development environment is ready!$(NC)"
	@echo "$(GREEN)Access Airflow at: http://localhost:8080$(NC)"

quick-start: ## Quick start (assumes already initialized)
	docker-compose up -d postgres airflow-webserver airflow-scheduler
	@echo "$(GREEN)Quick start complete! Access at http://localhost:8080$(NC)"

# Monitoring
monitor: ## Monitor system resources
	@echo "$(GREEN)Container Resource Usage:$(NC)"
	docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

check-health: ## Check health of all services
	@echo "$(GREEN)Service Health Status:$(NC)"
	@docker-compose ps --format table

# Backup and restore (if needed)
backup-db: ## Backup PostgreSQL database
	docker-compose exec postgres pg_dump -U airflow airflow > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)Database backed up successfully!$(NC)"


