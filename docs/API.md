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

[back to top](#api-documentation)
## Route Calculation

**`GET /cities/route?startpoint=<city>&endpoint=<city>`**  
Calculates the shortest route between two cities.

### Parameters
- `startpoint`: The starting city name (required).
- `endpoint`: The destination city name (required).

### Response Example
```json
{
  "distance": 1134.28,
  "route": {
    "0": "Whiterun",
    "1": "Ivarstead",
    "2": "Riften"
  }
}
```

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

[back to top](#api-documentation)
