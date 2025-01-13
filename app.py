import streamlit as st
from solvia_caller import solvia_caller
from conversations import display_conversations


st.sidebar.title("📞 Dialler")
agent_id = solvia_caller()  # Get the agent_id from the caller function

    # Pass the agent_id to display_conversations
if agent_id:  # Ensure agent_id is not empty
        display_conversations(agent_id)
