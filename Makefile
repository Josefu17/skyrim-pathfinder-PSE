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
	@echo "Dependencies installed."

remove:
	pip uninstall -y -r backend/requirements.txt
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

start: build
	docker compose up -d


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
	python -m pytest --cov=backend/src --cov-report=html:backend/htmlcov backend/src/tests/ --cov-config=backend/setup.cfg

coverage-open-windows: coverage
	 start backend\htmlcov\index.html

run-tests:
# instrument the code for coverage
#	@python ./frontend/src/tests/instrument_code.py
# Execute the PowerShell script to start the server, open the tests, and stop the server after the tests
	@powershell -File ./scripts/run_tests.ps1

run-test-server:
	@python -m http.server 7777

# Navigation service management
lint:
	python -m pylint --rcfile=backend/.pylintrc backend/src

format:
	python -m black --config backend/pyproject.toml backend/src

# Services management
nav-enter:
	docker exec -it group2-navigation-service-1 bash

backend-enter:
	docker exec -it group2-web-backend-1 bash

# Database management
connect-to-database:
	docker exec -it group2-postgres-1 psql -U pg-2 -d navigation

pre-commit: test format lint


