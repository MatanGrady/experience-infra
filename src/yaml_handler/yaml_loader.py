# src/yaml_handler/yaml_loader.py

import os
from ruamel.yaml import YAML

def load_yaml_files(yaml_folder):
    yaml = YAML()
    yaml_data = []
    for filename in os.listdir(yaml_folder):
        if filename.endswith(".yml"):
            file_path = os.path.join(yaml_folder, filename)
            with open(file_path, "r") as file:
                data = yaml.load(file)
                # Extract title and description for each YAML file
                title = data.get("title", "No Title")
                description = data.get("description", "No Description")
                yaml_data.append({
                    "title": title,
                    "description": description,
                    "filename": filename
                })
    return yaml_data