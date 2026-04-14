# assets.py
import base64
import os
import streamlit as st

@st.cache_data
def get_bg_base64(file_path="bg_tile.png"):
    try:
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    except Exception:
        pass
    return ""