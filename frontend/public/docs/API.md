# API Documentation

This document details the API routes provided by the backend.

---

## Endpoints Overview

1. [Maps](#maps)
2. [Cities](#cities)
3. [Route Calculation](#route-calculation)
4. [Health Check](#health-check)
5. [User Management](#user-management)
6. [Metrics](#metrics)

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

### `POST /auth/register`

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

### `POST /auth/login`

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

**`POST /users/<int:user_id>/routes`** and **`POST /routes`**

Calculates the shortest route between two cities.

Request body

- `startpoint`: The starting city name (required).
- `endpoint`: The destination city name (required).

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

**`DELETE /users/<int:user_id>/routes/<int:route_id>`**
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

### Route filtering

**`GET /users/<int:user_id>/routes`**

Parameters

- `user_id`: The user's ID.
- `limit`: The number of routes to return.
- `descending`: Sort routes in descending order.
- Optional parameters:
    - `from_date`: Filter routes from a specific date.
    - `to_date`: Filter routes up to a specific date.
    - `startpoint`: Filter routes by starting city.
    - `endpoint`: Filter routes by destination city.

Request Example

```json
{
    "user_id": 7,
    "limit": 10,
    "descending": true
}
```

Response Example

```json
{
    "routes": [
        {
            "endpoint": "Riften",
            "id": 14,
            "route": {
                "alternative_distance": 2376.27,
                "alternative_route": {
                    "0": "Markarth",
                    "1": "Falkreath",
                    "2": "Helgen",
                    "3": "Ivarstead",
                    "4": "Riften"
                },
                "distance": 2343.5,
                "route": {
                    "0": "Markarth",
                    "1": "Rorikstead",
                    "2": "Whiterun",
                    "3": "Ivarstead",
                    "4": "Riften"
                }
            },
            "startpoint": "Markarth"
        },
        {
            "endpoint": "Winterhold",
            "id": 12,
            "route": {
                "alternative_distance": 2055.9,
                "alternative_route": {
                    "0": "Markarth",
                    "1": "Karthwasten",
                    "2": "Dragon Bridge",
                    "3": "Morthal",
                    "4": "Dawnstar",
                    "5": "Winterhold"
                },
                "distance": 2008.69,
                "route": {
                    "0": "Markarth",
                    "1": "Rorikstead",
                    "2": "Morthal",
                    "3": "Dawnstar",
                    "4": "Winterhold"
                }
            },
            "startpoint": "Markarth"
        },
        {
            "endpoint": "Riften",
            "id": 13,
            "route": {
                "alternative_distance": 2376.27,
                "alternative_route": {
                    "0": "Markarth",
                    "1": "Falkreath",
                    "2": "Helgen",
                    "3": "Ivarstead",
                    "4": "Riften"
                },
                "distance": 2343.5,
                "route": {
                    "0": "Markarth",
                    "1": "Rorikstead",
                    "2": "Whiterun",
                    "3": "Ivarstead",
                    "4": "Riften"
                }
            },
            "startpoint": "Markarth"
        }
    ]
}
```

### Clear route history

**`DELETE /users/<int:user_id>/routes`**

Parameters

- `user_id`: The user's ID.

Response Example

```json
{
    "deleted_count": 2,
    "success": "Route history cleared"
}
```

**`DELETE /users/<string:user_name>/routes`**

Response Example

```json
{
    "deleted_count": 3,
    "success": "Route history cleared"
}
```

[back to top](#api-documentation)

## Metrics

The `/metrics` endpoint provides the four golden signals for monitoring the application:

1. **Latency:** The time taken to calculate a route.
2. **Traffic:** The number of logged in user and requested route calculation.
3. **Errors:** The number of failed route calculations.
4. **Saturation:** The number of concurrent users.
