# src/api_clients/port_api.py

import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

# Explicitly load the .env file here
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

class PortAPI:
    def __init__(self):
        self.base_url = "https://api.getport.io/v1"
        self.client_id = os.getenv("PORT_CLIENT_ID")
        self.client_secret = os.getenv("PORT_CLIENT_SECRET")
        self.token = None
        self.headers = {"Content-Type": "application/json"}

    def authenticate(self):
        """
        Retrieve an access token using clientId and clientSecret.
        """
        auth_url = f"{self.base_url}/auth/access_token"
        auth_data = {
            "clientId": self.client_id,
            "clientSecret": self.client_secret
        }

        response = requests.post(auth_url, json=auth_data, headers=self.headers)
        response.raise_for_status()

        self.token = response.json().get("accessToken")
        # Update headers with the token
        self.headers["Authorization"] = f"Bearer {self.token}"
        return self.token

    def get_blueprint_data(self, blueprint_id: str) -> Dict[str, Any]:
        """
        Fetch blueprint data for a given blueprint ID.
        """
        if not self.token:
            self.authenticate()

        url = f"{self.base_url}/blueprints/{blueprint_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        return response.json()