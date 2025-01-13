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
                st.error("Login failed")
