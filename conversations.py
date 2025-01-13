import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

BASE_URL = "https://api.elevenlabs.io/v1"
ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]

def fetch_conversations(agent_id):
    """Fetches all conversations for a given agent_id."""
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    url = f"{BASE_URL}/convai/conversations?agent_id={agent_id}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching conversations: {e}")
        return None

def fetch_conversation_details(conversation_id: str):
    """Fetches the detailed info for a specific conversation from ElevenLabs."""
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    url = f"{BASE_URL}/convai/conversations/{conversation_id}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()  # Contains detailed conversation info
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching conversation {conversation_id}: {e}")
        return None

def display_conversations(agent_id):
    """Displays the conversations with summary and detail view."""
    st_autorefresh(interval=30000, key="conversation_refresh")
    if st.button("Fetch Conversations", key="fetch_conversations_button"):
        data = fetch_conversations(agent_id)
        if data and "conversations" in data:
            conversations = data["conversations"]

            if not conversations:
                st.warning("No conversations returned.")
            else:
                st.subheader("Last 10 Conversations")

                for i, convo in enumerate(conversations[:10], start=1):
                    conversation_id = convo.get("conversation_id", "N/A")
                    agent_name = convo.get("agent_name", "N/A")
                    call_duration_secs = convo.get("call_duration_secs", "N/A")
                    message_count = convo.get("message_count", "N/A")
                    call_successful = convo.get("call_successful", "N/A")

                    st.write(
                        f"**No.{i} — Agent: {agent_name}**\n"
                        f"- **Conversation ID:** {conversation_id}\n"
                        f"- **Duration:** {call_duration_secs} seconds\n"
                        f"- **Messages:** {message_count}\n"
                        f"- **Successful:** {'Yes' if call_successful else 'No'}"
                    )

                    with st.expander("View Details", expanded=False):
                        details = fetch_conversation_details(conversation_id)
                        if details:
                            st.json(details)
                        else:
                            st.write("No additional details available for this conversation.")
        else:
            st.warning("No conversations found or unable to retrieve data.")