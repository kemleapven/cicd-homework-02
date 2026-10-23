# Homework 2: CI/CD with Jenkins, GitHub, Docker & Docker Swarm on AWS

**Student Name:** Ven KemLeap  
**Class:** Master - Cloud Computing & DevOps  
**Repository:** [kemleapven/cicd-homework-02](https://github.com/kemleapven/cicd-homework-02)  
**Docker Hub:** [kemleapx20/cicd-web-app](https://hub.docker.com/r/kemleapx20/cicd-web-app)  

---

## 1. Project Overview & Architecture

This project implements an automated, production-grade **CI/CD Pipeline**. Any code pushed to GitHub automatically triggers a Jenkins pipeline to run unit tests, build a containerized Python Flask web microservice, push tagged images to **Amazon ECR** (and **Docker Hub**), and automatically roll out the new version to a **Docker Swarm cluster** (1 Manager + 1 Worker) on **Amazon EC2** with zero downtime.

```text
 ┌─────────────────┐       Git Push        ┌──────────────────┐
 │  Developer PC   │ ───────────────────► │  GitHub Repo     │
 └─────────────────┘                      └─────────┬────────┘
                                                    │ Webhook Payload
                                                    ▼
 ┌─────────────────────────────────────────────────────────────┐
 │                      Jenkins Server                         │
 │  1. Checkout SCM                                            │
 │  2. Lint & Unit Test (pytest)                               │
 │  3. Docker Build (tagged with ${BUILD_NUMBER} & latest)      │
 │  4. Authenticate & Push to Amazon ECR / Docker Hub          │
 │  5. Deploy / Update Stack on Docker Swarm Manager           │
 └──────────────┬───────────────────────────────┬──────────────┘
                │ Push Image                    │ docker stack deploy
                ▼                               ▼
 ┌─────────────────────────┐     ┌─────────────────────────────┐
 │  Amazon ECR / Registry  │     │   Docker Swarm on AWS EC2   │
 │  (Private Repository)   │     │  ┌───────────────────────┐  │
 └──────────────┬──────────┘     │  │ Swarm Manager (EC2)   │  │
                │ Pull Image     │  └───────────┬───────────┘  │
                └───────────────►│              │ Overlay Net  │
                                 │  ┌───────────▼───────────┐  │
                                 │  │ Swarm Worker (EC2)    │  │
                                 │  └───────────────────────┘  │
                                 │  Replicas: 3 (Auto LB)      │
                                 └─────────────────────────────┘
```

---

## 2. Repository Structure

```text
Homeword_Kemeleap_02/
├── .dockerignore                 # Excludes unnecessary build files
├── .gitignore                    # Excludes Python bytecode, caches, envs
├── Dockerfile                    # Production multi-worker Gunicorn container
├── Jenkinsfile                   # Declarative CI/CD pipeline (Cross-Platform)
├── README.md                     # Complete project documentation
├── app.py                        # Python Flask application
├── docker-compose.yml            # Local development Compose file
├── docker-stack.yml              # Production Swarm stack specification
├── requirements.txt              # Application dependencies
└── test_app.py                   # Automated unit tests for CI test stage
```

---

## 3. GitHub Workflow & Pull Request (Deliverable 1)

1. Development is done on feature branches:
   ```bash
   git checkout -b feature/aws-ecr-swarm-pipeline
   # Make changes and commit
   git add .
   git commit -m "Enhance Jenkinsfile with Amazon ECR authentication and Swarm registry auth"
   git push origin feature/aws-ecr-swarm-pipeline
   ```
2. A **Pull Request (PR)** is opened on GitHub from `feature/aws-ecr-swarm-pipeline` into `main`.
3. After review, the PR is merged into `main`.
4. GitHub Webhook triggers Jenkins automatically on the push event.

---

## 4. Containerization & Local Testing (Deliverable 2)

### Run Unit Tests
```bash
python -m pytest test_app.py -v
```

### Build & Test Container Locally
```bash
docker build -t kemleapx20/cicd-web-app:latest .
docker run -d -p 5000:5000 --name cicd-test kemleapx20/cicd-web-app:latest
curl http://localhost:5000/health
docker rm -f cicd-test
```

---

## 5. Amazon ECR Configuration (Deliverable 3)

### Step 1: Create a Private Amazon ECR Repository
```bash
aws ecr create-repository \
    --repository-name cicd-web-app \
    --region ap-southeast-1 \
    --image-scanning-configuration scanOnPush=true
```

### Step 2: Authenticate Docker to ECR
```bash
aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.ap-southeast-1.amazonaws.com
```

### Step 3: Tag and Push Image to ECR
```bash
docker tag kemleapx20/cicd-web-app:latest <AWS_ACCOUNT_ID>.dkr.ecr.ap-southeast-1.amazonaws.com/cicd-web-app:latest
docker tag kemleapx20/cicd-web-app:latest <AWS_ACCOUNT_ID>.dkr.ecr.ap-southeast-1.amazonaws.com/cicd-web-app:${BUILD_NUMBER}
docker push <AWS_ACCOUNT_ID>.dkr.ecr.ap-southeast-1.amazonaws.com/cicd-web-app:${BUILD_NUMBER}
docker push <AWS_ACCOUNT_ID>.dkr.ecr.ap-southeast-1.amazonaws.com/cicd-web-app:latest
```

---

## 6. AWS EC2 Docker Swarm Cluster Setup (Deliverable 4)

### Security Groups Rules
| Port / Protocol | Source | Purpose |
|---|---|---|
| `TCP 22` | Admin IP | SSH access |
| `TCP 5000` | `0.0.0.0/0` | Web application access |
| `TCP 2377` | Swarm nodes SG / Private Subnet | Cluster management communication |
| `TCP/UDP 7946` | Swarm nodes SG / Private Subnet | Node-to-node discovery |
| `UDP 4789` | Swarm nodes SG / Private Subnet | Overlay network traffic |

### Step 1: Initialize Swarm on EC2 Manager Node
```bash
# On EC2 Manager instance:
sudo docker swarm init --advertise-addr <MANAGER_PRIVATE_IP>
```
The command outputs the join token for workers:
```bash
docker swarm join --token SWMTKN-1-xxxx <MANAGER_PRIVATE_IP>:2377
```

### Step 2: Join EC2 Worker Node
```bash
# On EC2 Worker instance:
sudo docker swarm join --token <TOKEN_FROM_STEP_1> <MANAGER_PRIVATE_IP>:2377
```

### Step 3: Verify Cluster Status (On Manager)
```bash
sudo docker node ls
```
*Expected output: Both manager and worker nodes report `Ready` and `Active` status.*

---

## 7. Jenkins CI/CD Pipeline Automation

The declarative [`Jenkinsfile`](./Jenkinsfile) handles:
1. **Lint & Unit Test:** Automatically installs requirements and executes unit tests.
2. **Docker Build:** Builds container image tagged with `${BUILD_NUMBER}` and `latest`.
3. **Registry Push:** Authenticates to Amazon ECR (`aws ecr get-login-password`) and Docker Hub, pushing versioned tags.
4. **Deploy to Swarm:** Executes `docker stack deploy --with-registry-auth -c docker-stack.yml cicd-homework`. The `--with-registry-auth` flag passes ECR credentials to Swarm worker nodes so they can pull private ECR images without manual login.

---

## 8. Verification & Rolling Updates

1. **Verify Services:**
   ```bash
   docker stack services cicd-homework
   docker service ps cicd-homework_web
   ```
2. **Test Load Balancing:**
   ```bash
   curl http://<EC2_PUBLIC_IP>:5000/health
   ```
   *Notice the `hostname` changes dynamically across requests, confirming Swarm routing mesh load balances traffic across all 3 replicas.*

3. **Verify Zero-Downtime Rolling Update:**
   When a new commit is pushed, Swarm updates 1 replica at a time (`parallelism: 1`, `delay: 10s`, `order: start-first`), ensuring the web service remains 100% available with zero downtime.

---

## 9. Key Challenges & Solutions

1. **Windows vs Linux Shell in Jenkins:**
   - *Problem:* Jenkins controller on Windows threw `Cannot run program "sh"` because Unix shell was not on Windows PATH.
   - *Solution:* Used Jenkins `isUnix()` condition to dynamically execute `bat` on Windows and `sh` on Linux.
2. **Exposing Local Jenkins to GitHub Webhook:**
   - *Problem:* Local Jenkins on `localhost:9090` cannot receive GitHub webhooks behind NAT.
   - *Solution:* Deployed Cloudflare Tunnel to provide an SSL-secured public domain (`https://thoughts-cakes-household-tamil.trycloudflare.com/github-webhook/`).
3. **Private ECR Authentication on Swarm Worker Nodes:**
   - *Problem:* Worker nodes cannot pull private ECR images if only the manager authenticated.
   - *Solution:* Deployed using `docker stack deploy --with-registry-auth` so the manager safely forwards registry authentication tokens to all worker nodes in the swarm.
