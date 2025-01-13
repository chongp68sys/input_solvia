import streamlit as st
import requests
import re
from conversations import fetch_conversations

def is_valid_phone_number(phone_number):
    """Validate phone number format."""
    pattern = r"^\+\d{10,15}$"
    return bool(re.match(pattern, phone_number))

def solvia_caller():
    """Main logic for the Solvia Lead Caller."""
    with st.sidebar:
        st.subheader("Caller Information")
        name = st.text_input("Enter the person's name", "Paul")
        to_number = st.text_input("Enter the recipient's phone number", "+447764666395")
        agent_id = st.text_input("Agent ID", "wkf3emR8JrlVMWl93pu7")

        if st.button("📞 Make Call", key="make_call_button"):
            if not is_valid_phone_number(to_number):
                st.error("Invalid phone number! Ensure it starts with '+' and has 10 to 15 digits.")
            else:
                url = "https://solvia-lead.fly.dev/calls"
                headers = {
                    "Content-Type": "application/json",
                    "X-API-Key": "i-like-pomme",
                }
                payload = {"name": name, "to_number": to_number, "agent_id": agent_id}
                try:
                    response = requests.post(url, headers=headers, json=payload)
                    if response.status_code == 200:
                        st.success(f"Call initiated successfully: {response.text}")
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred while making the call: {e}")

# Uncomment below to run the application
# if __name__ == "__main__":
#     solvia_caller()
