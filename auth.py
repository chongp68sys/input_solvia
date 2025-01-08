import streamlit as st
from descope.descope_client import DescopeClient
from descope.exceptions import AuthException

# Load your project ID from Streamlit secrets
DESCOPE_PROJECT_ID = str(st.secrets.get("DESCOPE_PROJECT_ID"))
descope_client = DescopeClient(project_id=DESCOPE_PROJECT_ID)

def authenticate_user():
    """Handles user authentication."""
    if "token" not in st.session_state:
        if "code" in st.query_params:
            # Handle the callback with the authorization code
            code = st.query_params["code"]
            st.query_params.clear()
            try:
                with st.spinner("Authenticating..."):
                    jwt_response = descope_client.sso.exchange_token(code)
                st.session_state["token"] = jwt_response["sessionToken"].get("jwt")
                st.session_state["refresh_token"] = jwt_response["refreshSessionToken"].get("jwt")
                st.session_state["user"] = jwt_response["user"]
                st.rerun()
            except AuthException:
                st.error("Login failed!")
        else:
            st.warning("You're not logged in. Please log in to use the app.")
            # Social login buttons
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("Sign In with Google"):
                    redirect_to_oauth("google")
            with col2:
                if st.button("Sign In with Facebook"):
                    redirect_to_oauth("facebook")
            with col3:
                if st.button("Sign In with Microsoft"):
                    redirect_to_oauth("microsoft")
            with col4:
                if st.button("Sign In with GitHub"):
                    redirect_to_oauth("github")
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

def redirect_to_oauth(provider):
    """Redirects the user to the OAuth login page."""
    try:
        oauth_response = descope_client.oauth.start(
            provider=provider, return_url="https://tel-solvia.fly.dev/"
        )
        st.markdown(
            f'<meta http-equiv="refresh" content="0; url={oauth_response["url"]}">',
            unsafe_allow_html=True,
        )
    except AuthException:
        st.error(f"Failed to initiate login with {provider.capitalize()}!")
