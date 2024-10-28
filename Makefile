build:
	docker build -t registry.code.fbi.h-da.de/bpse-wise2425/group2/test-application:latest .

push:
	docker push registry.code.fbi.h-da.de/bpse-wise2425/group2/test-application:latest

run:
	docker-compose up -d

login:
	docker login registry.code.fbi.h-da.de

update:
	make login
	make build
	make push