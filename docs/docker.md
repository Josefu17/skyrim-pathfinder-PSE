# Docker

We use Docker and a Dockerfile to create an NGINX image, which we push to the server's registry. The frontend runs on this server accordingly.

## Makefile to deploy the application with only one command
// TODO

### Load docker image and start docker container
run the following command on the deployment server:

```make start```

this runs:

```@(cd ./app/ && docker-compose up -d)```[*command note](#command-notes)

### Stop running docker container
run the following command on the deployment server:

```make stop```

this runs:

```@(cd ./app/ && docker-compose down)```[*command note](#command-notes)

### Remove docker image
run the following command on the deployment server:

```make remove```

this runs:

```@docker rmi registry.code.fbi.h-da.de/bpse-wise2425/group2/test-application```[*command note](#command-notes)

## Useful docker commands
Displays all images

```
docker images
```
Display running docker containers
```
docker ps
```

## Docker on local computer

### Build docker image
run the following command in git root-directory:

```make build```

this runs:
```
docker build -t registry.code.fbi.h-da.de/bpse-wise2425/group2/test-application:latest --platform
linux/amd64 .
```
```--platform linux/amd64``` is only for ARM system like a MacBook


### Log into the docker registry
run the following command in git root-directory:

```make login```

this runs:

```docker login registry.code.fbi.h-da.de```

### Push the docker image
run the following command in git root-directory:

```make push```

this runs:

```
docker push registry.code.fbi.h-da.de/bpse-wise2425/group2/test-application:latest
```

## Docker on deployment server

### Log into the docker registry
run the following command on the deployment server:

```make login```

this runs:

```@docker login registry.code.fbi.h-da.de```[*command note](#command-notes)

**The first time you log in, you have to use an API access token, 
as you should not use your personal credentials on the server since they are stored on the server unencrypted!**

### Generating an API Access Token in GitLab

Follow these steps to generate a personal access token in GitLab:

1. **Log in to GitLab**:
   - Go to your GitLab instance and log in with your credentials.

2. **Navigate to Project Access Tokens**:
   - Go to project's page.
   - Navigate to Settings -> Access tokens

3. **Create a New Token**:
   - Enter a descriptive name (e.g., `ProjectX API Token`).
   - Set an **expiration date** if needed.
   - Select the required scopes (e.g., `api`, `read_repository`, etc.).
   - Click **Create personal access token**.

4. **Copy and Save the Token**:
   - Copy the generated token immediately. GitLab will not show it again.
   - Save it securely in your `.env` file or a credentials manager:
     ```plaintext
     API_ACCESS_TOKEN=your_generated_token
     ```

---

### Using the Token
- **In Code**: Access the token via environment variables:
  ```python
  import os
  token = os.getenv("API_ACCESS_TOKEN")
  ```
- **In CI Pipelines**:
  - Add the token as a **protected variable** in GitLab CI/CD settings:
    - Go to **Settings > CI/CD > Variables**.
    - Add a variable with the key `API_ACCESS_TOKEN` and paste the token as the value.

---

### Notes
- Do **not** commit the token to version control.
- Rotate the token periodically for better security.


## Update docker container (from local to server)
[back to top](#Docker)

After saving your changes run the following command in git root-directory:

```make update```

this runs:

```
make login
make build
make push 
```

Then connect to the [server](./server.md#deployment-server) and run the following command on the standard directory "debian@group2:~$":

```make update```

this runs:

```
make login
make stop
make remove
make start
```

#### Command notes
- @ prevents the echoing of the executed command
- ( ) executes command in a subshell. 
This allows you to jump back to your original location after executing the command.
