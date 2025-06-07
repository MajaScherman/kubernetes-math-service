# locustfile.py
from locust import HttpUser, task, between
import json

class MathServiceUser(HttpUser):
    """
    User class that does a POST request to the math-service.
    """
    # Simulate user think time between requests.
    # This means each "user" will wait between 1 and 2 seconds after completing a request
    # before making the next one. Adjust as needed.
    wait_time = between(1, 2)

    # The host should be set when running locust, e.g.:
    # locust -H http://a696433661b4249bbb423c18b7bab074-139383333.eu-west-2.elb.amazonaws.com/

    @task
    def add_numbers(self):
        """
        Sends a POST request to the / endpoint with sample data.
        """
        payload = {"a": 10, "b": 5}
        headers = {"Content-Type": "application/json"}
        # The '/' path refers to the root endpoint of your FastAPI service
        response = self.client.post("/", data=json.dumps(payload), headers=headers)

        # Optional: Add validation if response is not 200 OK
        if response.status_code != 200:
            print(f"Request failed with status code: {response.status_code}, response: {response.text}")
        else:
            # You can also add assertions for the response content if desired
            pass