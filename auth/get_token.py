

import os
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")


SCOPE = "openid profile email w_member_social"

captured_code = None

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """
    A minimal HTTP server that runs locally to catch LinkedIn's redirect.
    When you log in to LinkedIn, it redirects to http://localhost:8080/callback
    with an authorization code in the URL. This handler grabs that code.
    """

    def do_GET(self):
        global captured_code

        
        query_params = parse_qs(urlparse(self.path).query)
        captured_code = query_params.get("code", [None])[0]

        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"""
            <html>
            <body style="font-family: sans-serif; text-align: center; padding: 50px;">
                <h2>&#10003; Authentication Successful!</h2>
                <p>You can close this tab and return to your terminal.</p>
            </body>
            </html>
        """)

    def log_message(self, format, *args):
        pass  

def run_auth_flow():
    """
    Full OAuth 2.0 flow:
    1. Open LinkedIn login in browser
    2. User logs in and approves permissions
    3. LinkedIn redirects to localhost with auth code
    4. We exchange auth code for access token
    5. Print token for user to copy into .env
    """

    
    auth_url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPE.replace(' ', '%20')}"
        f"&state=scrollstopper_auth"   
    )

    print(" Opening LinkedIn login in your browser...")
    print(" If it doesn't open automatically, visit this URL:")
    print(f"   {auth_url}\n")
    webbrowser.open(auth_url)

    
    print(" Waiting for LinkedIn to redirect back...")
    server = HTTPServer(("localhost", 8080), OAuthCallbackHandler)
    server.handle_request()   

    if not captured_code:
        print(" Error: No authorization code received. Please try again.")
        return

    print(" Authorization code received!\n")

    
    print("Exchanging code for access token...")

    token_response = requests.post(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data={
            "grant_type": "authorization_code",
            "code": captured_code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    token_data = token_response.json()

    if "access_token" not in token_data:
        print(f" Token exchange failed: {token_data}")
        return

    access_token = token_data["access_token"]
    expires_in = token_data.get("expires_in", "unknown")

    print("=" * 60)
    print(" SUCCESS! Your LinkedIn Access Token:")
    print("=" * 60)
    print(f"\n{access_token}\n")
    print("=" * 60)
    print(f" Token expires in: {expires_in} seconds (~60 days)")
    print("\n Copy the token above and paste it into your .env file:")
    print("   LINKEDIN_ACCESS_TOKEN=<paste here>")
    print("=" * 60)


if __name__ == "__main__":
    run_auth_flow()