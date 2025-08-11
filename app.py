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
    st.write("Hi")

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

    st.header("Chat with GenAI (OpenAI)")

    # Clear chat button
    if st.button("🧹 Clear Chat"):
        st.session_state['chat_history'] = []

    # Native chat history display using Streamlit containers
    with st.container():
        for chat in st.session_state['chat_history']:
            st.markdown(f"**You:** {chat['user']}  ", unsafe_allow_html=False)
            st.markdown(f"<span style='font-size:0.8em;color:#888;'>{chat['timestamp']}</span>", unsafe_allow_html=True)
            st.markdown(f"**GenAI:** {chat['ai']}  ", unsafe_allow_html=False)
            st.markdown(f"<span style='font-size:0.8em;color:#888;'>{chat['timestamp']}</span>", unsafe_allow_html=True)

    # Chat input area directly below chat history (not fixed, but always at bottom of chat section)
    user_message = st.text_area("Your message", key="user_message", height=60)
    send_col, loading_col = st.columns([1, 5])
    send_clicked = send_col.button("Send")

    # File uploader for CSV and Excel files (now below chat input)
    uploaded_file = st.file_uploader("Upload CSV or Excel file for analysis", type=["csv", "xlsx"])
    file_data_str = None
    send_file_clicked = False
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.write("Preview of uploaded data:")
            st.dataframe(df)
            file_data_str = df.to_csv(index=False)
            send_file_clicked = st.button("Send file to GenAI")
        except Exception as e:
            st.error(f"Error reading file: {e}")

    # (Spinner removed as requested)

    # Handle sending message
    if send_clicked and user_message.strip():
        if not api_key:
            st.error("Please enter your OpenAI API key in the sidebar.")
        else:
            openai.api_key = api_key
            st.session_state['is_loading'] = True
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": "You are a helpful assistant."}] +
                             [{"role": "user", "content": m['user']} for m in st.session_state['chat_history']] +
                             [{"role": "user", "content": user_message}]
                )
                ai_reply = response.choices[0].message.content
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                st.session_state['chat_history'].append({
                    "user": user_message,
                    "ai": ai_reply,
                    "timestamp": timestamp
                })
                st.session_state['is_loading'] = False
                st.rerun()
            except Exception as e:
                st.session_state['is_loading'] = False
                st.error(f"Error: {e}")

    # Handle sending file to GenAI
    if send_file_clicked and file_data_str:
        if not api_key:
            st.error("Please enter your OpenAI API key in the sidebar.")
        else:
            openai.api_key = api_key
            st.session_state['is_loading'] = True
            try:
                file_prompt = (
                    f"The following is the content of a spreadsheet file uploaded by the user. "
                    f"Please analyze, summarize, or provide insights as appropriate.\n\n"
                    f"{file_data_str[:4000]}"
                )
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": "You are a helpful assistant."}] +
                             [{"role": "user", "content": m['user']} for m in st.session_state['chat_history']] +
                             [{"role": "user", "content": file_prompt}]
                )
                ai_reply = response.choices[0].message.content
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                st.session_state['chat_history'].append({
                    "user": "[Sent spreadsheet data]",
                    "ai": ai_reply,
                    "timestamp": timestamp
                })
                st.session_state['is_loading'] = False
                st.rerun()
            except Exception as e:
                st.session_state['is_loading'] = False
                st.error(f"Error: {e}")