# FastAPI-URL-Shortener
This is a simple and efficient URL shortener API built using **FastAPI**. The API supports creating, retrieving, and redirecting shortened URLs. It uses a **FastAPI** for backend, and **PostgreSQL** for db. It also uses accounts, **JWT** and **bcrypt** for encrypting logins and passwords in db. Full list of used technologies is below.

# Technologies:
FastAPI

SlowAPI

SQLAlchemy

Asyncpg

PyDantic

Aioredis

AuthLib(JWT)

Bcrypt

PyTest

Nginx

Docker

Docker Compose

# Steps to deploy

### 1. Create DB
```
psql -U [user]
CREATE DATBASE [db name, and change it in 'config.py']
```

### 2. Start Docker Compose
```
cd fastapi_url_shortener
docker compose up --build        *Wait until the deployment is complete*
```

### 3. Deployment finished