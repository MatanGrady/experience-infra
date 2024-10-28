# src/web_app/app.py

from flask import Flask, render_template, request, jsonify

from src.yaml_handler.yaml_executor import YAMLExecutor
from src.yaml_handler.yaml_loader import load_yaml_files
from src.api_clients.port_api import PortAPI
import os
from ruamel.yaml import YAML

app = Flask(__name__, static_folder="../../static", template_folder="../../templates")

# Initialize the PortAPI instance
port_api = PortAPI()

# Load YAML files and check for required inputs when rendering the main page
@app.route('/')
def index():
    yaml_folder = os.path.join(os.path.dirname(__file__), "../../configuration_files")
    yaml_data = load_yaml_files(yaml_folder)  # Load YAML data with title, description, and inputs
    return render_template('index.html', yaml_data=yaml_data)


# Endpoint to execute steps based on YAML and inputs
@app.route('/execute_steps', methods=['POST'])
def execute_steps():
    data = request.get_json()
    filename = data.get("filename")
    inputs = data.get("inputs", {})

    # Load the YAML file content
    yaml_folder = os.path.join(os.path.dirname(__file__), "../../configuration_files")
    yaml_executor = YAMLExecutor(yaml_folder, port_api)

    # Load the YAML content
    try:
        yaml_content = yaml_executor.load_yaml(filename)
    except FileNotFoundError:
        return jsonify({"error": "YAML file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Pass the inputs and build the execution plan
    yaml_executor.inputs = inputs
    execution_plan = yaml_executor.build_execution_plan(yaml_content)

    # Execute the steps and filter the response
    results = yaml_executor.execute_steps()
    filtered_results = [
        {
            "step_number": result.get("step_number"),
            "step_name": result.get("step_name"),
            "action": result.get("action"),
            "status": result.get("status")
        }
        for result in results
    ]

    # Return the filtered execution results
    return jsonify({"execution_results": filtered_results})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)