.PHONY: help create-venv install remove build build-ci push start login stop restart update test coverage \
coverage-open-windows lint format nav-enter backend-enter connect-to-database pre-commit

.DEFAULT_GOAL := help
help:
	@echo "Hi! Please specify a target. Available targets:"
	@grep -E '^[a-zA-Z_-]+:' Makefile | grep -v '.PHONY' | awk '{print "  -", $$1}'

# Dependency management
create-venv:
	@if [ "$(OS)" = "Windows_NT" ]; then \
		py -m venv .venv; \
		echo "To activate: .venv\\Scripts\\activate"; \
	else \
		python3 -m venv .venv; \
		echo "To activate: source .venv/bin/activate"; \
	fi

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
test:
	python -m pytest ./backend/src/tests/

coverage:
	python -m pytest --cov=backend/src --cov-report=html:backend/coverage-reports/htmlcov backend/src/tests/ --cov-config=backend/setup.cfg --cov-report=xml:backend/coverage-reports/coverage.xml

coverage-open-windows: coverage
	 start backend\coverage-reports\htmlcov\index.html

# SonarQube management
sonar: coverage
	sonar-scanner

run-tests:
	@echo "TODO: Implement tests for frontend"

# Navigation service management
lint:
	python -m pylint --rcfile=backend/.pylintrc backend/src
	@make npm run=lint

format:
	python -m black --config backend/pyproject.toml backend/src
	@make npm run=format

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

pre-commit: test format lint coverage

# npm management
run ?= format

npm:
	@cd frontend && npm run $(run)

dev:
	@cd frontend && npm run dev

# Linux / Unix specific commands:
unix-coverage-open: coverage
	xdg-open backend/coverage-reports/htmlcov/index.html
