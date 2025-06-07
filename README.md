# 🚀 FastAPI URL Shortener

A simple and efficient **URL shortener API** built using **FastAPI**. This project allows users to create, retrieve, and redirect shortened URLs with account-based access. It includes user authentication via **JWT**, password hashing with **bcrypt**, and uses a **PostgreSQL** database. The API is containerized using **Docker** and includes Nginx for production-ready deployments.

Additionally, the application is integrated with **Prometheus** for monitoring and **Grafana** for visualization, enabling real-time monitoring of key metrics.


---

## 🛠️ Tech Stack

| Category          | Technologies Used                                    |
|-------------------|------------------------------------------------------|
| **Backend**       | FastAPI, SQLAlchemy, PyDantic                        |
| **Database**      | PostgreSQL, Asyncpg                                  |
| **Caching**       | Aioredis                                             |
| **Security**      | AuthLib (JWT), bcrypt                                |
| **Rate Limiting** | SlowAPI                                              |
| **Monitoring**    | Prometheus, Grafana                                  |
| **Testing**       | PyTest                                               |
| **Deployment**    | Docker, Docker Compose, Nginx                        |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/fastapi_url_shortener.git
cd fastapi_url_shortener
```

### 2. Start Docker Compose

```bash
docker compose up --build
```

🕒 *Wait until the deployment is complete. Services will be available shortly.*

---

## 📦 Features

- 🔐 Secure user authentication (JWT, bcrypt)
- 🔗 URL shortening and redirection
- 📈 Rate limiting with SlowAPI
- 🧪 Test coverage with PyTest
- 🐳 Full Docker support with Nginx reverse proxy
- ⚡ High-performance async backend
- 📊 Prometheus monitoring integration for real-time metrics collection
- 📈 Grafana dashboards for visualizing API performance in real-time