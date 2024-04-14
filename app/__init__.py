"""Module providing server initialization."""

import os
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool

webserver = Flask(__name__)
from app import routes

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
webserver.tasks_runner = ThreadPool(webserver.data_ingestor)

webserver.job_counter = 1
if not os.path.exists('results'):
    os.makedirs('results')
