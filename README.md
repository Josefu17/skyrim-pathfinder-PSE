[![coverage report](https://code.fbi.h-da.de/bpse-wise2425/group2/badges/main/coverage.svg)](https://code.fbi.h-da.de/bpse-wise2425/group2/-/commits/main)


# Documentation Project System Development
**Developers: Yusuf Birdane | Tarik-Cemal Atis | Arian Farzad**

In this section, you can find general information about the project.
- [Code styling](/docs/code_styling.md)
- [Server](/docs/server.md)
- [Database](/docs/database.md)
- [Docker](/docs/docker.md)
- [Make](/docs/make.md)
  
## Stage #1 - Documentation
In stage 1, we established a structure for the project. The frontend runs in a docker container on a server. The web 
backend fetches the map data from the map server and stores it in the database. The navigation service retrieves the 
data from the database, calculates the shortest route, and makes it available through an RPC API. 
The web backend api provides this route to the frontend, allowing the user to view the calculated route.

- [Project Management](/docs/management.md)
- [DevExp](/docs/devexp.md)
- [CI/CD Operation](/docs/ci.md)
- [Application](/docs/app.md)
- [Stage Overview](/docs/Stages/stage_1.md)