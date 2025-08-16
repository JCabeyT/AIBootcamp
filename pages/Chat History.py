selected_account = st.selectbox("Choose a test account:", options)

if selected_account and selected_account != "Select an account":
    st.session_state.chat_history.append({
        "selection": selected_account,
        "source": "Test Account Matcher",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    st.experimental_rerun()
