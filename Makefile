.PHONY: help install pull update installLint lint baseline freeze deprecations clean compile

baselinefile = .baseline.json

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Install all deps
	pip install -r requirements.txt
	npm install

pull:
	git pull

update: pull install ## Update the installed deps
	npm audit fix

installLint: ## Install the linting deps
	pip install autoflake autopep8 isort flake8 flake8-django bandit eradicate

lint: .baseline.json ## Format, sort imports and lint
	autoflake --expand-star-imports --exclude "migrations" --exclude "node_modules" -i -r --remove-unused-variables --remove-all-unused-imports .
	autopep8 -a -a -a --exclude "migrations,node_modules" --in-place --recursive .
	isort "." --skip "stef/wsgi.py" --skip-glob "**/migrations/*" --skip-glob "*/node_modules/*"
	flake8 --exclude migrations,node_modules .
	bandit -x "./node_modules" -b $(baselinefile) -r .
	eradicate -r --in-place .

.baseline.json:
	touch .baseline.json

baseline: ## Write a baseline file for bandit security linter
	bandit -x "./node_modules" -f json -o $(baselinefile) -r . || true

freeze: ## Update requirements
	pip freeze | grep -v pkg-resources==0.0.0 > requirements.txt

deprecations: ## Run tests with deprecations excluding 3rd party packages
	python -Wd manage.py check 2>&1 #| grep -A 1 -v site-packages

clean: ## Clean all pyc files
	find . -name *.pyc -exec rm -f {} \;

compile: ## Compile static assets
	grunt compile

.DEFAULT_GOAL := help
