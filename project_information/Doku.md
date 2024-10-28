# Dokumentation der Gruppe 2

## Table of contents
- [Dokumentation der Gruppe 2](#Dokumentation-der-Gruppe-2)
  - [Gruppen-Konventionen](#Gruppen-Konventionen)
  - [Server Erreichbarkeit](#Server-Erreichbarkeit)
  - [Useful commands](#Useful-commands)
- [Database Connection](#Database-Connection)
  - [On server](#On-server)
  - [On Local computer](#On-Local-computer)
  - [Update database on server](#Update-database-on-server)
  - [Insert dumpfile content into local database](#Insert-dumpfile-content-into-local-database)
  - [Connect to local database](#Connect-to-local-database)
- [Docker](#Docker)
  - [Docker on local computer](#Docker-on-local-computer)
  - [Docker on deployment server](#Docker-on-deployment-server)
  - [Update docker container (from local to server)](#Update-docker-container-from-local-to-server)
- [make](#make)
  - [Makefile Beispiel](#Makefile-Beispiel)
- [Todos for Stage 1](#Todos-for-Stage-1)
  - [Project Management](#Project-Management)
  - [DevExp](#DevExp)
  - CI/CD and Operation
- [Questions](#Questions)

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

## Server Erreichbarkeit
[back to top](#Dokumentation-der-Gruppe-2)

Jedes der Server wird auf seine eigene Weise erreicht. Hier wird festgehalten, auf welche Weise man den jeweiligen Server erreichen kann.

### Map-Server

Aufbau einer Anfrage:

```curl https://maps.proxy.devops-pse.users.h-da.cloud/map?name=skyrim```

oder mit jq ```curl https://maps.proxy.devops-pse.users.h-da.cloud/map?name=skyrim | jq```

### Deployment-Server

Es benötigt einige Schritte und einen [ssh-Schlüssel](https://code.fbi.h-da.de/help/user/ssh.md#generate-an-ssh-key-pair) um Zugriff auf den Deployment-Server zu erhalten.

-> Verbinden mit ssh-Server ```ssh debian@group2.devops-pse.users.h-da.cloud``` 

-> Passwort für den Zugriff auf den lokalen ssh-Schlüssel eingeben
	
-> User zum Server hinzufügen, indem der public ssh-key zur Datei ".ssh/authorized_keys" hinzugefügt wird.

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

```docker exec -it app_postgres_1 psql -U pg-2 -d navigation```

## On server:
[back to top](#Dokumentation-der-Gruppe-2)

Export database:

```docker exec -t 851713c3adfe pg_dumpall -c -U pg-2 > ~/dumpfile.sql```

check if ```dumpfile.sql``` exists:

```ls -l ~/dumpfile.sql```

## On Local computer:
[back to top](#Dokumentation-der-Gruppe-2)

secure copy from deployment server to local computer:

```scp debian@group2.devops-pse.users.h-da.cloud:~/dumpfile.sql "path/to/repo"```

## Update database on server
[back to top](#Dokumentation-der-Gruppe-2)

```pg_dump -U pg-2 -d navigation > dumpfile.sql```

## Insert dumpfile content into local database
[back to top](#Dokumentation-der-Gruppe-2)

```Get-Content dumpfile.sql | docker exec -i group2-postgres-1 psql -U pg-2 -d navigation```

## Connect to local database
[back to top](#Dokumentation-der-Gruppe-2)

```docker exec -it group2-postgres-1 psql -U pg-2 -d navigation```

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
```--platform linux/amd64``` is only for ARM system like a MacBook


### Log into the docker registery
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

### Log into the docker registery
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

- Installation of dependencies with a "one-click" + **Documentation**
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


### Q2:
How does gitlab-ci service and artifacts work?

### A1:

