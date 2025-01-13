import streamlit as st
from descope.descope_client import DescopeClient
from descope.exceptions import AuthException

# Load your project ID from Streamlit secrets
DESCOPE_PROJECT_ID = str(st.secrets.get("DESCOPE_PROJECT_ID"))
descope_client = DescopeClient(project_id=DESCOPE_PROJECT_ID)

def authenticate_user():
    """Handles user authentication with Magic Link."""
    if "token" not in st.session_state:
        if "code" in st.query_params:
            # Handle the callback with the authorization code from the magic link
            code = st.query_params["code"]
            st.query_params.clear()
            try:
                with st.spinner("Authenticating..."):
                    jwt_response = descope_client.magiclink.verify(code)
                st.session_state["token"] = jwt_response["sessionToken"].get("jwt")
                st.session_state["refresh_token"] = jwt_response["refreshSessionToken"].get("jwt")
                st.session_state["user"] = jwt_response["user"]
                st.rerun()
            except AuthException:
                st.error("Login failed! Please try again.")
        else:
            # Prompt user to enter their email or phone
            st.warning("You're not logged in. Enter your email to receive a Magic Link.")
            user_email = st.text_input("Email", placeholder="Enter your email", key="email_input")
            if st.button("Send Magic Link", key="send_button"):
                send_magic_link(user_email)
        return False  # User is not authenticated
    else:
        try:
            with st.spinner("Validating session..."):
                jwt_response = descope_client.validate_and_refresh_session(
                    st.session_state.token, st.session_state.refresh_token
                )
                st.session_state["token"] = jwt_response["sessionToken"].get("jwt")
            return True  # User is authenticated
        except AuthException:
            del st.session_state["token"]
            st.rerun()

def send_magic_link(email):
    """Sends a magic link to the user's email."""
    try:
        with st.spinner("Sending Magic Link..."):
            descope_client.magiclink.send(
                login_id=email,
                uri="https://tel-solvia.fly.dev/",  # Replace with your app's return URL
            )
        st.success(f"Magic Link sent to {email}. Check your inbox!")
    except AuthException:
        st.error("Failed to send Magic Link. Please check the email address and try again.")

# Main Streamlit app logic
if authenticate_user():
    st.success(f"Welcome, {st.session_state['user']['name']}!")
    # App logic goes here for authenticated users
else:
    st.info("Please log in to continue.")
