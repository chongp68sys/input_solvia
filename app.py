import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import re

# Set the interval to 10000 milliseconds (10 seconds)
st_autorefresh(interval=10000, key="data_refresh")

# Replace with your actual ElevenLabs API key or use st.secrets for security
ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
BASE_URL = "https://api.elevenlabs.io/v1"

headers = {
    "xi-api-key": ELEVENLABS_API_KEY,
    "Content-Type": "application/json"
}

st.title("📞 Solvia Lead Caller")

# Sidebar Inputs
with st.sidebar:
    st.subheader("Caller Information")

    # Input fields in the sidebar
    name = st.text_input("Enter the person's name", "Juan")
    to_number = st.text_input("Enter the recipient's phone number", "+447764666395")

    # Function to validate phone number
    def is_valid_phone_number(phone_number):
        # Validate if the number starts with a '+' followed by 10 to 15 digits
        pattern = r"^\+\d{10,15}$"
        return bool(re.match(pattern, phone_number))

    # Custom CSS for the button
    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        div.stButton > button:first-child:hover {
            background-color: #45a049;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Button (with telephone emoji) in the sidebar
    if st.button("📞 Make Call"):
        # Validate the input
        if not is_valid_phone_number(to_number):
            st.error("Invalid phone number! Ensure it starts with '+' and has 10 to 15 digits.")
        else:
            url = "https://solvia-lead.fly.dev/calls"
            headers = {
                "Content-Type": "application/json",
                "X-API-Key": "i-like-pomme",
            }
            payload = {"name": name, "to_number": to_number}

            try:
                response = requests.post(url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    st.success(f"Call initiated successfully: {response.text}")
                elif response.status_code == 401:
                    st.error("Unauthorized: Check your API key.")
                elif response.status_code == 400:
                    st.error("Bad Request: Check the phone number format.")
                elif response.status_code == 404:
                    st.error("Not Found: Verify the API URL.")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred while making the call: {e}")
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
