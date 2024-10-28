# tests/test_port_api.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.api_clients.port_api import PortAPI

def test_port_api():
    # Initialize PortAPI
    port_api = PortAPI()

    # Authenticate and get the access token
    token = port_api.authenticate()
    print("Access Token:", token)

    # Fetch a blueprint data as a test
    blueprint_id = "service"  # Replace with a valid blueprint ID for testing
    blueprint_data = port_api.get_blueprint_data(blueprint_id)
    print("Blueprint Data:", blueprint_data)

if __name__ == "__main__":
    test_port_api()