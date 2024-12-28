import requests

def get_ups_shipping_rate(access_token, ship_from, ship_to, package):
    return None
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def get_ups_estimated_delivery(access_token, delivery_data):
    url = "https://wwwcie.ups.com/api/shipments/v1/transittimes"  # Replace :version with the actual version number
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
        "transactionSrc": "testing"
    }
    
    response = requests.post(url, json=delivery_data, headers=headers)
    return response.json()