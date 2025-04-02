import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import glob

# Define the scopes your application needs
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

def setup_credentials():
    """
    Set up and save YouTube API credentials
    
    This script will:
    1. Check for existing token.json file
    2. If not found or tokens expired, run OAuth 2.0 flow
    3. Save credentials to token.json for future use
    """
    credentials = None
    
    # Token file stores the user's access and refresh tokens
    token_file = "token.json"
    
    # Check if token file exists
    if os.path.exists(token_file):
        try:
            credentials = Credentials.from_authorized_user_info(
                json.loads(open(token_file).read()), SCOPES
            )
        except Exception as e:
            print(f"Error loading existing credentials: {e}")
    
    # If no valid credentials available, let the user log in
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            # Look for client secrets file
            client_secrets_file = None
            
            # Check for client_secret* files in the current directory and parent directory
            possible_files = (
                glob.glob("client_secret*.json") + 
                glob.glob("../client_secret*.json") +
                glob.glob("*.json")
            )
            
            if possible_files:
                client_secrets_file = possible_files[0]
                print(f"Found client secrets file: {client_secrets_file}")
            else:
                # If not found automatically, ask user
                client_secrets_file = input("Enter path to your OAuth client secrets JSON file: ")
            
            if not os.path.exists(client_secrets_file):
                print(f"Error: File {client_secrets_file} not found!")
                return
            
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, SCOPES)
            credentials = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(credentials.to_json())
            print(f"Credentials saved to {token_file}")
    
    print("Credentials setup completed successfully!")
    return credentials

if __name__ == "__main__":
    setup_credentials() 