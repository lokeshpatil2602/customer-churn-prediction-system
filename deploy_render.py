"""
Render deployment script for Customer Churn Prediction System.
Creates backend (Flask) and frontend (Streamlit) as two web services.
"""

import urllib.request
import urllib.error
import json
import time

API_KEY   = "rnd_RlzMGBHkr9X75xplhmy78IQw5mJL"
OWNER_ID  = "tea-d8vte937uimc738s1r10"
REPO      = "https://github.com/lokeshpatil2602/customer-churn-prediction-system"
BASE_URL  = "https://api.render.com/v1"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


def api(method, path, payload=None):
    url = BASE_URL + path
    data = json.dumps(payload).encode() if payload else None
    req  = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return e.code, body


def create_service(name, root_dir, build_cmd, start_cmd, env_vars):
    payload = {
        "autoDeploy": "yes",
        "branch": "main",
        "name": name,
        "ownerId": OWNER_ID,
        "repo": REPO,
        "rootDir": root_dir,
        "type": "web_service",
        "serviceDetails": {
            "runtime": "python",
            "buildCommand": build_cmd,
            "startCommand": start_cmd,
            "envSpecificDetails": {
                "pythonVersion": "3.12.3"
            }
        },
        "envVars": [{"key": k, "value": v} for k, v in env_vars.items()]
    }
    return api("POST", "/services", payload)


# ── 1. Deploy Backend ───────────────────────────────────────────────
print("=" * 55)
print("Deploying churn-backend (Flask API)...")
print("=" * 55)

status, result = create_service(
    name      = "churn-backend",
    root_dir  = "backend",
    build_cmd = "pip install -r requirements.txt",
    start_cmd = "gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120",
    env_vars  = {
        "FLASK_ENV":      "production",
        "PYTHON_VERSION": "3.12.3",
    }
)

print(f"Status: {status}")
if status == 201:
    svc = result.get("service", result)
    backend_id  = svc.get("id", "")
    backend_url = f"https://{svc.get('slug', 'churn-backend')}.onrender.com"
    print(f"Backend service created!")
    print(f"  ID  : {backend_id}")
    print(f"  URL : {backend_url}")
else:
    print("Response:", result)
    # Try to extract URL from error or existing service
    backend_url = "https://churn-backend.onrender.com"
    backend_id  = ""

# ── 2. Deploy Frontend ──────────────────────────────────────────────
print()
print("=" * 55)
print("Deploying churn-frontend (Streamlit)...")
print("=" * 55)

status2, result2 = create_service(
    name      = "churn-frontend",
    root_dir  = "frontend",
    build_cmd = "pip install -r requirements.txt",
    start_cmd = "streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true",
    env_vars  = {
        "BACKEND_URL":    backend_url,
        "PYTHON_VERSION": "3.12.3",
    }
)

print(f"Status: {status2}")
if status2 == 201:
    svc2 = result2.get("service", result2)
    frontend_id  = svc2.get("id", "")
    frontend_url = f"https://{svc2.get('slug', 'churn-frontend')}.onrender.com"
    print(f"Frontend service created!")
    print(f"  ID  : {frontend_id}")
    print(f"  URL : {frontend_url}")
else:
    print("Response:", result2)
    frontend_url = "https://churn-frontend.onrender.com"

# ── 3. Summary ──────────────────────────────────────────────────────
print()
print("=" * 55)
print("DEPLOYMENT TRIGGERED")
print("=" * 55)
print(f"Backend  : {backend_url}")
print(f"Frontend : {frontend_url}")
print()
print("Build takes ~3-5 minutes. Check progress at:")
print("https://dashboard.render.com")
print()
print("Once live, open the Frontend URL in your browser.")
