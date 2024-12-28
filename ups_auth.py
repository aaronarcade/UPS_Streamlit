import requests

def get_ups_token(client_id, client_secret):
    token_url = "https://onlinetools.ups.com/security/v1/oauth/token"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "client_credentials",
    }
    
    # Basic auth using client_id and client_secret
    response = requests.post(
        token_url,
        headers=headers,
        data=data,
        auth=(client_id, client_secret)
    )
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Failed to get token: {response.text}")