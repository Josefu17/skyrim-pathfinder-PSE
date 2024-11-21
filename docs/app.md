# Application
## Stateless navigation service
The Navigation Service uses the Dijkstra algorithm to calculate the best route between two cities. The function receives a graph, the start city, and the destination city as parameters.

First, the **min_heap**, **distances**, and **previous_nodes** are initialized:

- **min_heap**: This is a priority queue that sorts cities by the shortest known distance. It is initialized with the start city and a distance of 0.

- **distances**: This stores the shortest known distance to each city. Initially, all distances are set to infinity, except for the start city, which is set to 0.

- **previous_nodes**: This stores the city from which each other city is reached. It is used to reconstruct the actual path once the shortest route is found.

**Main logic**:

- As long as min_heap is not empty, the city with the lowest distance is chosen.
- If the current city is the destination city, the loop stops.
- It calculates the distance for each neighboring city. If the new distance is shorter than the current distance, the algorithm updates the distance and adds the neighboring city to the min_heap

**Path reconstruction:**

- It starts with the destination city and uses the previous_nodes to find the previous city in the route
- The path is backwards (``[::-1]``) because it is reconstructed from the destination city to the start city

**Method:**
- `get_route(start_city_name, end_city_name, data)`: the method that calculates the shortest route (if any) as well as the total distance
  - `data`: python dictionary that contains all the cities and connections information for the algorithm to use

**Returns:**

- The reconstructed path
- The distance to the destination city
- Return type is a python dictionary which then gets converted to a Json before being passed to the frontend by the backend
  
### RPC-API
#### Server:
The server uses `SimpleXMLRPCServer` to expose the `get_route` function via XML-RPC. It listens on port 8000 and handles incoming requests.

#### Client:
The client sends XML-RPC requests to the server to call the `get_route` function and retrieve a calculated route.

**Request**
```
<?xml version="1.0"?>
<methodCall>
  <methodName>get_route</methodName>
  <params>
    <param><value><string>Markarth</string></value></param>
    <param><value><string>Riften</string></value></param>
  </params>
</methodCall>
```
**Response**
```
<?xml version='1.0'?>
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
## Frontend
### Fetch and display maps from the Web Backend.
The ``load_cities()`` function fetches all cities with their x and y positions from http://localhost:5000/cities. The response returns JSON data that includes all cities in the database. We use JavaScript to create a DOM element to display all the cities.

### User Interaction
The user is provided with dropdown fields for both the starting point and the destination. Users can select cities and receive an optimal route to their destination. We have made the user interaction easy and intuitive, ensuring that users cannot select the same city for both the start and destination or enter an invalid city.

### Display the route on the map
After the user selects the start and destination city, the frontend sends a request (e.g.: http://localhost:5000/cities/route?startpoint=Markarth&endpoint=Riften). The server calculates the route and responds with the route and distance, which the frontend then displays in new DOM elements.
