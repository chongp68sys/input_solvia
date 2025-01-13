import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# Constants
BASE_URL = "https://api.elevenlabs.io/v1"
ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]

# Functions to fetch data
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

# Main Application
def main():
    st.title("Conversations Viewer")
    
    # Input for Agent ID
    agent_id = st.text_input("Enter Agent ID", value="", help="Provide the Agent ID to fetch conversations.")
    
    if agent_id:
        # Placeholder for the conversations list
        conversations_placeholder = st.empty()
        
        # Button to manually fetch conversations
        fetch_button = st.button("Fetch Conversations")
        
        # Auto-refresh every 30 seconds (30000 milliseconds)
        refresh_count = st_autorefresh(interval=30000, key="conversation_refresh", 
                                       min_interval=10000, max_interval=60000, 
                                       limit=None, 
                                       stale_time=1000)
        
        # Function to load and display conversations
        def load_conversations():
            data = fetch_conversations(agent_id)
            if data and "conversations" in data:
                conversations = data["conversations"]
                if not conversations:
                    conversations_placeholder.warning("No conversations returned.")
                else:
                    with conversations_placeholder.container():
                        st.subheader("Last 10 Conversations")
                        for i, convo in enumerate(conversations[:10], start=1):
                            conversation_id = convo.get("conversation_id", "N/A")
                            agent_name = convo.get("agent_name", "N/A")
                            call_duration_secs = convo.get("call_duration_secs", "N/A")
                            message_count = convo.get("message_count", "N/A")
                            call_successful = convo.get("call_successful", False)
                            
                            st.markdown(
                                f"### No.{i} — Agent: {agent_name}\n"
                                f"- **Conversation ID:** {conversation_id}\n"
                                f"- **Duration:** {call_duration_secs} seconds\n"
                                f"- **Messages:** {message_count}\n"
                                f"- **Successful:** {'Yes' if call_successful else 'No'}"
                            )
                            
                            with st.expander("View Details"):
                                details = fetch_conversation_details(conversation_id)
                                if details:
                                    st.json(details)
                                else:
                                    st.write("No additional details available for this conversation.")
            else:
                conversations_placeholder.warning("No conversations found or unable to retrieve data.")
        
        # Determine when to load conversations:
        # 1. When the user clicks the "Fetch Conversations" button.
        # 2. When the auto-refresh triggers (excluding the initial run).
        if fetch_button or refresh_count:
            load_conversations()
        else:
            conversations_placeholder.info("Click 'Fetch Conversations' to load data or wait for auto-refresh.")
    else:
        st.info("Please enter an Agent ID to fetch conversations.")

if __name__ == "__main__":
    main()
