.PHONY: install remove build push start login stop nav-enter nav-test restart update connect-to-database

# Dependency management
install:
	pip install -r requirements.txt
	@echo "Dependencies installed."

remove:
	pip uninstall -y -r requirements.txt
	@echo "Dependencies removed."

build:
	docker build -t registry.code.fbi.h-da.de/bpse-wise2425/group2/test-application:latest .

push:
	docker push registry.code.fbi.h-da.de/bpse-wise2425/group2/test-application:latest

start:
	docker-compose up -d

login:
	docker login registry.code.fbi.h-da.de

stop:
	docker-compose down

nav-enter:
	docker exec -it group2-navigation-service-1 bash

nav-test:
	python -m pytest ./app/src/tests/

restart: stop start

update: login build push

connect-to-database:
	docker exec -it group2-postgres-1 psql -U pg-2 -d navigation
