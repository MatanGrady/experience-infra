# src/web_app/app.py

from flask import Flask, render_template, request, jsonify
from src.yaml_handler.yaml_loader import load_yaml_files
import os
from ruamel.yaml import YAML

app = Flask(__name__, static_folder="../../static", template_folder="../../templates")


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
    file_path = os.path.join(yaml_folder, filename)  # This line may be causing the issue

    yaml = YAML()
    with open(file_path, 'r') as file:
        yaml_content = yaml.load(file)

    # Placeholder for Steps Manager logic
    execution_plan = []
    for i, step in enumerate(yaml_content.get("steps", []), start=1):
        execution_plan.append({
            "step": i,
            "action": step.get("action"),
            "details": step
        })

    return jsonify({"execution_plan": execution_plan})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)