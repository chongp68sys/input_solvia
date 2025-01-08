import streamlit as st
from descope.descope_client import DescopeClient
from descope.exceptions import AuthException

DESCOPE_PROJECT_ID = str(st.secrets.get("DESCOPE_PROJECT_ID"))
descope_client = DescopeClient(project_id=DESCOPE_PROJECT_ID)

def authenticate_user():
    """Handles user authentication."""
    if "token" not in st.session_state:
        if "code" in st.query_params:
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
            if st.button("Sign In with Google"):
                oauth_response = descope_client.oauth.start(
                    provider="google", return_url="https://tel-solvia.fly.dev/"
                )
                st.markdown(
                    f'<meta http-equiv="refresh" content="0; url={oauth_response["url"]}">',
                    unsafe_allow_html=True,
                )
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
