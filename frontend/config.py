"""
Centralised backend URL config.
Priority:
  1. BACKEND_URL environment variable (Railway / Docker / Streamlit Cloud secrets injected as env)
  2. Localhost fallback for local development
"""
import os

# Streamlit Cloud injects secrets as environment variables automatically.
# So just reading os.environ is sufficient for all platforms.
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:5000")
