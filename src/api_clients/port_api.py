# src/api_clients/port_api.py
import json
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

    def get_integration_data(self, integration_id: str) -> Dict[str, Any]:
        """
        Fetch integration data for a given integration ID.
        """
        if not self.token:
            self.authenticate()

        url = f"{self.base_url}/integration/{integration_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        return response.json()

    def update_blueprint(self, blueprint_identifier: str, payload: Dict[str, Any]) -> Any:
        if not self.token:
            self.authenticate()

        url = f"{self.base_url}/blueprints/{blueprint_identifier}"
        response = requests.patch(url, headers=self.headers, data=json.dumps(payload))

        # Check for HTTP errors and return a structured response
        try:
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            return {
                "status": "success",
                "data": response.json()  # Parse JSON response if successful
            }
        except requests.exceptions.HTTPError as http_err:
            return {
                "status": "error",
                "error": str(http_err),
                "details": response.text  # Include server's error message for context
            }
        except requests.exceptions.RequestException as req_err:
            return {
                "status": "error",
                "error": str(req_err),
                "details": "An error occurred during the request."
            }

    def create_scorecard(self, blueprint_identifier: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/blueprints/{blueprint_identifier}/scorecards"

        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        # Check for HTTP errors and return a structured response
        try:
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            return {
                "status": "success",
                "data": response.json()  # Parse JSON response if successful
            }
        except requests.exceptions.HTTPError as http_err:
            return {
                "status": "error",
                "error": str(http_err),
                "details": response.text  # Include server's error message for context
            }
        except requests.exceptions.RequestException as req_err:
            return {
                "status": "error",
                "error": str(req_err),
                "details": "An error occurred during the request."
            }