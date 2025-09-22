import streamlit as st
from ui_components import render_home, render_about, render_manual, render_jira_placeholder



st.set_page_config(page_title="User Story Extractor", page_icon="📄", layout="wide")

st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Go to:",
    ["🏠 Main", "ℹ️ About", "📘 User Manual", "🚀 Jira Integration"],
    index=0
)

if section == "🏠 Main":
    render_home()
elif section == "ℹ️ About":
    render_about()
elif section == "📘 User Manual":
    render_manual()
elif section == "🚀 Jira Integration":
    render_jira_placeholder()
