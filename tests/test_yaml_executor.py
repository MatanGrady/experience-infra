# tests/test_yaml_executor.py

from src.yaml_handler.yaml_executor import YAMLExecutor
from src.api_clients.port_api import PortAPI
import os
from dotenv import load_dotenv

# Load environment variables from .env file if not already loaded
load_dotenv()


def test_yaml_executor():
    # Initialize PortAPI
    port_api = PortAPI()

    # Path to YAML configuration files
    yaml_folder = "../configuration_files"

    # Sample inputs to resolve placeholders
    inputs = {
        "service": "service",  # Replace with an actual ID
        "Pull request": "githubPullRequest",
        "Git Integration": "53367788"
    }

    # Initialize YAMLExecutor with PortAPI instance and inputs
    executor = YAMLExecutor(yaml_folder, port_api, inputs)

    # Load the YAML file with a load_resource step
    yaml_content = executor.load_yaml("pr_metrics.yml")  # Ensure this YAML file has a load_resource step

    # Build the execution plan and display each step
    execution_plan = executor.build_execution_plan(yaml_content)
    print("Execution Plan:")
    for step in execution_plan:
        print(f"Step {step.step_number}: {step.action} on {step.resource_type} (ID: {step.resource_id})")
        print("Details:", step.details)

    # Execute the steps and print results, including load_resource
    results = executor.execute_steps()
    print("\nExecution Results:")
    for result in results:
        print(result)


if __name__ == "__main__":
    test_yaml_executor()