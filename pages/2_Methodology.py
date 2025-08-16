import streamlit as st

st.set_page_config(
    page_title="Methodology",
    page_icon="🧠",
)

st.title("Methodology")

st.markdown("""
The **Test Account Matcher** uses a structured, rule-based approach to help users find suitable test accounts based on their input profile.

---

### 🧩 Matching Logic

1. **User Input**  
   The user describes the required member profile — including attributes like role, region, permissions, and other criteria.

2. **CSV Lookup**  
   The app scans the uploaded test account CSV to find exact matches based on the specified attributes.

3. **Fallback Suggestions**  
   If no exact match is found, the app suggests the closest available test accounts using partial or fuzzy matching.

4. **Patch Instructions**  
   If no suitable accounts exist, the app provides instructions to notify the ITPM team so they can patch or provision a new test account.

---

### 📐 Matching Criteria

The matcher compares fields such as:
- Role (e.g. Advisor, Admin)
- Region or Market
- Access Level or Permissions
- Any custom tags or flags defined in the CSV

---

### 🔄 Reproducibility & Collaboration

- Matching logic is version-controlled via GitHub  
- Dependencies are tracked in `requirements.txt`  
- Team members can sync updates and contribute via pull requests

---

This methodology ensures consistent, transparent, and scalable test account management for GenAI assistant testing.
""")
