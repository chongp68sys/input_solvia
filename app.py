import streamlit as st
from auth import authenticate_user
from solvia_caller import solvia_caller
from conversations import display_conversations

if authenticate_user():
    st.sidebar.title("📞 Dialler")
    solvia_caller()

    # Get agent_id from user input
    agent_id = st.sidebar.text_input("Agent ID", "default_agent_id")

    # Pass agent_id to display_conversations
    display_conversations(agent_id)
else:
    st.stop()