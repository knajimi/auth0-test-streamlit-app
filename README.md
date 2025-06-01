# Auth0 Streamlit Test App

This is a Streamlit application that demonstrates Auth0 authentication flow and JWT token handling.

## Prerequisites

- Python 3.12 or higher (lower probably also supported)
- UV package manager
- Auth0 account and application

## Setup

1. Clone this repository
2. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate  # On Windows
   
   uv pip install -r pyproject.toml
   ```

3. Create a `.env` file based on `.env.example` and fill in your Auth0 credentials:
   ```
   AUTH0_DOMAIN=your-tenant.auth0.com
   AUTH0_CLIENT_ID=your-client-id
   AUTH0_CLIENT_SECRET=your-client-secret
   AUTH0_CALLBACK_URL=http://localhost:8501/callback
   AUTH0_AUDIENCE=your-api-identifier
   ```

## Running the Application

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

## Features

- Auth0 login integration
- JWT token retrieval and display
- Token decoding and display
- Session management
- Logout functionality

## Auth0 Configuration

1. Create a new application in your Auth0 dashboard
2. Set the callback URL to `http://localhost:8501/callback`
    - Make sure that callback URL is allowed in the Auth0 app settings.
3. Enable the "Authorization Code" grant type
4. Configure the application settings and copy the credentials to your `.env` file 
5. For the user profile to show up, you need to have `profile` configured as a scope returned by your Auth0 app (i.e. you should see `"scope": "profile"` in your decoded JWT.)
