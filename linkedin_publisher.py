import os
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_API_BASE = "https://api.linkedin.com/v2"

def get_user_urn() -> str:
    """
    Fetch your LinkedIn person URN — a unique identifier like 'urn:li:person:AbC123'.
    This is required by the API to know whose account to post to.
    """
    response = requests.get(
        f"{LINKEDIN_API_BASE}/userinfo",
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }
    )

    data = response.json()

    if "sub" not in data:
        raise Exception(
            f" Could not fetch LinkedIn user ID.\n"
            f"Response: {data}\n"
            f"Make sure your LINKEDIN_ACCESS_TOKEN is valid and not expired."
        )

    
    user_urn = f"urn:li:person:{data['sub']}"
    print(f" Posting as: {data.get('name', 'Unknown')} ({user_urn})")
    return user_urn


def publish_to_linkedin(post_content: str) -> str:
    """
    Publishes a text post to LinkedIn using the UGC Posts API.
    
    Args:
        post_content: The final post text (with emojis and hashtags)
    
    Returns:
        The LinkedIn post ID (e.g., 'urn:li:ugcPost:1234567890')
    
    Raises:
        Exception: If the API call fails
    """
    if not ACCESS_TOKEN:
        raise Exception(
            " LINKEDIN_ACCESS_TOKEN is not set in your .env file.\n"
            "Run: python auth/get_token.py"
        )

    user_urn = get_user_urn()

   
    payload = {
        "author": user_urn,
        "lifecycleState": "PUBLISHED",          
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post_content         
                },
                "shareMediaCategory": "NONE"    
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"  
        }
    }

    print("Sending post to LinkedIn API...")

    response = requests.post(
        f"{LINKEDIN_API_BASE}/ugcPosts",
        json=payload,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"   
        }
    )

    
    if response.status_code == 201:
        post_id = response.headers.get("x-restli-id", "unknown")
        print(f" Post published successfully!")
        print(f" Post ID: {post_id}")
        print(f" View your post at: https://www.linkedin.com/feed/")
        return post_id
    else:
        raise Exception(
            f" LinkedIn API error {response.status_code}:\n"
            f"{response.text}"
        )