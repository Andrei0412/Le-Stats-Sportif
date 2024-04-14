"""Module responsible for unittesting."""

import unittest
import os
import requests
import json

class TestWebserver(unittest.TestCase):
    """Class representing the tester."""

    def test_states_mean(self):
        self.helper_test_endpoint("states_mean")

    def test_state_mean(self):
        self.helper_test_endpoint("state_mean")

    def test_best5(self):
        self.helper_test_endpoint("best5")

    def test_worst5(self):
        self.helper_test_endpoint("worst5")

    def test_global_mean(self):
        self.helper_test_endpoint("global_mean")

    def test_diff_from_mean(self):
        self.helper_test_endpoint("diff_from_mean")

    def test_state_diff_from_mean(self):
        self.helper_test_endpoint("state_diff_from_mean")

    def test_mean_by_category(self):
        self.helper_test_endpoint("mean_by_category")

    def test_state_mean_by_category(self):
        self.helper_test_endpoint("state_mean_by_category")

    def helper_test_endpoint(self, endpoint):
        """The testing method."""
        output_dir = f"tests/{endpoint}/output/"
        input_dir = f"tests/{endpoint}/input/"

        input_file = "in-1.json"
        input_path = os.path.join(input_dir, input_file)
        output_path = os.path.join(output_dir, f"out-1.json")

        with open(input_path, "r") as fin:
            req_data = json.load(fin)

        with open(output_path, "r") as fout:
            ref_result = json.load(fout)

        with self.subTest():
            res = requests.post(f"http://127.0.0.1:5000/api/{endpoint}", json=req_data)
            job_id = res.json()["job_id"]

            try:
                res = requests.get(f"http://127.0.0.1:5000/api/get_results/{job_id}", timeout = 2)
                res.raise_for_status()
            except requests.exceptions.RequestException:
                print(f"Error retrieving results for: {endpoint}")
                return

        received_result = res.json()["result"]
        try:
            assert received_result == ref_result
            print(f"Test passed for: {endpoint}")
        except AssertionError:
            print(f"Test failed for: {endpoint}")
