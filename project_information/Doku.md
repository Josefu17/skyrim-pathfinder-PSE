# Dokumentation der Gruppe 2

## Gruppen-Konventionen

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

## Offene Fragen

#### Q1:

Das Navigation-Service darf keinen Cache bzw. keine Verbindung zur DB haben. Kann das Web Backend stattdessen Ergebnisse in die DB laden und überprüfen, ob eine Route schonmal angefragt wurde, sodass diese dann aus der DB geladen werden kann?

#### A1:

#### Q2:

Die Funktionsweise des gitlab-ci, service und artifacts

#### A1:

## Useful commands

# Database Connection

```docker exec -it app_postgres_1 psql -U pg-2 -d navigation```

## On server:

Export database:


```docker exec -t 851713c3adfe pg_dumpall -c -U pg-2 > ~/dumpfile.sql```

check if ```dumpfile.sql``` exists:

```ls -l ~/dumpfile.sql```

## On Local computer:
secure copy from deployment server to local computer:

```scp debian@group2.devops-pse.users.h-da.cloud:~/dumpfile.sql "path/to/repo"```


## Update database on server
```pg_dump -U pg-2 -d navigation > dumpfile.sql```

## Insert dumpfile content into local database

```Get-Content dumpfile.sql | docker exec -i group2-postgres-1 psql -U pg-2 -d navigation```

## Connect to local database
```docker exec -it group2-postgres-1 psql -U pg-2 -d navigation```

# Docker
## Build docker image

```
docker build -t registry.code.fbi.h-da.de/bpsewise2425/group2/test-application:latest --platform
linux/amd64 .
```


## Log into the docker registery

```docker login registry.code.fbi.h-da.de```

## Push the docker image
```
docker push registry.code.fbi.h-da.de/bpsewise2425/group2/test-application:latest
```

## Display docker container

 ```docker ps```

## Makefile Beispiel
start:
- ```docker-compose up -d```

stop:
- ```docker-compose down```
    
cleanall:
- ```docker system prune -a```


# Todos for Stage 1
## Project Management
- ~~Merge request Definition~~
- ~~Set issue workflow~~
- ~~Primary communication plattform~~
- Collaboration best practises + **Documentation**

## DevExp
- Installation of dependencies with a "one-click" + **Documentation**
- Start the application with "one-click" + **Documentation**
- Tests that run locally and in CI + **Documentation**
- Linter/formatter local and in CI + **Documentation**
- Debugger + **Documentation** 
- Project's setup process + Major design decision + **Documentation**

## CI/CD and Operation
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



