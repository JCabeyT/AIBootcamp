import streamlit as st

st.set_page_config(
    page_title="Chat History",
    page_icon="💬",
)

st.title("Chat History")

if "chat_history" not in st.session_state or not st.session_state.chat_history:
    st.info("No chat history yet.")
else:
    for chat in st.session_state.chat_history:
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"<span style='font-size:0.8em;color:#888;'>{chat['timestamp']}</span>", unsafe_allow_html=True)
        st.markdown(f"**GenAI:** {chat['bot']}")
        st.markdown(f"<span style='font-size:0.8em;color:#888;'>{chat['timestamp']}</span>", unsafe_allow_html=True)
        st.markdown("---")

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.success("Chat history cleared.")
