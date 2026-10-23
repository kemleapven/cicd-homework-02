import os
import socket
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Basic configuration
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_ENV = os.getenv("APP_ENV", "development")
STUDENT_NAME = os.getenv("STUDENT_NAME", "Ven KemLeap")
STUDENT_ID = os.getenv("STUDENT_ID", "Master - Cloud & DevOps")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CI/CD Homework 02 - {{ student_name }}</title>
    <style>
        :root {
            --bg-primary: #0f172a;
            --bg-card: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent: #38bdf8;
            --accent-hover: #0284c7;
            --success: #22c55e;
            --border: #334155;
        }
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            max-width: 650px;
            width: 100%;
            padding: 36px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
        }
        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 16px;
        }
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(34, 197, 94, 0.15);
            color: var(--success);
            padding: 6px 12px;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .badge::before {
            content: "";
            width: 8px;
            height: 8px;
            background: var(--success);
            border-radius: 50%;
            display: inline-block;
        }
        h1 {
            font-size: 1.75rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 8px;
        }
        .subtitle {
            color: var(--text-secondary);
            font-size: 1rem;
            margin-bottom: 24px;
            line-height: 1.5;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-bottom: 24px;
        }
        .info-card {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 14px 16px;
        }
        .info-label {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
            margin-bottom: 6px;
        }
        .info-value {
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--accent);
            word-break: break-all;
        }
        .actions {
            display: flex;
            gap: 12px;
            margin-top: 24px;
        }
        .btn {
            flex: 1;
            text-align: center;
            background-color: var(--accent);
            color: #0f172a;
            padding: 10px 18px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
            transition: background 0.2s;
        }
        .btn:hover {
            background-color: var(--accent-hover);
            color: #ffffff;
        }
        .btn-outline {
            background-color: transparent;
            color: var(--text-primary);
            border: 1px solid var(--border);
        }
        .btn-outline:hover {
            background-color: rgba(255, 255, 255, 0.05);
            color: var(--accent);
        }
        footer {
            margin-top: 24px;
            text-align: center;
            font-size: 0.8rem;
            color: var(--text-secondary);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1>CI/CD Web Application</h1>
                <p style="color: var(--text-secondary); font-size: 0.85rem;">Continuous Integration & Deployment</p>
            </div>
            <div class="badge">Healthy & Running</div>
        </div>

        <p class="subtitle">
            This microservice is automated via <strong>Jenkins CI/CD</strong>, containerized with <strong>Docker</strong>, and orchestrated using <strong>Docker Swarm</strong>.
        </p>

        <div class="grid">
            <div class="info-card">
                <div class="info-label">Student / Author</div>
                <div class="info-value">{{ student_name }}</div>
            </div>
            <div class="info-card">
                <div class="info-label">Program</div>
                <div class="info-value">{{ student_id }}</div>
            </div>
            <div class="info-card">
                <div class="info-label">Container Replica / Host</div>
                <div class="info-value">{{ hostname }}</div>
            </div>
            <div class="info-card">
                <div class="info-label">Environment / Version</div>
                <div class="info-value">{{ app_env }} | v{{ app_version }}</div>
            </div>
        </div>

        <div class="actions">
            <a href="/health" class="btn">Health Check Endpoint</a>
            <a href="/api/info" class="btn btn-outline">API Info (JSON)</a>
        </div>

        <footer>
            Master DevOps Lab &bull; Refreshed at {{ current_time }}
        </footer>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    hostname = socket.gethostname()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template_string(
        HTML_TEMPLATE,
        student_name=STUDENT_NAME,
        student_id=STUDENT_ID,
        hostname=hostname,
        app_env=APP_ENV,
        app_version=APP_VERSION,
        current_time=current_time
    )

@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "service": "cicd-web-app",
        "version": APP_VERSION,
        "hostname": socket.gethostname(),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

@app.route("/api/info")
def api_info():
    return jsonify({
        "name": "CI/CD Demo Application",
        "student": STUDENT_NAME,
        "program": STUDENT_ID,
        "version": APP_VERSION,
        "environment": APP_ENV,
        "hostname": socket.gethostname()
    }), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
