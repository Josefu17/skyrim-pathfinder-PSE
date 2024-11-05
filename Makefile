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

restart:
	make stop
	make start

update:
	make login
	make build
	make push

connect-to-database:
	docker exec -it group2-postgres-1 psql -U pg-2 -d navigation
