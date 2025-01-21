# Monitoring and Observability
This document provides an overview of metrics sent to Prometheus and visualized in Grafana.

---
## Table of Contents
1. [Prometheus Metrics](#prometheus-metrics)
2. [Grafana Dashboards](#grafana-dashboards)
   1. [Dashboard 1: Traffic Metrics](#dashboard-1-traffic-metrics)
   2. [Dashboard 2: Latency Metrics](#dashboard-2-latency-metrics)
   3. [Dashboard 3: Error Metrics](#dashboard-3-error-metrics)
   4. [Dashboard 4: Saturation Metrics](#dashboard-4-saturation-metrics)

---

## Prometheus Metrics
The application sends the following metrics to Prometheus for monitoring:
- traffic:
  - m_anonymous_calculated_route
  - m_logged_in_users
  - m_registered_calculated_route
- latency:
  - m_anonymous_avg_execution_time
  - m_registered_avg_execution_time
- error:
  - m_error_calculating_route
  - m_error_clearing_route_history
  - m_error_existing_username
  - m_error_missing_city
  - m_error_missing_username
  - m_error_route_not_found
  - m_error_user_not_found
- saturation:
  - m_concurrent_requests

---

## Grafana Dashboards
The Grafana dashboards provide insights into the application's performance and user interactions.

### Dashboard 1: Traffic Metrics
This dashboard visualizes the number of logged-in users and route calculations over time.
![Traffic Metrics](./images/grafana_traffic_dashboard.png)

### Dashboard 2: Latency Metrics
This dashboard displays the average execution time for route calculations by anonymous and registered users.
![Latency Metrics](./images/grafana_latency_dashboard.png)
