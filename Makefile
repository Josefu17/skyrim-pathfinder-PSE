.PHONY: help install remove build build-ci push start stop restart test-backend test-frontend test \
 coverage coverage-backend coverage-frontend coverage-open lint lint-backend lint-frontend \
 format format format-backend format-frontend pre-commit pre-commit-backend pre-commit-frontend \
 nav-enter backend-enter db-migrate db-connect db-seed db-clear npm dev \

.DEFAULT_GOAL := help
help:
	@echo "Hi! Please specify a target."

install:
	pip install -r backend/requirements.txt
	cd frontend && npm ci
	@echo "Dependencies installed."

remove:
	pip uninstall -y -r backend/requirements.txt
	@powershell -Command "Remove-Item -Path "./frontend/node_modules" -Recurse -Force"
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

start:build
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
test-frontend:
	@make npm run=test
test-frontend-startup:
	@make npm run=test-startup
test: test-backend test-frontend


# Coverage management
coverage: coverage-backend coverage-frontend

coverage-backend:
	python -m pytest --cov=backend/src --cov-report=html:backend/coverage-reports/htmlcov backend/src/tests/ --cov-config=backend/setup.cfg --cov-report=xml:backend/coverage-reports/coverage.xml

coverage-frontend:
	@make npm run=coverage

coverage-open-windows: coverage
	powershell -Command "Start-Process -FilePath 'backend\coverage-reports\htmlcov\index.html'"
	powershell -Command "Start-Process -FilePath 'frontend/coverage/index.html'"

coverage-open-unix: coverage
	xdg-open backend/coverage-reports/htmlcov/index.html
	xdg-open frontend/coverage/index.html

# SonarQube management
sonar: coverage
	sonar-scanner

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
pre-commit-backend: format-backend lint-backend coverage-backend
pre-commit-frontend: format-frontend lint-frontend coverage-frontend
pre-commit: pre-commit-backend pre-commit-frontend

# Services management
nav-enter:
	docker exec -it group2-navigation-service bash

backend-enter:
	docker exec -it group2-web-backend bash

# Database management
db-migrate:
	alembic -c backend/alembic.ini upgrade head

db-connect:
	docker exec -it group2-postgres psql -U pg-2 -d pg-2

db-seed:
	python -m backend.src.database.seed_db seed

db-clear:
	python -m backend.src.database.seed_db clear


# npm management
run ?= format

npm:
	@cd frontend && npm run $(run)

dev:
	@cd frontend && npm run dev
