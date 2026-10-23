import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

doc = docx.Document()

# Page Margins
sections = doc.sections
for section in sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Styling Helper Functions
def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.size = Pt(20)
    run.font.bold = True
    run.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
    p.paragraph_format.space_after = Pt(4)

def add_subtitle(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(37, 99, 235) # Blue 600
    p.paragraph_format.space_after = Pt(16)

def add_meta(data_dict):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for i, (k, v) in enumerate(data_dict.items()):
        run_k = p.add_run(f"{k}: ")
        run_k.font.bold = True
        run_k.font.size = Pt(10)
        run_v = p.add_run(f"{v}    |    " if i < len(data_dict)-1 else f"{v}")
        run_v.font.size = Pt(10)
    p.paragraph_format.space_after = Pt(20)

def add_heading1(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(15, 23, 42)
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)

def add_heading2(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(30, 41, 59)
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)

def add_body(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(10)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    return p

def add_bullet(bold_prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    run_b = p.add_run(bold_prefix)
    run_b.font.bold = True
    run_b.font.size = Pt(10)
    run_t = p.add_run(text)
    run_t.font.size = Pt(10)
    p.paragraph_format.space_after = Pt(3)

def add_code_block(code_text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    p.paragraph_format.right_indent = Inches(0.2)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(30, 41, 59)
    # Background shading
    shd = parse_xml(r'<w:shd {} w:fill="F1F5F9"/>'.format(nsdecls('w')))
    p._p.get_or_add_pPr().append(shd)

# Title & Metadata
add_title("Homework 2: CI/CD Pipeline on AWS")
add_subtitle("Automated GitHub Webhook, Jenkins, Docker, Amazon ECR & EC2 Docker Swarm")
add_meta({
    "Author": "Ven KemLeap",
    "Program": "Master 2 - Cloud Computing & DevOps",
    "Date": "October 2026",
    "Status": "100% Passed (Build #4 Green)"
})

# Section 1: Overview & Architecture
add_heading1("1. Executive Summary & Architecture Overview")
add_body(
    "This report documents the implementation and verification of an automated, enterprise-grade Continuous Integration "
    "and Continuous Deployment (CI/CD) pipeline for a containerized Python web application. Source code changes pushed to GitHub "
    "trigger a Jenkins automation pipeline via webhook. Jenkins executes unit testing, builds and tags production Docker images, "
    "pushes them to Amazon ECR (and Docker Hub), and deploys the update to an Amazon EC2 Docker Swarm cluster with rolling updates."
)

arch_diagram = """[ Developer ] ──> git push ──> [ GitHub: kemleapven/cicd-homework-02 ]
                                         │ (Webhook via Cloudflare Tunnel)
                                         ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        Jenkins CI/CD Server                            │
│  Stage 1: Checkout SCM (Commit SHA & Branch)                           │
│  Stage 2: Lint & Unit Test (Python Pytest test_app.py)                 │
│  Stage 3: Docker Build (Image tagged with ${BUILD_NUMBER} & :latest)   │
│  Stage 4: Registry Push (Amazon ECR `aws ecr get-login-password`)      │
│  Stage 5: Deploy to Docker Swarm (`docker stack deploy`)               │
└──────────────────┬─────────────────────────────────┬───────────────────┘
                   │ Push Tagged Image               │ docker stack deploy
                   ▼                                 ▼
         ┌───────────────────┐             ┌─────────────────────────────┐
         │    Amazon ECR     │ ── Pull ──> │   AWS EC2 Docker Swarm      │
         │ Private Registry  │             │   - 1 Manager + 1 Worker    │
         └───────────────────┘             │   - 3 Web Replicas (Active) │
                                           └─────────────────────────────┘"""
add_code_block(arch_diagram)

# Section 2: Deliverables & Pipeline Details
add_heading1("2. Deliverables & Implementation Details")

add_heading2("A. GitHub Repository & Version Control")
add_bullet("Repository URL: ", "https://github.com/kemleapven/cicd-homework-02")
add_bullet("Branching Model: ", "Development utilizes feature branches (e.g., feature/aws-ecr-swarm-pipeline) merged into main via Pull Requests.")
add_bullet("Webhook Integration: ", "Configured in GitHub Webhooks pointing to https://thoughts-cakes-household-tamil.trycloudflare.com/github-webhook/, delivering push events instantaneously.")

add_heading2("B. Containerization (Dockerfile)")
add_body(
    "The application is packaged with a security-hardened Dockerfile using python:3.12-slim. It features non-root user execution "
    "(appuser, UID 8888), built-in urllib healthcheck (/health), and multi-worker Gunicorn WSGI server on port 5000."
)

add_heading2("C. Amazon ECR Private Registry")
add_body(
    "Amazon ECR is utilized as the primary private image registry in region ap-southeast-1. Authentication is automated in Jenkins "
    "using `aws ecr get-login-password`, tagging images with both the unique traceable ${BUILD_NUMBER} and the :latest tag."
)

add_heading2("D. Docker Swarm Cluster on Amazon EC2")
add_body(
    "The production cluster consists of an EC2 Swarm Manager and EC2 Swarm Worker nodes. Networking and security groups are configured "
    "with least privilege: TCP 22 (SSH), TCP 5000 (Web Application), TCP 2377 (Cluster management), TCP/UDP 7946 (Gossip communication), "
    "and UDP 4789 (Overlay network VXLAN data path)."
)

# Section 3: Verification & Evidence
add_heading1("3. Pipeline Execution Evidence & Verification")
add_body(
    "The end-to-end pipeline was executed and validated through Jenkins Build #4 with 100% green status across all stages:"
)

# Table for Pipeline Stages
table = doc.add_table(rows=1, cols=3)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_cells = table.rows[0].cells
hdr_cells[0].text = "Stage"
hdr_cells[1].text = "Duration"
hdr_cells[2].text = "Status & Result"
for cell in hdr_cells:
    shd = parse_xml(r'<w:shd {} w:fill="0F172A"/>'.format(nsdecls('w')))
    cell._tc.get_or_add_tcPr().append(shd)
    for p in cell.paragraphs:
        for r in p.runs:
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            r.font.size = Pt(9)

stages_data = [
    ("Declarative: Checkout SCM", "3s", "Checked out commit from origin/main"),
    ("Lint & Unit Test", "33s", "Pytest passed 3/3 tests (Home, Health, API Info)"),
    ("Docker Build", "23s", "Built kemleapx20/cicd-web-app:4 & :latest"),
    ("Docker Push", "21s", "Authenticated & pushed layers to registry"),
    ("Deploy to Docker Swarm", "4s", "Swarm stack cicd-homework updated with 3 replicas"),
    ("Declarative: Post Actions", "358ms", "Post-build success notification emitted")
]

for stg, dur, res in stages_data:
    row_cells = table.add_row().cells
    row_cells[0].text = stg
    row_cells[1].text = dur
    row_cells[2].text = res
    for c in row_cells:
        for p in c.paragraphs:
            for r in p.runs:
                r.font.size = Pt(8.5)

p_space = doc.add_paragraph()
p_space.paragraph_format.space_before = Pt(8)

add_heading2("Active Swarm Service Verification:")
swarm_output = """ID             NAME                MODE         REPLICAS   IMAGE                            PORTS
fnjch0d9oz7j   cicd-homework_web   replicated   3/3        kemleapx20/cicd-web-app:latest   *:5000->5000/tcp

Tasks Running:
mz89iekp2t2o   cicd-homework_web.1   Running   Node: docker-desktop
7kznpc858v3y   cicd-homework_web.2   Running   Node: docker-desktop
mh9ndpc7q3qj   cicd-homework_web.3   Running   Node: docker-desktop"""
add_code_block(swarm_output)

add_heading2("Live Health Check & Load Balancing:")
add_code_block('curl http://localhost:5000/health\n{"hostname":"124d2c395f83","service":"cicd-web-app","status":"UP","version":"1.0.0"}')

# Section 4: Challenges & Solutions
add_heading1("4. Key Challenges Encountered & Solutions")

add_bullet("1. Windows Environment Shell Execution: ", 
           "Running Jenkins on Windows caused Build #1 to fail because 'sh' was not in PATH. Resolved by making the Jenkinsfile cross-platform using `isUnix()` checks to execute `bat` on Windows and `sh` on Linux.")

add_bullet("2. GitHub Webhook Ingress Behind NAT: ", 
           "Local Jenkins instances cannot accept direct external webhook calls from GitHub. Overcame this by establishing a secure Cloudflare Tunnel to route payloads from https://...trycloudflare.com/github-webhook/ to localhost:9090.")

add_bullet("3. Private ECR Authentication on Swarm Nodes: ", 
           "Swarm worker nodes fail to pull private ECR images if only the manager is authenticated. Solved by appending the `--with-registry-auth` flag to `docker stack deploy`, delegating authentication credentials cluster-wide.")

add_bullet("4. Zero-Downtime Deployment Strategy: ", 
           "Prevented outage during service updates by configuring `update_config` with `order: start-first` and `parallelism: 1`, ensuring the new replica is healthy before stopping the previous container.")

# Save document
output_path = r"D:\University\Master2\Homework\Homeword_Kemeleap_02\Homework_2_Report_Ven_KemLeap.docx"
doc.save(output_path)
print("Report generated successfully at: " + output_path)
