import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030"
)
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/"
)


# Method for GET requests to the backend
def get_request(endpoint, **kwargs):
    """Send a GET request to the backend with optional query parameters."""
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"

    request_url = f"{backend_url}{endpoint}?{params}"
    print(f"GET from {request_url}")

    try:
        # Call GET method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        # Handle network exceptions
        print(f"Network exception occurred: {e}")
    finally:
        print("GET request call complete!")


# Function for retrieving sentiments
def analyze_review_sentiments(text):
    """Analyze the sentiment of a review using an external sentiment analyzer."""
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected error: {err}, {type(err)}")
        print("Network exception occurred")


# Method for posting a review
def post_review(data_dict):
    """Send a POST request to insert a new review."""
    request_url = f"{backend_url}/insert_review"

    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")
