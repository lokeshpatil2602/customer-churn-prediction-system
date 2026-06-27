"""
Centralised configuration for the Streamlit frontend.
Set BACKEND_URL environment variable in production to point at the deployed
Flask API (e.g. https://your-app.onrender.com).
"""

import os

# Backend API base URL — falls back to localhost for local development
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:5000")
