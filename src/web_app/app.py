from flask import Flask, render_template
from src.yaml_handler.yaml_loader import load_yaml_files
import os

app = Flask(__name__, template_folder="../../templates", static_folder="../../static")  # Explicitly set the template folder path

@app.route('/')
def index():
    yaml_folder = os.path.join(os.path.dirname(__file__), "../../configuration_files")
    yaml_data = load_yaml_files(yaml_folder)
    return render_template('index.html', yaml_data=yaml_data)

if __name__ == "__main__":
    app.run(debug=True)