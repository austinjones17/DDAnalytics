import requests
import json

''' Defining Global Variables '''

# DD-ANALYTICS-DEANGELIS-DIAMOND-CONSTRUCTION-HQ
CONSTRUCTION_ID = "6e3d461b4a4b00f7600700ff9ffd39a5561c3b8ff5b4047d1039414f8069b67e"
CONSTRUCTION_SECRET = "3a0e9feb4e5b6a45f3c43575c819d15bf3ac0d75f30b93c545c3047449e5f23b"

# DD-ANALYTICS-DEANGELIS-DIAMOND-HEALTHCARE

HEALTHCARE_ID = "5f3215a03186d8af0ebf6a8228506afb3334d9696ff31c9207248ea630b6e61d"
HEALTHCARE_SECRET = "1390ee26c788fb60138af1d3b4842a3753a0bbc3924bc434908a7b49518a41f7"

# Construction global auth token

# CONSTRUCTION_TOKEN = None

# Healthcare global auth token

HEALTHCARE_TOKEN = None


def refresh_construction_token():
    url = "https://api.procore.com/oauth/token"
    querystring = {"grant_type": "client_credentials",
                   "client_id": CONSTRUCTION_ID,
                   "client_secret": CONSTRUCTION_SECRET
                   }
    response = requests.request("POST", url, params=querystring)
    data = json.loads(response.text)
    token = data['access_token']
    return token


def refresh_healthcare_token():
    url = "https://api.procore.com/oauth/token"
    querystring = {"grant_type": "client_credentials",
                   "client_id": HEALTHCARE_ID,
                   "client_secret": HEALTHCARE_SECRET
                   }
    response = requests.request("POST", url, params=querystring)
    data = json.loads(response.text)
    token = data['access_token']
    return token