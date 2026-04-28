.PHONY: install venv activate run test

venv: ## Create virtual environment
	python3 -m venv .venv

install: ## Install dependencies
	pip install -e .

run: ## Run the bot
	python3 src/bot/main.py

test: ## Run tests
	pytest tests/ -v
