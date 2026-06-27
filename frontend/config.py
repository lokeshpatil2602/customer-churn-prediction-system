"""
Centralised configuration for the Streamlit frontend.
Set BACKEND_URL environment variable in production to point at the deployed
Flask API (e.g. https://your-app.onrender.com).
"""

import os

# Backend API base URL
# - Locally:     http://localhost:5000
# - On Render:   set BACKEND_URL env var to https://churn-backend.onrender.com
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:5000")
