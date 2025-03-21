# docker-with-postgres

Just a testing/practice repository for spinning up a Docker container with Postgres!

# Spinning Everything Up

Here’s how to get everything running. If something isn’t working, try checking the container logs or verifying that Docker is running properly.

## Spinning Up Docker

Make sure you have both Docker and Docker Compose installed on your machine. If installed, run:

```
docker compose up --build
```

This will start all necessary services. If you'd like a visual representation of what's running, you can use the **Docker Desktop app**.

### Troubleshooting

- Check running containers:  
  `docker ps`
- View logs for a specific service (e.g., Postgres):  
  `docker logs postgres_db`
- Restart everything if needed:  
  `docker compose down && docker compose up --build`

---

## Logging Into pgAdmin

Once all Docker containers are running, open your browser and go to:

[http://localhost:5050](http://localhost:5050)

### Login Credentials

- **Email**: `admin@admin.com`
- **Password**: `admin`

### Registering the Database

1. Right-click on **"Servers"**, then click **"Register" → "Server"**.
2. Go to the **General** tab:
   - **Name**: `Postgres DB`
3. Go to the **Connection** tab:
   - **Host name/address**: `db`
   - **Username**: `myuser`
   - **Password**: `mypassword`
4. Click **Save**, and you should be connected!
