# API Documentation

This document details the API routes provided by the backend.

---

## Endpoints Overview

1. [Maps](#maps)  
2. [Cities](#cities)  
3. [Route Calculation](#route-calculation)  
4. [Health Check](#health-check)

---

## Maps

**`GET /maps`**  
Fetches all map data, including cities and connections.

### Response Example
```json
{
  "cities": [
    {
      "id": 1,
      "name": "Markarth",
      "position_x": 380,
      "position_y": 1196
    },
    {
      "id": 2,
      "name": "Karthwasten",
      "position_x": 628,
      "position_y": 992
    }
  ],
  "connections": [
    {
      "parent_city_id": 1,
      "child_city_id": 2
    },
    {
      "parent_city_id": 2,
      "child_city_id": 3
    }
  ]
}
```

---

[back to top](#api-documentation)
## Cities

**`GET /cities`**  
Fetches all city data.

### Response Example
```json
{
  "cities": [
    {
      "name": "Markarth",
      "position_x": 380,
      "position_y": 1196
    },
    {
      "name": "Karthwasten",
      "position_x": 628,
      "position_y": 992
    }
  ]
}
```

---


### Error Example
```json
{
  "error": "Start and end cities are required"
}
```

---

## Health Check

**`GET /healthz`**  
Verifies the application's health status by checking critical services.

### Criteria
1. **Database Connection**: Executes a `SELECT 1` query to verify connectivity.
2. **Map Service Connection**: Sends a request to the map service and checks for a `200` response.
3. **Navigation Service Connection**: Sends a request to the navigation service and checks for a `200` response.

### Response Example (Healthy)
```json
{
  "details": {
    "database_connection": true,
    "frontend_availability": true,
    "map_service_connection": true,
    "navigation_service_connection": true
  },
  "status": "healthy"
}
```

### Response Example (Unhealthy)
```json
{
  "details": {
    "database_connection": true,
    "map_service_connection": true,
    "frontend_availability": false,
    "message": "Elements are missing",
    "missing_elements": [
      {
        "id": "root",
        "tag": "div"
      }
    ],
    "navigation_service_connection": true
  },
  "status": "unhealthy"
}
```

## User Management

### ```POST /auth/register```
Registers a new user and stores their credentials in the database.

Request Body:
```json
{
  "username": "Max Mustermann"
}
```

Response:
```json
{
    "message": "User Max Mustermann registered successfully.",
    "user": {
        "id": 6,
        "username": "Max Mustermann"
    }
}
```

### ```POST /auth/login```
Checks if the user exists in the database and returns their username and id.

Request Body:
```json
{
  "username": "Max Mustermann"
}
```

Response:
```json
{
    "message": "User Max Mustermann logged in successfully.",
    "user": {
        "id": 6,
        "username": "Max Mustermann"
    }
}
```

## Route History Management

### Route Calculation

**`POST /cities/route?startpoint=<city>&endpoint=<city>`**  
Calculates the shortest route between two cities.

Parameters

- `startpoint`: The starting city name (required).
- `endpoint`: The destination city name (required).
- `user_id`: The user's ID (optional).

Response Example

```json
{
    "alternative_distance": 1750.45,
    "alternative_route": {
        "0": "Riften",
        "1": "Shor’s Stone",
        "2": "Riften",
        "3": "Shor’s Stone",
        "4": "Windhelm",
        "5": "Winterhold"
    },
    "distance": 1297.55,
    "route": {
        "0": "Riften",
        "1": "Shor’s Stone",
        "2": "Windhelm",
        "3": "Winterhold"
    }
}
```

### Route deletion
**`DELETE /cities/route?user_id=<user_id>&route_id=<route_id>`**
Deletes a route from the database.

Parameters

- `user_id`: The user's ID (required).
- `route_id`: The route's ID (required).

Response Example

```json
{
    "success": "Route deleted"
}
```
[back to top](#api-documentation)
