
# YAML-Driven Workflow Executor

This repository provides a Python-based web application to execute workflows defined in YAML files. The workflows integrate with the [Port API](https://docs.getport.io/api-reference) to manage resources. It allows for easy configuration and execution of workflows to automate tasks within Port's developer portal.

## Key Features

- **YAML-Driven Workflows**: Define workflows with YAML files specifying sequential steps and actions.
- **Integration with Port API**: Interact with Port blueprints, properties, and scorecards through authenticated API calls.
- **Dynamic Inputs and Execution**: Accept inputs via a web UI, dynamically resolving placeholders in YAML steps.
- **Execution Plan and Status Monitoring**: Executes each workflow step-by-step and provides status and results for each action.

## Use Cases

- **Automate Blueprint Management**: Define and manage blueprints with properties and relationships using YAML-based workflows.
- **Create and Update Scorecards**: Automate the creation of scorecards with rules and levels for performance monitoring.
- **Upsert Integration Configurations**: Configure integrations by adding, updating, or validating integration data directly from YAML specifications.
- **Load and Manage Complex Entities**: Manage complex structures within Port by defining entity data, relations, and properties in a single YAML file.

## Repository Structure

```plaintext
.
├── src/
│   ├── api_clients/
│   │   └── port_api.py          # Client for interacting with the Port API
│   ├── yaml_handler/
│   │   └── yaml_executor.py     # Executes YAML-defined workflows
│   └── main.py                  # Web server and application entry point
├── configuration_files/         # Folder containing YAML configuration files
├── tests/                       # Test files for unit testing the application
└── README.md                    # Project documentation
```

## Getting Started

### Prerequisites

1. **Python 3.12+**: Ensure Python 3.8 or newer is installed.
2. **Port API Access**: Obtain `PORT_CLIENT_ID` and `PORT_CLIENT_SECRET` from Port to authenticate API requests.

### Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/MatanGrady/experience-infra.git
   cd experience-infra
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**

   Create a `.env` file in the root directory and add your Port credentials:

   ```plaintext
   PORT_CLIENT_ID=your_port_client_id
   PORT_CLIENT_SECRET=your_port_client_secret
   ```

### Running the Application

1. **Start the Web Application**

   ```bash
   python src/main.py
   ```

   The application will be accessible at `http://0.0.0.0:5001`.

2. **Access the Web Interface**

   Open your browser and go to `http://localhost:5001`. The main page displays available YAML workflow configurations as clickable boxes. Each box represents a YAML-defined workflow.

3. **Executing a Workflow**

   - Click on a workflow box to view or provide the necessary inputs.
   - After entering inputs (if any), click **Continue** to execute the workflow.
   - The workflow execution status will display the results for each step.

### Writing a YAML Workflow

Each YAML file in `configuration_files` defines a workflow with the following structure:

```yaml
title: "Add PR Metrics"
description: "Enrich your pull requests with advanced metrics"

inputs:
  service:
    type: blueprint
    result: service_blueprint_identifier
  Pull request:
    type: blueprint
    result: pull_request_blueprint_identifier

steps:
  - name: Load Service Blueprint
    action: load_resource
    resource_type: blueprint
    resource_id: "{{ inputs.service.result }}"
    result: service_data

  - name: Upsert Properties to Pull Request
    action: add_properties_to_blueprint
    blueprint_data: "{{ steps.Load Pull Request Blueprint.result }}"
    properties:
      - identifier: "changed_files"
        name: "Changed files"
        type: "number"
```

#### Key Elements

- **Inputs**: Specifies required inputs like `service` or `Pull request` that must be provided via the UI before executing the workflow.
- **Steps**: Each step includes:
  - `name`: A description of the step.
  - `action`: The type of action (e.g., `load_resource`, `add_properties_to_blueprint`).
  - `resource_type` and `resource_id`: Specify the resource type and ID.
  - `properties` or `rules`: Define properties or rules for actions like adding properties or creating scorecards.

#### Supported Methods

- **Add Properties to Blueprint**: Adds standard properties to a specified blueprint. These properties may include identifiers, titles, and data types to define attributes of the blueprint.
- **Add Aggregation Properties to Blueprint**: Adds aggregation properties that specify calculated metrics, such as averages, based on related entity data within the blueprint.
- **Add Scorecards to Blueprint**: Creates scorecards associated with a blueprint, each with custom rules and metrics to monitor and evaluate performance or quality standards.

#### Future Enhancements

- **Update Integration Mapping**: Ability to dynamically update the mappings in an existing integration based on predefined rules or data transformations.
- **Create Blueprint**: Automate the creation of new blueprints with specified properties, schema, and initial configuration.
- **Update Blueprint Calculation Properties**: Update or define complex calculation-based properties for a blueprint, which are derived from existing data points.
- **Update Blueprint Relations**: Add or modify relationships within a blueprint, connecting it to other entities or services within the system.

### Example API Calls

The application uses the Port API for actions like updating blueprints and creating scorecards. Here’s an example API call to add a scorecard:

```python
url = "https://api.getport.io/v1/blueprints/{blueprint_identifier}/scorecards"
payload = {
    "identifier": "scorecard_id",
    "title": "Scorecard Title",
    "rules": [
        {
            "identifier": "rule_id",
            "title": "Rule Title",
            "level": "Gold",
            "query": {
                "combinator": "and",
                "conditions": [{"property": "field", "operator": "=", "value": "some_value"}]
            }
        }
    ]
}
headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
response = requests.post(url, headers=headers, json=payload)
```

### Testing

To run the tests:

```bash
pytest tests/
```

This will execute unit tests to validate functionality, including the API client (`PortAPI`) and the YAML executor (`YAMLExecutor`).

### Troubleshooting

- **HTTP 403 Forbidden**: Ensure your Port API credentials are correctly set in the `.env` file.
- **Invalid YAML File**: Verify that the YAML syntax is correct and all placeholders are provided.
- **Execution Errors**: Check the console output for details on failed steps or errors in API requests.

## Contributing

If you'd like to contribute, please create a branch, make your changes, and open a pull request.

## License

This project is licensed under the MIT License.
