.PHONY: help install remove build build-ci push start login stop restart update test coverage \
coverage-open-windows lint format nav-enter backend-enter connect-to-database pre-commit

.DEFAULT_GOAL := help
help:
	@echo "Hi! Please specify a target."

install:
	pip install -r backend/requirements.txt
	cd frontend && npm ci
	@echo "Dependencies installed."

remove:
	pip uninstall -y -r backend/requirements.txt
	cd frontend && npm uninstall
	@echo "Dependencies removed."

# Docker management
build:
	docker build -t registry.code.fbi.h-da.de/bpse-wise2425/group2/web-frontend:latest .
	docker compose build

build-ci:
	docker build -t registry.code.fbi.h-da.de/bpse-wise2425/group2/web-frontend:latest .
	docker build -t registry.code.fbi.h-da.de/bpse-wise2425/group2/navigation-service:latest -f ./backend/src/navigation_service/Dockerfile .
	docker build -t registry.code.fbi.h-da.de/bpse-wise2425/group2/web-backend:latest -f ./backend/src/web_backend/Dockerfile .

push:
	docker push registry.code.fbi.h-da.de/bpse-wise2425/group2/web-frontend:latest
	docker push registry.code.fbi.h-da.de/bpse-wise2425/group2/navigation-service:latest
	docker push registry.code.fbi.h-da.de/bpse-wise2425/group2/web-backend:latest

start:build start-frontend
	docker compose up -d
	make dev

start-frontend:
	docker build -t web-frontend:latest .
	docker rm -f web-frontend && docker run -p 4242:80 --name web-frontend -d web-frontend:latest

login:
	docker login registry.code.fbi.h-da.de

stop:
	docker compose down

restart: stop start


update: login build push

# Test management
test-backend:
	python -m pytest ./backend/src/tests/
test-frontend: # TODO
test: test-backend test-frontend

coverage:
	python -m pytest --cov=backend/src --cov-report=html:backend/coverage-reports/htmlcov backend/src/tests/ --cov-config=backend/setup.cfg --cov-report=xml:backend/coverage-reports/coverage.xml

coverage-open-windows: coverage
	 start backend\coverage-reports\htmlcov\index.html

# SonarQube management
sonar: coverage
	sonar-scanner

run-tests:
	@echo "TODO: Implement tests for frontend"

# Linting
lint-backend:
	python -m pylint --rcfile=backend/.pylintrc backend/src
lint-frontend:
	@make npm run=lint
lint: lint-backend lint-frontend

# Formatting
format-backend:
	python -m black --config backend/pyproject.toml backend/src
format-frontend:
	@make npm run=format
format: format-backend format-frontend

# Pre commit
pre-commit-backend: test-backend format-backend lint-backend
pre-commit-frontend: test-frontend format-frontend lint-frontend
pre-commit: pre-commit-backend pre-commit-frontend

# Services management
nav-enter:
	docker exec -it group2-navigation-service-1 bash

backend-enter:
	docker exec -it group2-web-backend-1 bash

# Database management
migrate:
	alembic -c backend/alembic.ini upgrade head

connect-to-database:
	docker exec -it group2-postgres-1 psql -U pg-2 -d pg-2


# npm management
run ?= format

npm:
	@cd frontend && npm run $(run)

dev:
	@cd frontend && npm run dev

# Linux / Unix specific commands:
unix-coverage-open: coverage
	xdg-open backend/coverage-reports/htmlcov/index.html
