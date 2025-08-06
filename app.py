
import streamlit as st
import pandas as pd
import numpy as np


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