import os
import streamlit as st
from jose import jwt
import jwt as pyjwt
from dotenv import load_dotenv
from authlib.integrations.requests_client import OAuth2Session
from urllib.parse import urlencode

# Load environment variables
load_dotenv()

# Auth0 configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")

# Initialize session state
if "token" not in st.session_state:
    st.session_state.token = None
if "user_info" not in st.session_state:
    st.session_state.user_info = None

def get_auth_url():
    """Generate the Auth0 authorization URL"""
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": "openid profile email",
        "audience": AUTH0_AUDIENCE,
    }
    return f"https://{AUTH0_DOMAIN}/authorize?{urlencode(params)}"

def get_token(code):
    """Exchange the authorization code for a token"""
    client = OAuth2Session(
        AUTH0_CLIENT_ID,
        AUTH0_CLIENT_SECRET,
        token_endpoint=f"https://{AUTH0_DOMAIN}/oauth/token"
    )
    token = client.fetch_token(
        f"https://{AUTH0_DOMAIN}/oauth/token",
        grant_type="authorization_code",
        code=code,
        redirect_uri=AUTH0_CALLBACK_URL
    )
    return token

def get_jwks_client():
    """Get JWKS client for Auth0"""
    jwks_url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
    return pyjwt.PyJWKClient(jwks_url)

def decode_jwt(token):
    """Decode the JWT token"""
    try:
        jwks_client = get_jwks_client()
        rsa_key = jwks_client.get_signing_key_from_jwt(token).key
        
        decoded = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],  # Should match the algorithm set in the Auth0 app settings
            audience=AUTH0_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/"
        )
        return decoded
    except Exception as e:
        st.error(f"Error decoding JWT: {str(e)}")
        return None

def main():
    st.title("Auth0 Login Test App")
    
    # Check if we're in the callback
    if "code" in st.query_params:
        code = st.query_params["code"]
        token = get_token(code)
        st.session_state.token = token
        st.query_params.clear()
    
    if st.session_state.token:
        # Display token information
        st.subheader("Access Token")
        st.code(st.session_state.token["access_token"])
        
        # Decode and display JWT
        st.subheader("Decoded JWT")
        decoded_token = decode_jwt(st.session_state.token["access_token"])
        if decoded_token:
            st.json(decoded_token)
        
        # Logout button
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.user_info = None
            st.experimental_rerun()
    else:
        # Login button
        auth_url = get_auth_url()
        st.markdown(f'<a href="{auth_url}" target="_self">Login with Auth0</a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 