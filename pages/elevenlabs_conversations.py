import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests

# Set Streamlit page config
st.set_page_config(page_title="Conversations", layout="wide")

st.title("🗣️ Conversations with Expanding Table")

# Set the interval to 10000 milliseconds (10 seconds)
st_autorefresh(interval=10000, key="data_refresh")

# Replace with your actual ElevenLabs API key or use st.secrets for security
ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
BASE_URL = "https://api.elevenlabs.io/v1"

headers = {
    "xi-api-key": ELEVENLABS_API_KEY,
    "Content-Type": "application/json"
}

def fetch_conversations():
    """Fetches all conversations from ElevenLabs and returns the JSON response."""
    url = f"{BASE_URL}/convai/conversations?agent_id=wkf3emR8JrlVMWl93pu7"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()  # Should return a dict with a 'conversations' key
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching conversations: {e}")
        return None

def fetch_conversation_details(conversation_id: str):
    """Fetches the detailed info for a specific conversation from ElevenLabs."""
    url = f"{BASE_URL}/convai/conversations/{conversation_id}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()  # Contains conversation_name, messages, etc.
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching conversation {conversation_id}: {e}")
        return None

# Fetch and display the last 10 conversations in an "expanding table"
data = fetch_conversations()

if data and "conversations" in data:
    conversations = data["conversations"]

    if not conversations:
        st.warning("No conversations returned.")
    else:
        # Just take the first 10 items (or adjust if you want to sort them)
        last_ten = conversations[:10]

        st.subheader("Last 10 Conversations")

        for i, convo in enumerate(last_ten, start=1):
            conversation_id = convo.get("conversation_id", "N/A")
            agent_name = convo.get("agent_name", "N/A")
            call_duration_secs = convo.get("call_duration_secs", "N/A")
            message_count = convo.get("message_count", "N/A")
            call_successful = convo.get("call_successful", "N/A")


            # Fetch the full details for each conversation
            details = fetch_conversation_details(conversation_id)

            # Create an expander row for each conversation
            with st.expander(f"No.{i} — {conversation_id} - {agent_name} — {call_duration_secs} — {message_count}, — {call_successful}", expanded=False):
                

                # You can show more summary fields as needed here

                # Then the raw details (JSON)
                st.markdown("**Detailed Conversation Data:**")
                if details:
                    st.json(details)
                else:
                    st.write("No details available for this conversation.")
else:
    st.warning("No conversations found or unable to retrieve data.")
