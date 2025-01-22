# Server

Each server is accessed in its own way. This documents the method for accessing each respective server.

---

## Table of Contents

1. [Map-Server](#map-server)
2. [Deployment-Server](#deployment-server)
3. [Postgres-Server](#postgres-server)

## Map-Server

Requesting the map data:

```
curl https://maps.proxy.devops-pse.users.h-da.cloud/map?name=skyrim
```

or with jq:

```
curl https://maps.proxy.devops-pse.users.h-da.cloud/map?name=skyrim | jq
```

## Deployment-Server

Accessing the deployment server requires several steps and an [SSH key](https://code.fbi.h-da.de/help/user/ssh.md#generate-an-ssh-key-pair)

Connect to server:

```
ssh debian@group2.devops-pse.users.h-da.cloud
```

- Enter the password to access the local SSH key
- Add a user to the server by appending the public SSH key to the `.ssh/authorized_keys` file

Deployment-Server links (with TLS):

- [API](https://api.group2.proxy.devops-pse.users.h-da.cloud/healthz): &emsp; &emsp; &emsp; `https://api.group2.proxy.devops-pse.users.h-da.cloud/`
- [Frontend](https://group2.proxy.devops-pse.users.h-da.cloud/): &emsp; `https://group2.proxy.devops-pse.users.h-da.cloud/`

[back to top](#server)

## Postgres-Server

[Postgres-UI](https://postgres.group2.proxy.devops-pse.users.h-da.cloud/): `https://postgres.group2.proxy.devops-pse.users.h-da.cloud/`

Postgres-Backend: `sre-backend.devops-pse.users.h-da.cloud` (Only available from withing OpenStack cluster, so your deployment server)

| Parameter    | Value        |
| ------------ | ------------ |
| **Port**     | `5433`       |
| **Username** | `<USERNAME>` |
| **Password** | `<PASSWORD>` |
| **Host**     | `postgres`   |
| **Database** | `<DATABASE>` |

### Notes:

- Replace `<USERNAME>` and `<PASSWORD>` with the actual database credentials.
- Credentials can be found in the **lecture slides**
- For security, use environment variables to store sensitive credentials:
    ```bash
    export POSTGRES_USER=<USERNAME>
    export POSTGRES_PASSWORD=<PASSWORD>
    export POSTGRES_DB=<DATABASE>
    ```

[back to top](#server)
