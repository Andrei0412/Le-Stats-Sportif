from app import webserver
from flask import request, jsonify
import re

import os
import json

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    print(f"JobID is {job_id}")
    # TODO
    # Check if job_id is valid
    value = re.search(r'\d+', job_id).group()

    if int(value) < 1 or int(value) > (webserver.job_counter - 1):
        return jsonify({
            'status': 'error',
            'reason': 'Invalid job_id'
        }), 500

    file_path = f"results/{value}.json"

    if os.path.isfile(file_path):
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        return jsonify({
            'status': 'done',
            'data': data
        }), 200 
    else:
        return jsonify({
            'status': 'running'
        }), 200

@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():
    result = 0
    for i in range(1, webserver.job_counter):
        file_path = f"results/{i}.json"
        if not os.path.isfile(file_path):
            result += 1

    return jsonify({
            'num_jobs': result
        }), 200 

@webserver.route('/api/jobs', methods=['GET'])
def get_jobs():
    result = {}
    for i in range(1, webserver.job_counter):
        file_path = f"results/{i}.json"
        if os.path.isfile(file_path):
            result[f"job_id_{i}"] = "done"
        else:
            result[f"job_id_{i}"] = "running"

    return jsonify({
            'status': 'done',
            'data': result
        }), 200 

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def stop_server():
    webserver.tasks_runner.stop()

    return jsonify({
            'status': 'done'
        }), 200 

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    # Get request data
    data = request.json

    # TODO
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    request_type = "states_mean"

    webserver.tasks_runner.add_task((webserver.job_counter - 1, request_type, data))

    # Return associated job_id
    return jsonify({'job_id': job_id}), 200

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    # TODO
    # Get request data
    data = request.json

    # Register job. Don't wait for task to finish
    # Increment job_id counter
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    request_type = "state_mean"

    webserver.tasks_runner.add_task((webserver.job_counter - 1, request_type, data))

    # Return associated job_id
    return jsonify({'job_id': job_id}), 200


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    # Get request data
    data = request.json

    # TODO
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    request_type = "best5"

    webserver.tasks_runner.add_task((webserver.job_counter - 1, request_type, data))

    # Return associated job_id
    return jsonify({'job_id': job_id}), 200

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    # Get request data
    data = request.json

    # TODO
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    request_type = "worst5"

    webserver.tasks_runner.add_task((webserver.job_counter - 1, request_type, data))

    # Return associated job_id
    return jsonify({'job_id': job_id}), 200

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    # Get request data
    data = request.json

    # TODO
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    request_type = "global_mean"

    webserver.tasks_runner.add_task((webserver.job_counter - 1, request_type, data))

    # Return associated job_id
    return jsonify({'job_id': job_id}), 200

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    # Get request data
    data = request.json

    # TODO
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    request_type = "diff_from_mean"

    webserver.tasks_runner.add_task((webserver.job_counter - 1, request_type, data))

    # Return associated job_id
    return jsonify({'job_id': job_id}), 200

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    # Get request data
    data = request.json

    # TODO
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    request_type = "state_diff_from_mean"

    webserver.tasks_runner.add_task((webserver.job_counter - 1, request_type, data))

    # Return associated job_id
    return jsonify({'job_id': job_id}), 200

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    data = request.json

    # TODO
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    request_type = "mean_by_category"

    webserver.tasks_runner.add_task((webserver.job_counter - 1, request_type, data))

    # Return associated job_id
    return jsonify({'job_id': job_id}), 200

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    data = request.json

    # TODO
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    request_type = "state_mean_by_category"

    webserver.tasks_runner.add_task((webserver.job_counter - 1, request_type, data))

    # Return associated job_id
    return jsonify({'job_id': job_id}), 200

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
