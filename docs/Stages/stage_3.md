# Stage 3 Overview (Deadline 18.12.2024)

# Requirements of Stage 2

## **Requirements from Previous Stage**
  For remaining tasks, kindly refer to: [Stage 2](stage_2.md)  

---

## **New Requirements**

### **Database Management**
- **[Database Migration Practices](../../README.md#migrations)**  
  - **Adjust the database schema to accommodate new requirements**  
    - **Add a new table `User`**  
    - **Add a new table `Map`**
    - **Add a new table `route`**

    ✅ Completed

### **User register and login functionality**
  - **Implement a route for [user registration](../API.md#post-authregister)**  
    - **`POST /auth/register`**  
      ✅ Completed  
  - **Implement a route for [user login](../API.md#post-authlogin)**  
    - **`POST /auth/login`**  
      ✅ Completed

### **Route history management**
- **Implement a route for route history retrieval**  
  - **`GET /routes`**  
      ✅ Completed  
- **Implement a route for route history deletion**  
  - **`DELETE /routes`**  
      ✅ Completed  

### **Advanced route calculation**
- **Adjust the [navigation service](../App.md#stateless-navigation-service) to calculate an alternative route**
    - **Return an alternative route along with its distance**  
      ✅ Completed