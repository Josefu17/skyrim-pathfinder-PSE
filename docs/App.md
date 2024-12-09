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
  - **second\_distances**: Stores the second shortest known distance to each city. Initially, all distances are infinity.
  - **path**: Stores the shortest path found.
  - **second\_path**: Stores the second-shortest path found.

- **Main Logic**:
  - Repeatedly extracts the city with the lowest distance from `min_heap`.
  - Terminates once the destination city is reached, as by definition the shortest path to that city has been determined.
  - Updates distances for neighboring cities if a shorter path is found, adding them back to `min_heap`.
  - Also updates the second-shortest path if a new second-shortest path is found.

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
- **GET `/cities`**: Returns city details.
- **GET `/cities/route`**: Accepts `startpoint` and `endpoint` query parameters and returns the optimal route and distance.

These endpoints serve as the bridge between the frontend, database, and navigation service.

---

[back to top](#application)
## Frontend

### Fetch and Display Maps
The `load_cities()` function fetches all cities with their x and y positions from the backend (`/cities` endpoint). The frontend processes the JSON response and creates DOM elements to visually display the cities on the map.

### User Interaction
Users can:
- Select a starting city and a destination city from dropdown menus.
- Receive the optimal route and distance based on their selection.
- Ensure valid input with restrictions preventing duplicate or invalid city selections.

### Displaying the Route
Once a route is calculated, the backend sends the route and distance back to the frontend. The frontend updates the DOM to visually highlight the route and display the distance in a user-friendly format.



[back to top](#application)
