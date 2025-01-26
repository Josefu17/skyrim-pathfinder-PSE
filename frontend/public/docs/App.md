# Application

This document provides an overview of the application's architecture and functionality, detailing components like the
Stateless Navigation Service, RPC-API, Backend, and Frontend. It includes explanations of algorithms, API usage, and
user interaction flows.

---

## **Table of Contents**

1. [Stateless Navigation Service](#stateless-navigation-service)

    - Overview of Dijkstra's algorithm and method details

2. [RPC-API](#rpc-api)

    - Server and client communication via XML-RPC

3. [Backend](#backend)

    - Map data handling and RESTful API endpoints

4. [Frontend](#frontend)

## Stateless Navigation Service

The Navigation Service uses the Dijkstra algorithm to calculate the best route between two cities. The function receives a graph, the start city, and the destination city as parameters.

### Algorithm Details

- **Initialization**:

    - **min_heap**: A priority queue that sorts cities by the shortest known distance. It starts with the start city and a distance of 0.
    - **distances**: Stores the shortest known distance to each city. Initially, all distances are infinity, except for the start city, which is 0.
    - **second_distances**: Stores the second-shortest known distance to each city. Initially, all distances are infinity.
    - **path**: Stores the shortest path found.
    - **second_path**: Stores the second-shortest path found.

- **Main Logic**:
    - Repeatedly extracts the city with the lowest distance from `min_heap`.
    - Terminates only after all cities were visited. Since all possible paths are checked, the shortest possible route is found.
    - Updates distances for neighboring cities if a shorter path is found, adding them back to `min_heap`.
    - Also updates the second-shortest path if a new second-shortest path is found.
    - If the alternative path contains a city twice, the algorithm recalculates the path with current path to provide a valid short path.

### Method

- `get_route(start_city_name, end_city_name, data)`:
    - Calculates the shortest and second-shortest routes and total distances between two cities.
    - `data`: A Python dictionary containing all city and connection information.
    - **Returns**:
        - The reconstructed paths as lists.
        - The total distances to the destination city.
        - The result is returned as a dictionary and converted to JSON for the frontend.

---

[back to top](#application)

## RPC-API

### Server

The server exposes the `get_route` function using `SimpleXMLRPCServer`. It listens on port 8000 and handles incoming XML-RPC requests.

### Client

The client communicates with the server via XML-RPC, calling the `get_route` function to retrieve a calculated route.

#### Example Request

```xml
<?xml version="1.0"?>
<methodCall>
  <methodName>get_route</methodName>
  <params>
    <param><value><string>Markarth</string></value></param>
    <param><value><string>Riften</string></value></param>
  </params>
</methodCall>
```

#### Example Response

```xml
<?xml version="1.0"?>
<methodResponse>
  <params>
    <param>
      <value>
        <string>{
  "route": [
      "Markarth",
      "Rorikstead",
      "Whiterun",
      "Ivarstead",
      "Riften"
  ],
  "distance": 2343.5
}</string>
      </value>
    </param>
  </params>
</methodResponse>
```

---

[back to top](#application)

## Backend

### Fetch and Store Map

The backend fetches map data (cities and connections) from an external source and stores it in the database. This ensures the navigation service operates with up-to-date information.

### API Endpoints for Frontend

The backend exposes RESTful endpoints for the frontend:

- **GET `/maps`**: Returns all cities and connections.
- **GET `/cities`**: Returns all cities.
- **POST `/users/<int:user_id>/routes`**: Accepts startpoint, endpoint and user_id as request body, then returns the optimal route along with its distance. Additionally, provides an alternative route and its corresponding distance. Finally, it stores the user's route in the database.
- **POST `/routes`**: Accepts startpoint and endpoint as request body, then returns the optimal route along with its distance. Calculated routes are not stored in the database.
- **POST `/auth/regiser`**: Registers a new user and stores their credentials in the database.
- **POST `/auth/login`**: Checks if the user exists in the database and returns their username and id.
- **DELETE `/users/<int:user_id>/routes/<int:route_id>`**: Deletes a user's route from the database.
  These endpoints serve as the bridge between the frontend, database, and navigation service.
- **GET `/users/<int:user_id>/routes`**: Returns the user's route history.
- **DELETE `/users/<int:user_id>/routes`**: Deletes all routes associated with a user (by user`s id).
- **DELETE `/users/<string:user_name>/routes`**: Deletes all routes associated with a user (by user`s name).

---

[back to top](#application)

## Frontend

### Fetch and Display Maps

The `fetchMapData()` function fetches all cities with their positions and connections from the backend (`/maps` endpoint). The frontend processes the JSON response and creates DOM elements to visually display the cities on the map.

### User Interaction

Users can:

- Select a starting city and a destination city from the interactive map by clicking on the nodes.
- Receive the optimal (and alternative) route, along with the distance, based on their selection. To toggle between the main and alternative routes, click the "Show Alternative Route" / "Show Main Route" button.
- TODO: Ensure valid input by implementing restrictions to prevent duplicate or invalid city selections.
- Create an account by entering a username and submitting it by clicking the "`Register`" button. Both options can be accessed by clicking the "`Register Now`" button in the left section.

### Displaying the Documtentation

Our application offers insight in its developement process by giving the user free access to this documentation in the Documentation section of the header navigation. It is designed, to navigate through the documentation as usually(without actually leaving the documentation page), so that there should'nt be anything the user has to get used to anew. Currently using the actual documentation is yet implemented, so the files are copied to the public folder of the frontend to enable access to it.

### Displaying the Route

Once a route is calculated, the backend sends the route and distance back to the frontend. The frontend updates the relevant DOM to visually highlight the route and display the distance in a user-friendly format.

[back to top](#application)
