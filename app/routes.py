"""Module responsible for handling the requests."""

import re
import fcntl
import os
import json
import logging
from logging.handlers import RotatingFileHandler
from flask import request, jsonify
from app import webserver

handler = RotatingFileHandler(filename = "webserver.log",
                              maxBytes = 10000,
                              backupCount = 10)

logger = logging.getLogger("MyLogger")
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    """Endpoint definition."""
    if request.method == 'POST':
        data = request.json
        response = {"message": "Received data successfully", "data": data}

        return jsonify(response)

    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """Function responsible for handling the /api/get_results request."""
    logger.info("----- Entry for: /api/get_results -----")
    logger.info("Received job_id: %s", job_id)

    value = re.search(r'\d+', job_id).group()

    if int(value) < 1 or int(value) > (webserver.job_counter - 1):
        logger.info("Invalid job_id")
        return jsonify({
            'status': 'error',
            'reason': 'Invalid job_id'
        }), 500

    file_path = f"results/{value}.json"

    if os.path.isfile(file_path):
        with open(file_path, mode = "r", encoding = "utf-8") as json_file:
            try:
                fcntl.flock(json_file, fcntl.LOCK_SH | fcntl.LOCK_NB)
                if os.path.getsize(file_path) > 0:
                    data = json.load(json_file)
                    logger.info("Job is done")
                    return jsonify({
                    'status': 'done',
                    'data': data
                    }), 200
            except IOError:
                logger.info("Job is running")
                return jsonify({
                'status': 'running'
                }), 200

    logger.info("Job is running")
    return jsonify({
                'status': 'running'
                }), 200

@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():
    """Function responsible for handling the /api/num_jobs request."""
    logger.info("----- Entry for: /api/num_jobs -----")

    result = 0
    for i in range(1, webserver.job_counter):
        file_path = f"results/{i}.json"
        if not os.path.isfile(file_path):
            result += 1

    logger.info("Running jobs number: %d", result)
    return jsonify({
            'num_jobs': result
        }), 200

@webserver.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Function responsible for handling the /api/jobs request."""
    logger.info("----- Entry for: /api/jobs -----")
    result = {}
    for i in range(1, webserver.job_counter):
        file_path = f"results/{i}.json"
        if os.path.isfile(file_path):
            result[f"job_id_{i}"] = "done"
        else:
            result[f"job_id_{i}"] = "running"

    logger.info("Jobs sent")
    return jsonify({
            'status': 'done',
            'data': result
        }), 200

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def stop_server():
    """Function responsible for shutting down the server."""
    logger.info("----- Entry for: /api/graceful_shutdown -----")
    webserver.tasks_runner.stop()

    return jsonify({
            'status': 'done'
        }), 200

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """Function responsible for handling the /api/states_mean request."""
    logger.info("----- Entry for: /api/states_mean -----")

    data = request.json
    logger.info(data)
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    request_type = "states_mean"

    webserver.tasks_runner.add_task((webserver.job_counter - 1, request_type, data))

    logger.info("Job_id is: %s", job_id)
    return jsonify({'job_id': job_id}), 200

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """Function responsible for handling the /api/state_mean request."""
    logger.info("----- Entry for: /api/state_mean -----")

    data = request.json
    logger.info(data)
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    request_type = "state_mean"

    webserver.tasks_runner.add_task((webserver.job_counter - 1, request_type, data))

    logger.info("Job_id is: %s", job_id)
    return jsonify({'job_id': job_id}), 200


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """Function responsible for handling the /api/best5 request."""
    logger.info("----- Entry for: /api/best5 -----")

    data = request.json
    logger.info(data)
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    request_type = "best5"

    webserver.tasks_runner.add_task((webserver.job_counter - 1, request_type, data))

    logger.info("Job_id is: %s", job_id)
    return jsonify({'job_id': job_id}), 200

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """Function responsible for handling the /api/worst5 request."""
    logger.info("----- Entry for: /api/worst5 -----")

    data = request.json
    logger.info(data)
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    request_type = "worst5"

    webserver.tasks_runner.add_task((webserver.job_counter - 1, request_type, data))

    logger.info("Job_id is: %s", job_id)
    return jsonify({'job_id': job_id}), 200

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """Function responsible for handling the /api/global_mean request."""
    logger.info("----- Entry for: /api/global_mean -----")

    data = request.json
    logger.info(data)
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    request_type = "global_mean"

    webserver.tasks_runner.add_task((webserver.job_counter - 1, request_type, data))

    logger.info("Job_id is: %s", job_id)
    return jsonify({'job_id': job_id}), 200

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """Function responsible for handling the /api/diff_from_mean request."""
    logger.info("----- Entry for: /api/diff_from_mean -----")

    data = request.json
    logger.info(data)
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    request_type = "diff_from_mean"

    webserver.tasks_runner.add_task((webserver.job_counter - 1, request_type, data))

    logger.info("Job_id is: %s", job_id)
    return jsonify({'job_id': job_id}), 200

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """Function responsible for handling the /api/state_diff_from_mean request."""
    logger.info("----- Entry for: /api/state_diff_from_mean -----")

    data = request.json
    logger.info(data)
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    request_type = "state_diff_from_mean"

    webserver.tasks_runner.add_task((webserver.job_counter - 1, request_type, data))

    logger.info("Job_id is: %s", job_id)
    return jsonify({'job_id': job_id}), 200

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """Function responsible for handling the /api/mean_by_category request."""
    logger.info("----- Entry for: /api/mean_by_category -----")

    data = request.json
    logger.info(data)
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    request_type = "mean_by_category"

    webserver.tasks_runner.add_task((webserver.job_counter - 1, request_type, data))

    logger.info("Job_id is: %s", job_id)
    return jsonify({'job_id': job_id}), 200

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """Function responsible for handling the /api/state_mean_by_category request."""
    logger.info("----- Entry for: /api/state_mean_by_category -----")

    data = request.json
    logger.info(data)
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    request_type = "state_mean_by_category"

    webserver.tasks_runner.add_task((webserver.job_counter - 1, request_type, data))

    logger.info("Job_id is: %s", job_id)
    return jsonify({'job_id': job_id}), 200

@webserver.route('/')
@webserver.route('/index')
def index():
    """Function responsible for showing the user the defined routes."""
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    """Function responsible for retrieving the routes"""
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
