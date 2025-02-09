import streamlit as st

def Navbar():
    with st.sidebar:
        st.page_link("streamlit_app.py", label="Mineability Calculator", icon="⛏️")
        st.page_link("pages/dataset_visualization.py", label="Dataset Visualization", icon="📊")