# CI/CD & Docker Swarm Homework 02

**Author:** Ven KemLeap  
**Class:** Cloud Computing & DevOps  

---

## 📌 Project Overview

This repository contains a containerized Python Flask web microservice designed for an end-to-end **CI/CD Pipeline** using **Jenkins**, **Docker**, and **Docker Swarm**.

### Features:
- **Web Application:** Python Flask application serving dynamic host metadata, system health check (`/health`), and REST API endpoint (`/api/info`).
- **Containerization:** Production-ready `Dockerfile` with multi-worker Gunicorn and non-root security.
- **Continuous Integration / Continuous Deployment:** Declarative `Jenkinsfile` automating testing, container building, pushing to Docker Hub, and deploying to Docker Swarm.
- **Orchestration:** `docker-stack.yml` configured with 3 replicas, zero-downtime rolling updates, resource constraints, and overlay networking.

---

## 📂 Project Structure

```text
Homeword_Kemeleap_02/
├── .dockerignore         # Docker ignore rules
├── .gitignore            # Git ignore rules
├── Dockerfile            # Container image build instructions
├── Jenkinsfile           # Jenkins declarative CI/CD pipeline definition
├── README.md             # Project documentation
├── app.py                # Main Flask web application
├── docker-compose.yml    # Local development Compose file
├── docker-stack.yml      # Docker Swarm deployment stack file
├── requirements.txt      # Python dependencies (Flask, Gunicorn, Pytest)
└── test_app.py           # Automated unit tests for CI testing stage
```

---

## 🚀 1. Local Development & Testing

### Option A: Run with Python directly
```bash
# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run automated tests
pytest test_app.py -v

# Start application locally
python app.py
```
Open [http://localhost:5000](http://localhost:5000) in your browser.

---

### Option B: Run locally with Docker Compose
```bash
# Build and run container
docker compose up --build -d

# Check container status
docker compose ps

# View logs
docker compose logs -f

# Stop container
docker compose down
```

---

## 🛠️ 2. Docker Swarm Deployment (`docker-stack.yml`)

### Step 1: Initialize Swarm (if not already active)
```bash
docker swarm init
```

### Step 2: Build & Push Image
```bash
# Build image
docker build -t kemleapx20/cicd-web-app:latest .

# Log in and push to Docker Hub
docker login
docker push kemleapx20/cicd-web-app:latest
```

### Step 3: Deploy the Stack
```bash
docker stack deploy -c docker-stack.yml cicd-homework
```

### Step 4: Verify Deployment & Replicas
```bash
# Check stack services
docker stack services cicd-homework

# List the 3 running replica tasks
docker service ps cicd-homework_web
```

Test load balancing across the replicas by refreshing [http://localhost:5000](http://localhost:5000) or executing:
```bash
curl http://localhost:5000/health
```
*(Notice how the `hostname` field dynamically changes across the Swarm tasks).*

### Step 5: Remove the Stack
```bash
docker stack rm cicd-homework
```

---

## 🔄 3. Jenkins CI/CD Pipeline

The included `Jenkinsfile` automates the following stages:

1. **Checkout:** Clones the repository upon commit / webhook trigger.
2. **Lint & Unit Test:** Installs dependencies and runs `pytest test_app.py`.
3. **Docker Build:** Builds container image tagged with `BUILD_NUMBER` and `latest`.
4. **Docker Push:** Authenticates to Docker Hub using stored credentials and pushes images.
5. **Deploy to Docker Swarm:** Deploys or updates the stack seamlessly using rolling updates (`docker stack deploy`).
