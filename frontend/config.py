"""
Centralised backend URL config.
Priority:
  1. Streamlit secrets (st.secrets) — used on Streamlit Cloud
  2. BACKEND_URL environment variable — used on Railway / Docker
  3. Localhost fallback — used for local development
"""
import os

def get_backend_url():
    # Try Streamlit secrets first (Streamlit Cloud deployment)
    try:
        import streamlit as st
        return st.secrets["BACKEND_URL"]
    except Exception:
        pass
    # Fall back to environment variable or localhost
    return os.environ.get("BACKEND_URL", "http://localhost:5000")

BACKEND_URL = get_backend_url()
