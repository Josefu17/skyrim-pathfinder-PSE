# API Routes

# Maps

# Cities

# Route calculation

# healthz

Request the application's health status with:

```url
https://api.group2.proxy.devops-pse.users.h-da.cloud/healthz
```

Or [click here](https://api.group2.proxy.devops-pse.users.h-da.cloud/healthz)

The Response for the healthy application looks like:

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

The controller checks whether all criteria for the application's healthy status
are met and returns a response indicating the application's status as healthy.
If any criteria are not met, it returns an unhealthy status along with a specific
error message.

## Criteria

1. **Database Connection:**
   The database connection is tested with a simple query:
   "SELECT 1".
   If the result is not None, this criterion is marked as true.

2. **Frontend Availability:**
   The frontend availability is checked by sending a request to the frontend. 
   The response contains the frontend's page source code. 
   If the response status code is `200` and the response body covers the most important html tags, this criterion is marked as true.

3. **Map Service Connection:**
   The connection to the map service is verified by sending a request to the map service.
   If the response status code is `200`, this criterion is marked as true.

4. **Navigation Service Connection:**
   The navigation service connection test is similar to the map service connection test.
   If the response status code is `200`, this criterion is marked as true.

