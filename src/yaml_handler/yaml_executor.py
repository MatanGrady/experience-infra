# src/yaml_handler/yaml_executor.py

from dataclasses import dataclass, field
from typing import List, Dict, Any

import requests
from ruamel.yaml import YAML
import os
import re
from src.api_clients.port_api import PortAPI  # Import the PortAPI class


@dataclass
class Step:
    step_number: int
    action: str
    resource_type: str
    resource_id: str
    details: Dict[str, Any] = field(default_factory=dict)
    result: Any = None


class YAMLExecutor:
    def __init__(self, yaml_folder: str, port_api: PortAPI, inputs: Dict[str, Any] = None):
        self.yaml_folder = yaml_folder
        self.port_api = port_api
        self.inputs = inputs or {}  # Store user inputs
        self.steps: List[Step] = []

        # Define a function registry for action handlers
        self.action_registry = {
            "load_resource": self.load_resource,
            "add_properties_to_blueprint": self.add_properties_to_blueprint,
            "add_scorecards_to_blueprint": self.add_scorecards_to_blueprint,
            "upsert_integration": self.upsert_integration
        }

    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """
        Load the YAML file and return its content as a dictionary.
        """
        file_path = os.path.join(self.yaml_folder, filename)
        yaml = YAML()
        with open(file_path, 'r') as file:
            return yaml.load(file)

    def build_execution_plan(self, yaml_content: Dict[str, Any]) -> List[Step]:
        """
        Parse the YAML content and convert each step into a Step object
        without resolving placeholders.
        """
        steps = yaml_content.get("steps", [])
        execution_plan = []
        for i, step_data in enumerate(steps, start=1):
            action = step_data.get("action")

            # Capture resource type and id without resolving placeholders
            resource_type = step_data.get("resource_type")
            resource_id = step_data.get("resource_id")

            # Capture all other fields as part of `details`
            details = {key: value for key, value in step_data.items() if
                       key not in ["action", "resource_type", "resource_id"]}

            # Create the Step object with additional details
            step = Step(
                step_number=i,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                details=details
            )
            execution_plan.append(step)
        self.steps = execution_plan
        return execution_plan

    def resolve_placeholders(self, text: str) -> str:
        """
        Detects and resolves placeholders in the given text by delegating to
        specific resolvers for inputs or step results.
        """
        if not text or not isinstance(text, str):
            return text

        # Resolve inputs placeholders
        text = self.resolve_input_placeholder(text)

        # Resolve step result placeholders
        text = self.resolve_step_result_placeholder(text)

        return text

    def resolve_input_placeholder(self, text: str) -> str:
        """
        Resolves placeholders in the format {{ inputs.<key> }} using values from self.inputs.
        """
        pattern = r"{{\s*inputs\.([\w\s]+)\s*}}"

        def replacer(match):
            key = match.group(1).strip()
            return str(self.inputs.get(key, f"{{{{ inputs.{key} }}}}"))  # Leave unresolved if not found

        return re.sub(pattern, replacer, text)

    def resolve_step_result_placeholder(self, text: str) -> str:
        """
        Resolves placeholders in the format {{ steps.<step_name>.result }} using values
        from the results of previous steps in self.steps.
        """
        # Updated pattern to match placeholders like {{ steps.<step_name>.result }}
        # <step_name> can include alphanumeric characters, spaces, and underscores
        pattern = r"{{\s*steps\.([a-zA-Z0-9_ ]+)\.result\s*}}"

        def replacer(match):
            # Extract the step name from the matched pattern
            step_name = match.group(1).strip()

            # Find the step by name and get its result
            for step in self.steps:
                if step.details.get("name") == step_name:
                    # Return the resolved result or leave the placeholder unresolved if result is None
                    return str(step.result) if step.result is not None else f"{{{{ steps.{step_name}.result }}}}"

            # If no matching step is found, return the placeholder as-is
            return f"{{{{ steps.{step_name}.result }}}}"

        return re.sub(pattern, replacer, text)

    def load_resource(self, step: Step) -> Dict[str, Any]:
        """
        Action handler for loading a resource.
        Calls the appropriate PortAPI method based on resource_type.
        """
        resource_type = step.resource_type
        resource_id = step.resource_id

        try:
            if resource_type == "blueprint":
                # Call the PortAPI method to get blueprint data
                resource_data = self.port_api.get_blueprint_data(resource_id)
            # elif resource_type == "integration":
                # Placeholder for future integration API call
                # resource_data = self.port_api.get_integration_data(resource_id)  # Hypothetical method
            else:
                return {
                    "status": "error",
                    "message": f"Unsupported resource type: {resource_type}"
                }

            return {
                "status": "success",
                "action": "load_resource",
                "resource_type": resource_type,
                "resource_id": resource_id,
                "data": resource_data
            }

        except requests.RequestException as e:
            return {
                "status": "error",
                "action": "load_resource",
                "error": str(e)
            }

    def add_properties_to_blueprint(self, step: Step) -> Dict[str, Any]:
        """
        Action handler for adding properties to a blueprint.
        """
        properties = step.details.get("properties", [])
        blueprint_data = step.details.get("blueprint_data")

        # Simulate adding properties to a blueprint
        return {"status": "success", "action": "add_properties_to_blueprint", "properties_added": properties, "context": blueprint_data}

    def add_scorecards_to_blueprint(self, step: Step) -> Dict[str, Any]:
        """
        Action handler for adding scorecards to a blueprint.
        """
        scorecards = step.details.get("scorecards", [])
        blueprint_data = step.details.get("blueprint_data")

        # Simulate adding scorecards to a blueprint
        return {"status": "success", "action": "add_scorecards_to_blueprint", "scorecards_added": scorecards, "context": blueprint_data}

    def upsert_integration(self, step: Step) -> Dict[str, Any]:
        """
        Action handler for upserting an integration.
        """
        integration_data = step.details.get("data", [])
        # Simulate upserting an integration
        return {"status": "success", "action": "upsert_integration", "integration_data": integration_data}

    def execute_steps(self) -> List[Dict[str, Any]]:
        """
        Execute each step in the execution plan, resolving placeholders as needed.
        """
        results = []
        for step in self.steps:
            # Resolve placeholders just before executing the step
            step.resource_type = self.resolve_placeholders(step.resource_type)
            step.resource_id = self.resolve_placeholders(step.resource_id)
            step.details = {key: self.resolve_placeholders(value) for key, value in step.details.items()}

            # Look up the handler based on the action name
            handler = self.action_registry.get(step.action)
            if handler:
                result = handler(step)  # Call the appropriate handler with the step
                step.result = result  # Store the result directly in the Step object
            else:
                result = {"step_number": step.step_number, "status": "unknown action", "action": step.action}

            result["step_number"] = step.step_number  # Include the step number in the result
            results.append(result)
        return results