"""
Local Web Dashboard for OpenCode Test Project.

A Flask-based dashboard that displays real-time system resource usage
(CPU, RAM, disk) and Ollama server status. Serves a web UI for
monitoring the local testing environment.

Dependencies: Flask, psutil
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime
from flask import Flask, render_template_string, jsonify

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_API_PATH = "/api/tags"

app = Flask(__name__)


# ---------------------------------------------------------------------------
# System Resource Monitoring
# ---------------------------------------------------------------------------
def get_system_metrics() -> dict:
    """Collect CPU, RAM, and disk system metrics from the system."""
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "cpu": {},
        "memory": {},
        "disk": {},
    }

    # --- CPU Usage ---
    try:
        import psutil

        cpu_percent = psutil.cpu_percent(interval=1)
        metrics["cpu"]["usage_percent"] = round(cpu_percent, 2)
        metrics["cpu"]["core_count"] = psutil.cpu_count(logical=True)
        metrics["cpu"]["total_cores"] = psutil.cpu_count(logical=False)
    except Exception as exc:
        metrics["cpu"]["error"] = f"CPU monitoring failed: {str(exc)}"

    # --- Memory Usage ---
    try:
        mem = psutil.virtual_memory()
        metrics["memory"]["total_gb"] = round(mem.total / (1024 ** 3), 2)
        metrics["memory"]["used_gb"] = round(mem.used / (1024 ** 3), 2)
        metrics["memory"]["free_gb"] = round(mem.free / (1024 ** 3), 2)
        metrics["memory"]["usage_percent"] = round(mem.percent, 2)
    except Exception as exc:
        metrics["memory"]["error"] = f"Memory monitoring failed: {str(exc)}"

    # --- Disk Usage ---
    try:
        mount = psutil.disk_usage()
        metrics["disk"]["total_gb"] = round(mount.total / (1024 ** 3), 2)
        metrics["disk"]["used_gb"] = round(mount.used / (1024 ** 3), 2)
        metrics["disk"]["free_gb"] = round(mount.free / (1024 ** 3), 2)
        metrics["disk"]["usage_percent"] = round(mount.percent, 2)
    except Exception as exc:
        metrics["disk"]["error"] = f"Disk monitoring failed: {str(exc)}"

    return metrics


def check_ollama_status() -> dict:
    """Check the health and availability of the local Ollama server."""
    result = {
        "host": OLLAMA_HOST,
        "status": "unknown",
        "details": "",
        "reachable": False,
        "error": "",
    }

    try:
        url = f"{OLLAMA_HOST}{OLLAMA_API_PATH}"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            result["reachable"] = True
            result["status"] = "running"
            result["details"] = "Ollama server is reachable and responding."
            result["models"] = data.get("models", [])
    except urllib.error.HTTPError as exc:
        result["reachable"] = False
        result["status"] = "error"
        result["error"] = f"HTTP {exc.code}"
        result["details"] = f"Ollama server returned HTTP {exc.code}."
    except Exception as exc:
        result["reachable"] = False
        result["status"] = "error"
        result["error"] = str(exc)
        result["details"] = f"Ollama server unreachable: {str(exc)}"

    return result


# ---------------------------------------------------------------------------
# HTML Template
# ---------------------------------------------------------------------------
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local Web Dashboard — OpenCode Test Project</title>
    <style>
        body {
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
            background: #f5f7fa;
            color: #2c3e50;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.5rem;
        }
        .section {
            background: white;
            border-radius: 8px;
            padding: 1.2rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        .section h2 {
            color: #3498db;
            margin-top: 0;
        }
        .metric-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }
        .metric-card {
            background: #ecf0f1;
            border-radius: 6px;
            padding: 0.9rem;
            border-left: 4px solid #3498db;
        }
        .metric-card.warning { border-left-color: #e74c3c; }
        .metric-card.error { border-left-color: #c0392b; }
        .value {
            font-size: 1.6rem;
            font-weight: bold;
            color: #2c3e50;
        }
        .label {
            font-size: 0.85rem;
            color: #7f8c8d;
            margin-bottom: 0.2rem;
        }
        .status-running { color: #27ae60; }
        .status-error { color: #c0392b; }
        .status-unknown { color: #7f8c8d; }
        .details {
            font-size: 0.8rem;
            color: #7f8c8d;
            margin-top: 0.5rem;
            white-space: pre-wrap;
        }
        .timestamp {
            font-size: 0.75rem;
            color: #95a5a6;
            margin-bottom: 0.8rem;
        }
    </style>
</head>
<body>
    <h1>Local Web Dashboard — OpenCode Test Project</h1>
    <p class="timestamp">Generated: {{ timestamp }}</p>

    <div class="section">
        <h2>System Resources</h2>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="label">CPU Usage</div>
                <div class="value">{{ cpu.usage_percent }}%</div>
                <div class="label">Cores: {{ cpu.core_count }} / {{ cpu.total_cores }}</div>
            </div>
            <div class="metric-card">
                <div class="label">Memory Usage</div>
                <div class="value">{{ memory.usage_percent }}%</div>
                <div class="label">Used: {{ memory.used_gb }} GB / {{ memory.total_gb }} GB</div>
            </div>
            <div class="metric-card">
                <div class="label">Disk Usage</div>
                <div class="value">{{ disk.usage_percent }}%</div>
                <div class="label">Used: {{ disk.used_gb }} GB / {{ disk.total_gb }} GB</div>
            </div>
        </div>
        {% if cpu.error %}<div class="metric-card error">{{ cpu.error }}</div>{% endif %}
        {% if memory.error %}<div class="metric-card error">{{ memory.error }}</div>{% endif %}
        {% if disk.error %}<div class="metric-card error">{{ disk.error }}</div>{% endif %}
    </div>

    <div class="section">
        <h2>Ollama Server Status</h2>
        <div class="metric-card {% if ollama.status == 'running' %}running{% elif ollama.status == 'error' %}error{% else %}unknown{% endif %}">
            <div class="value">{{ ollama.status }}</div>
            <div class="label">Host: {{ ollama.host }}</div>
            {% if ollama.reachable %}
                <div class="details">Ollama server is reachable and responding. Models: {{ ollama.details }}</div>
            {% else %}
                <div class="details">{% if ollama.error %}{{ ollama.error }}{% else %}Ollama server unreachable.{% endif %}</div>
            {% endif %}
        </div>
    </div>

    <div class="section">
        <h2>Quick Actions</h2>
        <p>This dashboard provides real-time monitoring of system resources and the local Ollama server. Use it to verify that the testing environment is operating correctly during autonomous coding tasks.</p>
    </div>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def dashboard():
    """Render the main dashboard page with live system metrics."""
    system_metrics = get_system_metrics()
    ollama_status = check_ollama_status()
    system_metrics["ollama"] = ollama_status
    return render_template_string(HTML_PAGE, **system_metrics)


@app.route("/api/metrics", methods=["GET"])
def api_metrics():
    """JSON endpoint returning current system and Ollama metrics."""
    system_metrics = get_system_metrics()
    system_metrics["ollama"] = check_ollama_status()
    return jsonify(system_metrics)


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint used for validation tests."""
    system_metrics = get_system_metrics()
    ollama_status = check_ollama_status()
    system_metrics["ollama"] = ollama_status
    system_metrics["status"] = "ok"
    return jsonify(system_metrics)


@app.route("/test", methods=["GET"])
def run_validation():
    """Run a validation test that checks all dashboard components."""
    validation_results = []

    # Test 1: System metrics collection
    try:
        metrics = get_system_metrics()
        validation_results.append({
            "test": "System metrics collection",
            "status": "passed",
            "details": f"Collected CPU, memory, and disk metrics successfully.",
            "error": ""
        })
    except Exception as exc:
        validation_results.append({
            "test": "System metrics collection",
            "status": "failed",
            "details": "",
            "error": str(exc)
        })

    # Test 2: Ollama server status check
    try:
        ollama = check_ollama_status()
        validation_results.append({
            "test": "Ollama server status check",
            "status": "passed" if ollama["reachable"] else "failed",
            "details": f"Status: {ollama['status']}, reachable: {ollama['reachable']}",
            "error": ollama.get("error", "") if not ollama["reachable"] else ""
        })
    except Exception as exc:
        validation_results.append({
            "test": "Ollama server status check",
            "status": "failed",
            "details": "",
            "error": str(exc)
        })

    # Test 3: API endpoints accessibility
    try:
        for path in ["/", "/api/metrics", "/health"]:
            with app.test_client():
                response = app.test_client().get(path)
                status_code = int(response.status_code)
                validation_results.append({
                    "test": f"API endpoint {path}",
                    "status": "passed" if status_code == 200 else "failed",
                    "details": f"HTTP {status_code}",
                    "error": "" if status_code == 200 else f"HTTP {status_code}"
                })
    except Exception as exc:
        validation_results.append({
            "test": "API endpoint accessibility",
            "status": "failed",
            "details": "",
            "error": str(exc)
        })

    overall_status = "all_passed" if all(r["status"] == "passed" for r in validation_results) else "has_errors"
    return {
        "overall_status": overall_status,
        "timestamp": datetime.now().isoformat(),
        "results": validation_results,
        "message": "Validation completed successfully." if overall_status == "all_passed" else "Validation completed with errors."
    }


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Allow running in testing/validation mode for automated checks.
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        with app.app_context():
            result = run_validation()
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["overall_status"] == "all_passed" else 1)

    # Start the web server.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
