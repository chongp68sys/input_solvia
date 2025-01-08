import streamlit as st
from auth import authenticate_user
from solvia_caller import solvia_caller
from conversations import display_conversations

if authenticate_user():
    # Sidebar for Caller functionality
    st.sidebar.title("📞 Dialler")
    solvia_caller()

    # Main section for Conversations
    st.title("📞 Solvia Lead Caller")
    display_conversations()
else:
    st.stop() 