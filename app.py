import streamlit as st
import requests

# Streamlit App
st.title("📞 Solvia Lead Caller")

# Input fields
to_number = st.text_input("Enter the recipient's phone number", "+44764666395")

# Function to validate phone number
def is_valid_phone_number(phone_number):
    # Validate if the number starts with a '+' followed by 10 to 15 digits
    import re
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

# Button with telephone emoji
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
        payload = {"to_number": to_number}

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
