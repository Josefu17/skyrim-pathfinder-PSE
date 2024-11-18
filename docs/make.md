# make
We use a Makefile to execute multiple commands with a single command and automate tasks.
## Makefile Beispiel

```
start:
  docker-compose up -d

stop:
  docker-compose down
    
cleanall:
  docker system prune -a
```
