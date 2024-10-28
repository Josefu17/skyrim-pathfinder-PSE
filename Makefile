build:
	cd ./docker/
	docker build -t registry.code.fbi.h-da.de/bpse-wise2425/group2/test-application:latest
	cd ..
push:
	cd ./docker/
	docker push registry.code.fbi.h-da.de/bpsewise2425/group2/test-application:latest
	cd ..
run:
	cd ./docker/
	docker-compose up -d
	cd ..
