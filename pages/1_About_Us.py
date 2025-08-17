import streamlit as st

st.set_page_config(
    page_title="About Us",
    page_icon="👋",
)

st.title("About Us")

st.markdown("""
Welcome to the **Test Account Matcher** — a smart tool designed to support GenAI testing workflows.

This app helps teams efficiently match test accounts to user-defined profiles, ensuring smoother testing and faster iteration.

---

### 👩‍💻 Built By
- Alycia & Jeremy  
- Powered by Python, Streamlit, and GenAI logic

### 🧰 Key Features
- Match test accounts based on role, region, and permissions  
- Suggest similar accounts when no exact match is found  
- Provide instructions to notify ITPM for patching or provisioning

### 📬 Feedback & Support
If you have suggestions or run into issues, please contact your ITPM lead or project coordinator.

---
""")
