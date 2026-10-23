## 🚀 Homework 2: CI/CD Pipeline on AWS

### 📌 Author & Program
- **Student Name:** Ven KemLeap
- **Program:** Master - Cloud Computing & DevOps

---

### 📝 Summary of Changes
This pull request introduces the end-to-end automated deployment pipeline:
1. **EC2 Provisioning Helper:** Added automated setup script [`scripts/aws-ec2-setup.sh`](./scripts/aws-ec2-setup.sh) for Ubuntu instances.
2. **Amazon ECR Integration:** Automated authentication via `aws ecr get-login-password` in [`Jenkinsfile`](./Jenkinsfile) with fallback to Docker Hub.
3. **Docker Swarm Rolling Updates:** Configured [`docker-stack.yml`](./docker-stack.yml) with 3 replicas and `--with-registry-auth` for zero-downtime updates.
4. **Documentation & Deliverables:** Comprehensive [`README.md`](./README.md) and Word report document [`Homework_2_Report_Ven_KemLeap.docx`](./Homework_2_Report_Ven_KemLeap.docx).

---

### ✅ Verification Checklist
- [x] Application passes all local unit tests (`pytest test_app.py`)
- [x] Docker image builds cleanly and runs locally (`/health` returns HTTP 200)
- [x] Jenkins pipeline executes all stages (Checkout -> Test -> Build -> Push -> Deploy)
- [x] Swarm service deployed across nodes with 3 replicas
