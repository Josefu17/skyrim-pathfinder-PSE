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

- Underscore/Camelcase?
- Englisch
- Tab(4 Leerzeichen)

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

## Möglicherweise nützliche Befehle

Dateien-Suche mit ```find /path/to/your/project -name "*.yaml"```

Alle Docker-Prozesse anzeigen mit ```docker ps```

### Makefile Beispiel
start:
- ```docker-compose up -d```

console:
- ```docker exec -it ewa_lab_php_apache bash```

stop:
- ```docker-compose down```

build:
- ```docker-compose down -v```
- ```docker-compose build```
- ```docker-compose up -d --force-recreate mariadb```
- ```docker-compose up -d```

clean:
- ```docker rm -v --force ewa_lab_php_apache```
- ```docker rm -v --force ewa_lab_mariadb```
- ```docker rm -v --force ewa_lab_phpmyadmin```
- ```docker network rm ewa_lab_net```
    
cleanall:
- ```docker system prune -a```
