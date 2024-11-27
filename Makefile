.PHONY: install remove build push start login stop nav-enter nav-test restart update connect-to-database

# Dependency management
install:
	pip install -r requirements.txt
	@echo "Dependencies installed."

remove:
	pip uninstall -y -r requirements.txt
	@echo "Dependencies removed."

# Docker management
build:
	docker build -t registry.code.fbi.h-da.de/bpse-wise2425/group2/web-frontend:latest .
	docker-compose build

push:
	docker push registry.code.fbi.h-da.de/bpse-wise2425/group2/web-frontend:latest
	docker push registry.code.fbi.h-da.de/bpse-wise2425/group2/navigation-service:latest
	docker push registry.code.fbi.h-da.de/bpse-wise2425/group2/web-backend:latest
	docker push registry.code.fbi.h-da.de/bpse-wise2425/group2/db-init:latest

start: build
	docker-compose up -d

login:
	docker login registry.code.fbi.h-da.de

stop:
	docker-compose down

restart: stop start


update: login build push

# Test management
test:
	python -m pytest ./backend/src/tests/

coverage-windows:
	python -m pytest --cov=backend/src --cov-report=html backend/src/tests/ --cov-config=setup.cfg && start htmlcov\index.html

# Navigation service management
nav-enter:
	docker exec -it group2-navigation-service-1 bash

nav-test:
	python -m pytest ./backend/src/tests/

# Database management
connect-to-database:
	docker exec -it group2-postgres-1 psql -U pg-2 -d navigation

lint:
	python -m pylint backend/src
