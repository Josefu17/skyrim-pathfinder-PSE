build:
	docker build -t registry.code.fbi.h-da.de/bpse-wise2425/group2/test-application:latest
push:
	docker push registry.code.fbi.h-da.de/bpsewise2425/group2/test-application:latest
run:
	docker-compose up -d
