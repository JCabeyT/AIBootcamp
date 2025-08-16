import streamlit as st
import pandas as pd
import numpy as np
import openai
import os
from datetime import datetime

st.set_page_config(
    page_title="Home", 
    page_icon="👋",
)

# --- Basic Authentication ---
USERS = {
    "admin": "admin",
    "jeremy": "letmein",
    "alycia": "password"
}

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''

def login():
    st.title('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        if username in USERS and USERS[username] == password:
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error('Invalid username or password')

def logout():
    st.session_state['authenticated'] = False
    st.session_state['username'] = ''
    st.rerun()

if not st.session_state['authenticated']:
    login()
    st.stop()
else:
    st.sidebar.write(f"Logged in as: {st.session_state['username']}")
    if st.sidebar.button('Logout'):
        logout()

    st.title('AI Bootcamp')
    st.write("""
    Welcome to the **Test Account Matcher** tool.
    
    To get started, please describe the profile of the member you need — including attributes like role, region, permissions, or any other relevant criteria.
    
    🔍 If a matching test account exists in the uploaded CSV, the assistant will return the exact match.
    
    🤔 If no exact match is found, the assistant will suggest the closest available test accounts based on similarity.
    
    📩 If none of the suggestions are suitable, follow the provided instructions to notify the ITPM team so they can patch or provision a new test account.
    
    This tool helps streamline GenAI assistant testing by ensuring you always have the right test data at your fingertips.
    """)

    # --- GenAI Chat Interface ---
    # Session state for chat and settings
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    DEFAULT_OPENAI_API_KEY = "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"
    if 'openai_api_key' not in st.session_state or not st.session_state['openai_api_key']:
        st.session_state['openai_api_key'] = DEFAULT_OPENAI_API_KEY
    if 'show_api_key_input' not in st.session_state:
        st.session_state['show_api_key_input'] = False
    if 'is_loading' not in st.session_state:
        st.session_state['is_loading'] = False

    # Sidebar for settings
    st.sidebar.header("Settings")
    if st.sidebar.button("Set/Change OpenAI API Key"):
        st.session_state['show_api_key_input'] = not st.session_state['show_api_key_input']
    if 'api_key_confirmed' not in st.session_state:
        st.session_state['api_key_confirmed'] = False

    if st.session_state['show_api_key_input']:
        api_key = st.sidebar.text_input("OpenAI API Key", type="password", value=st.session_state['openai_api_key'])
        if st.sidebar.button("Save API Key"):
            if api_key:
                st.session_state['openai_api_key'] = api_key
                st.session_state['api_key_confirmed'] = True
            else:
                st.session_state['api_key_confirmed'] = False
        if st.session_state['api_key_confirmed']:
            st.sidebar.success("OpenAI API Key accepted!")
    else:
        api_key = st.session_state['openai_api_key']

tab3 = st.container()
    
# --- Test Account Matcher Tab ---
with tab3:
    st.header("Test Account Matcher")

    # Sidebar CSV uploader
    st.sidebar.subheader("Upload Test Accounts CSV")
    accounts_file = st.sidebar.file_uploader("Upload CSV", type=["csv"], key="accounts_uploader")

    if accounts_file:
        try:
            accounts_df = pd.read_csv(accounts_file)
            required_cols = {'mbr_num', 'BRS', 'FRS', 'post_PEA', 'PBA', 'citizenship'}
            if not required_cols.issubset(set(accounts_df.columns)):
                st.sidebar.error("Uploaded CSV is missing required columns.")
            else:
                st.session_state['accounts_df'] = accounts_df
                st.sidebar.success("Test accounts loaded!")
        except Exception as e:
            st.sidebar.error(f"Error reading file: {e}")

    if 'accounts_df' in st.session_state:
        st.expander("Preview Uploaded Test Accounts").dataframe(st.session_state['accounts_df'])

        # Input form
        with st.form("account_requirements_form"):
            brs = st.selectbox("BRS", ["Y", "N"])
            frs = st.selectbox("FRS", ["Y", "N"])
            post_pea = st.selectbox("post_PEA", ["Y", "N"])
            pba = st.selectbox("PBA", ["paynow", "other"])
            citizenship = st.selectbox("Citizenship", ["SG", "non-SG"])
            submitted = st.form_submit_button("Find Matching Accounts")

        if submitted:
            df = st.session_state['accounts_df']

            # Exact match
            exact_matches = df[
                (df['BRS'] == brs) &
                (df['FRS'] == frs) &
                (df['post_PEA'] == post_pea) &
                (df['PBA'] == pba) &
                (df['citizenship'] == citizenship)
            ]

            if not exact_matches.empty:
                st.success("✅ Exact match found. No patching required.")
                st.write("Matching test accounts:")
                st.dataframe(exact_matches[['mbr_num']])
            else:
                # Closest match logic
                def score_row(row):
                    score = 0
                    diffs = []
                    if row['BRS'] != brs: diffs.append('BRS')
                    if row['FRS'] != frs: diffs.append('FRS')
                    if row['post_PEA'] != post_pea: diffs.append('post_PEA')
                    if row['PBA'] != pba: diffs.append('PBA')
                    if row['citizenship'] != citizenship: diffs.append('citizenship')
                    score = len(diffs)
                    return pd.Series({'score': score, 'diffs': diffs})

                scored_df = df.copy()
                scored_df[['score', 'diffs']] = df.apply(score_row, axis=1)
                closest_matches = scored_df.sort_values('score').head(3)

                st.warning("⚠️ No exact match found.")
                st.write("Closest test accounts:")
                st.dataframe(closest_matches[['mbr_num', 'diffs']])

                all_diffs = set(field for diff_list in closest_matches['diffs'] for field in diff_list)
                st.info(f"Please approach ITPM to patch the field(s): {', '.join(all_diffs)}")
    else:
        st.info("Please upload a test accounts CSV to begin.")
    
