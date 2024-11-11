# Dokumentation der Gruppe 2

## Table of contents
- [Dokumentation der Gruppe 2](#dokumentation-der-gruppe-2)
  - [Table of contents](#table-of-contents)
  - [Gruppen-Konventionen](#gruppen-konventionen)
    - [Festgelegte Sprachen](#festgelegte-sprachen)
    - [Code Styling](#code-styling)
    - [Merge Request Definition of Done](#merge-request-definition-of-done)
  - [Server Erreichbarkeit](#server-erreichbarkeit)
    - [Map-Server](#map-server)
    - [Deployment-Server](#deployment-server)
    - [Postgres-Server](#postgres-server)
  - [Useful commands](#useful-commands)
- [Database Connection](#database-connection)
  - [On server:](#on-server)
    - [Secure database on server](#secure-database-on-server)
  - [On Local computer:](#on-local-computer)
    - [Insert dumpfile content into local database](#insert-dumpfile-content-into-local-database)
    - [Connect to local database](#connect-to-local-database)
- [Docker](#docker)
    - [Display docker images](#display-docker-images)
    - [Display running docker containers](#display-running-docker-containers)
  - [Docker on local computer](#docker-on-local-computer)
    - [Build docker image](#build-docker-image)
    - [Log into the docker registry](#log-into-the-docker-registry)
    - [Push the docker image](#push-the-docker-image)
  - [Docker on deployment server](#docker-on-deployment-server)
    - [Log into the docker registry](#log-into-the-docker-registry-1)
    - [Load docker image and start docker container](#load-docker-image-and-start-docker-container)
    - [Stop running docker container](#stop-running-docker-container)
    - [Remove docker image](#remove-docker-image)
  - [Update docker container (from local to server)](#update-docker-container-from-local-to-server)
      - [Command notes](#command-notes)
- [make](#make)
  - [Makefile Beispiel](#makefile-beispiel)
- [Stage 1 - Documentation](#stage-1---documentation)
  - [Project Management](#project-management)
  - [DevExp](#devexp)
    - [One Click Dependencies Installation / Deletion](#Installation-and-Removal-of-Dependencies)
    - [Debugger (debugpy)](#debugger-debugpy)
      - [Changes in `docker-compose.yml`](#changes-in-docker-composeyml)
        - [Setup for Vs Code](#setup-for-vs-code)
        - [Setup for pycharm](#setup-for-pycharm)
  - [CI/CD and Operation](#cicd-and-operation)
- [Todos for Stage 1](#todos-for-stage-1)
  - [Project Management](#project-management-1)
  - [DevExp](#devexp-1)
  - [CI/CD and Operation](#cicd-and-operation-1)
- [Questions](#questions)
    - [Q1](#q1)
    - [A1](#a1)
    - [Q2](#q2)
    - [A2](#a2)
    - [Q3](#q3)
    - [A3](#a3)
    - [Q4](#q4)
    - [A4](#a4)

## Gruppen-Konventionen
[back to top](#Dokumentation-der-Gruppe-2)

- Primäre Kommunikationsplattform: Discord
- Kollaborations-Best-Practices: Kanban

### Festgelegte Sprachen

- Backend: Python
- Navigations-service: grpc
- Datenbank: Postgres
- (frontend: html/js/css(/php))

### Code Styling

- Underscore (underscore_example)
- Englisch
- Tab(4 Leerzeichen)
- Linter: pylint
- Formatter: black

### Merge Request Definition of Done

- Lauffähig
- Tests(Unit & Integration)
- Erfüllt Anforderungen (Issues)
- Code styling erfüllt
- Requires approval from at least one reviewer.
- All necessary documentation must be included at the time of creation; merge requests with missing or incomplete 
documentation will be rejected.

## Server Erreichbarkeit
[back to top](#Dokumentation-der-Gruppe-2)

Jedes der Server wird auf seine eigene Weise erreicht. Hier wird festgehalten, auf welche Weise man den jeweiligen Server erreichen kann.

### Map-Server

Aufbau einer Anfrage:

```curl https://maps.proxy.devops-pse.users.h-da.cloud/map?name=skyrim```

oder mit jq ```curl https://maps.proxy.devops-pse.users.h-da.cloud/map?name=skyrim | jq```

### Deployment-Server

Es benötigt einige Schritte und einen [ssh-Schlüssel](https://code.fbi.h-da.de/help/user/ssh.md#generate-an-ssh-key-pair) um Zugriff auf den Deployment-Server zu erhalten.

- Verbinden mit ssh-Server ```ssh debian@group2.devops-pse.users.h-da.cloud``` 

- Passwort für den Zugriff auf den lokalen ssh-Schlüssel eingeben
	
- User zum Server hinzufügen, indem der public ssh-key zur Datei ".ssh/authorized_keys" hinzugefügt wird.

Deployment-Server Links (mit TLS):
- [API](https://api.group2.proxy.devops-pse.users.h-da.cloud/): ```https://api.group2.proxy.devops-pse.users.h-da.cloud/```
- [Frontend](https://group2.proxy.devops-pse.users.h-da.cloud/): ```https://group2.proxy.devops-pse.users.h-da.cloud/```

Um auf dem Deployment-Server den Docker-Container zu starten bzw. zu stoppen, kann man im ~-Verzeichnis des Deployment-Servers ```make start``` und ```make stop``` verwenden oder mit ```cd ./app/``` in das eigentliche Verzeichnis wechseln und dort die zuvor erwähnten Befehle ausführen.

### Postgres-Server

[Postgres-UI](https://postgres.group2.proxy.devops-pse.users.h-da.cloud/): ```https://postgres.group2.proxy.devops-pse.users.h-da.cloud/```

Postgres-Backend: ```sre-backend.devops-pse.users.h-da.cloud``` (Only available from withing OpenStack cluster, so your deployment server)

- Port: ```5433```
- Username: ```pg-2```
- Password: ```pg-2```

## Useful commands
[back to top](#Dokumentation-der-Gruppe-2)

# Database Connection
[back to top](#Dokumentation-der-Gruppe-2)

## On server:
[back to top](#Dokumentation-der-Gruppe-2)

**Export database:** To export the database, the following command is executed within the Docker container. The PostgreSQL container ID is passed as a parameter, and the database is created as a PostgreSQL instance: 

```
docker exec -t 851713c3adfe pg_dumpall -c -U pg-2 > ~/dumpfile.sql
```

check if ```dumpfile.sql``` exists:

```
ls -l ~/dumpfile.sql
```

### Secure database on server
[back to top](#Dokumentation-der-Gruppe-2)

The command is used to create and secure backup of the database.
```
pg_dump -U pg-2 -d navigation > dumpfile.sql
```

## On Local computer:
[back to top](#Dokumentation-der-Gruppe-2)

The scp command is used to copy the dump file from the server to the local computer. The paths of the dump file on the server and the target path on the local computer are provided as parameters.

```
scp debian@group2.devops-pse.users.h-da.cloud:~/dumpfile.sql "path/to/repo"
```



### Insert dumpfile content into local database
[back to top](#Dokumentation-der-Gruppe-2)

This command recreates the PostgreSQL database running in a Docker container. The pipe operator sends the output of ```Get-Content``` to the next command, which executes and starts the database in the Docker container.

```
Get-Content dumpfile.sql | docker exec -i group2-postgres-1 psql -U pg-2 -d navigation
```

### Connect to local database
[back to top](#Dokumentation-der-Gruppe-2)

```docker exec -it group2-postgres-1 psql -U pg-2 -d navigation```

To connect to the local database, you need to start the following container: 
```
services:
  postgres:
    image: postgres:latest
    environment:
      POSTGRES_USER: pg-2
      POSTGRES_PASSWORD: pg-2
      POSTGRES_DB: navigation
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

```
Alternatively, one can start the local db with the following CLI commands:

Running for the first time:
```
docker/podman run -d \
  --name postgres \
  -e POSTGRES_USER=pg-2 \
  -e POSTGRES_PASSWORD=pg-2 \
  -e POSTGRES_DB=navigation \
  -p 5433:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  docker.io/library/postgres:latest
```
Running existing container:
```
docker/podman run -d \
  --name postgres \
  -e POSTGRES_USER=pg-2 \
  -e POSTGRES_PASSWORD=pg-2 \
  -e POSTGRES_DB=navigation \
  -p 5433:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  docker.io/library/postgres:latest
```

To start the database in Docker container: 
```
docker exec -it group2-postgres-1 psql -U pg-2 -d navigation
```

# Docker
[back to top](#Dokumentation-der-Gruppe-2)

### Display docker images

 ```docker images```

### Display running docker containers

 ```docker ps```


## Docker on local computer
[back to top](#Dokumentation-der-Gruppe-2)

### Build docker image
run the following command in git root-directory:

```make build```

this runs:
```
docker build -t registry.code.fbi.h-da.de/bpse-wise2425/group2/test-application:latest --platform
linux/amd64 .
```
```--platform linux/amd64``` is only necessary for ARM systems like a MacBook


### Log into the docker registry
run the following command in git root-directory:

```make login```

this runs:

```docker login registry.code.fbi.h-da.de```

### Push the docker image
run the following command in git root-directory:

```make push```

this runs:

```
docker push registry.code.fbi.h-da.de/bpse-wise2425/group2/test-application:latest
```

## Docker on deployment server
[back to top](#Dokumentation-der-Gruppe-2)

### Log into the docker registry
run the following command on the deployment server:

```make login```

this runs:

```@docker login registry.code.fbi.h-da.de```[*command note](#command-notes)

**The first time you log in, you have to use the API access token, 
as you should not use your personal credentials on the server.**
- name: ```API_access```
- you can find the password in the file named "[API_access.txt](API_access.txt)" 

### Load docker image and start docker container
run the following command on the deployment server:

```make start```

this runs:

```@(cd ./app/ && docker-compose up -d)```[*command note](#command-notes)

### Stop running docker container
run the following command on the deployment server:

```make stop```

this runs:

```@(cd ./app/ && docker-compose down)```[*command note](#command-notes)

### Remove docker image
run the following command on the deployment server:

```make remove```

this runs:

```@docker rmi registry.code.fbi.h-da.de/bpse-wise2425/group2/test-application```[*command note](#command-notes)

## Update docker container (from local to server)
[back to top](#Dokumentation-der-Gruppe-2)

After saving your changes run the following command in git root-directory:

```make update```

this runs:

```
make login
make build
make push 
```

Then connect to the [server](#Deployment-Server) and run the following command on the standard directory "debian@group2:~$":

```make update```

this runs:

```
make login
make stop
make remove
make start
```

#### Command notes
- @ prevents the echoing of the executed command
- ( ) executes command in a subshell. 
This allows you to jump back to your original location after executing the command.

# make
[back to top](#Dokumentation-der-Gruppe-2)

## Makefile Beispiel
[back to top](#Dokumentation-der-Gruppe-2)

start:
- ```docker-compose up -d```

stop:
- ```docker-compose down```
    
cleanall:
- ```docker system prune -a```

# Stage 1 - Documentation
## Project Management
## DevExp
### Debugger (debugpy)
- Add debugypy to requirements.txt
- Add to the docker-compose.yml file so that the debugger runs in the Python container.

#### Changes in `docker-compose.yml`
```
command: >
  sh -c "pip install --upgrade pip && \
         pip install -r /app/requirements.txt && \
         python -Xfrozen_modules=off -m debugpy --listen 0.0.0.0:5678 --wait-for-client /app/src/dijkstra_algorithm.py"
```
- `-Xfrozen_modules=off`
  - So that breakpoints work correctly
- `listen 0.0.0.0:5678`
  - The debugger listens on all network interfaces (0.0.0.0) and waits for connections on port 5678
- Add ports to `docker-compose.yml`
```
ports:
      - "80:80"
      - "5678:5678"
```
##### Setup for Vs Code
Create a file .vscode/launch.json in the root directory.

```
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Remote Attach",
      "type": "debugpy",
      "request": "attach",
      "connect": {
        "host": "localhost",
        "port": 5678
      },
      "pathMappings": [
        {
          "localRoot": "${workspaceFolder}/src",
          "remoteRoot": "/app/src"
        }
      ]
    }
  ]
}

```
Remote Attach: so that VS Code can attach to a running Python application on a remote system

##### Setup for pycharm
...

## CI/CD and Operation

# Todos for Stage 1
[back to top](#Dokumentation-der-Gruppe-2)

## Project Management
[back to top](#Dokumentation-der-Gruppe-2)

- ~~Merge request Definition~~
- ~~Set issue workflow~~
- ~~Primary communication plattform~~
- Collaboration best practises + **Documentation**

## DevExp
[back to top](#Dokumentation-der-Gruppe-2)

### Installation and Removal of Dependencies

Two targets have been added to the `Makefile`: `install` and `remove`. These targets check if a Python virtual 
environment exists. If it does not, they will create it automatically. Then, depending on the command, they will install
or remove the dependencies.

#### Usage

To install the dependencies, run the following command from the root folder:

```bash
make install
```

To remove the dependencies, run:

```bash
make remove
```

These commands provide a "one-click" solution for managing dependencies, ensuring a clean and isolated environment.

---


- Start the application with "one-click" + **Documentation**
- Tests that run locally and in CI + **Documentation**
- Linter/formatter local and in CI + **Documentation**
- Debugger + **Documentation** 
- Project's setup process + Major design decision + **Documentation**

## CI/CD and Operation
[back to top](#Dokumentation-der-Gruppe-2)

- Pipeline to build the application
- Deployment of application to a server
- Trigger automated releases via GitLab
- Automated tests
  - unit tests for navigation service
  - unit tests for backend
  - startup test for seperated frontend
  - Display code coverage in GitLab with an icon **???**
- ~~Linting and formatting~~
- dependency proxy usage **???**
- code analysis tools **???**
- ~~application runs on server~~
- local development with a ~~local database~~
- The production database must never be deleted; only apply migrations **???**
- ~~No real credentials (e.g. for log in to the container registry) should be on the server, only scoped API
tokens~~

# Questions
[back to top](#Dokumentation-der-Gruppe-2)


### Q1:
The navigation service must not have a cache or a connection to the DB. Can the web backend instead load results into the DB and check whether a route has already been requested so that it can then be loaded from the DB?

### A1:

---

### Q2:
How does gitlab-ci service and artifacts work?

### A2:
Services are set for usage in the following script.

---

### Q3:
Where is "${CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX}" set?

### A3:
It's set in the predefined CI/CD GitLab variables (We can not see it in GitLab)

---

### Q4:
In relation to Q1, a couple of follow-up questions regarding the implementation and the interaction between 
map Service - Database - Web Backend and the Navigation Service:
- When there is a new request for a route finding, should the web backend get the latest state from
the Map Service every time and update the database accordingly?
- If so, isn't the database kind of pointless here? What is the point of having a database if we have to update the 
state at every request? Couldn't we simply communicate directly with the Map Service and use the data that we receive 
from it?
- If not, when or under what condition should the web backend update the database?
- Is it a feasible proposition to save the calculated routes in its own bridge table (Zwischentabelle) and read directly
from it if there are no changes to the database or would this be undesired / unnecessary?

### A4:

---
