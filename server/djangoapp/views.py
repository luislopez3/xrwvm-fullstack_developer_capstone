# Required imports
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
import logging
import json
from django.views.decorators.csrf import csrf_exempt

from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review
from .models import CarMake, CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create a `login_request` view to handle sign-in request
@csrf_exempt
def login_user(request):
    """Handle user login request."""
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]

    user = authenticate(username=username, password=password)
    response_data = {"userName": username}

    if user is not None:
        login(request, user)
        response_data["status"] = "Authenticated"

    return JsonResponse(response_data)


# Create a `logout_request` view to handle sign-out request
def logout_request(request):
    """Handle user logout request."""
    logout(request)
    return JsonResponse({"userName": ""})


# Create a `registration` view to handle sign-up request
@csrf_exempt
def registration(request):
    """Handle user registration request."""
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data["email"]

    username_exist = User.objects.filter(username=username).exists()

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    else:
        return JsonResponse({"userName": username, "error": "Already Registered"})


# Get a list of dealerships (all by default, filtered by state if provided)
def get_dealerships(request, state="All"):
    """Retrieve and return a list of dealerships."""
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# Render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    """Retrieve and return a dealer's reviews."""
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        for review_detail in reviews:
            try:
                response = analyze_review_sentiments(review_detail["review"])
                review_detail["sentiment"] = response.get("sentiment", "neutral")
            except Exception as e:
                logger.error(f"Error analyzing sentiment: {e}")

        return JsonResponse({"status": 200, "reviews": reviews})

    return JsonResponse({"status": 400, "message": "Bad Request"})


# Render the dealer details
def get_dealer_details(request, dealer_id):
    """Retrieve and return dealer details."""
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})

    return JsonResponse({"status": 400, "message": "Bad Request"})


# Submit a review
def add_review(request):
    """Allow authenticated users to submit a review."""
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception as e:
            logger.error(f"Error posting review: {e}")
            return JsonResponse(
                {"status": 401, "message": "Error in posting review"}
            )

    return JsonResponse({"status": 403, "message": "Unauthorized"})


# Retrieve a list of cars
def get_cars(request):
    """Retrieve and return a list of cars."""
    if CarMake.objects.count() == 0:
        initiate()

    car_models = CarModel.objects.select_related("car_make")
    cars = [
        {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        for car_model in car_models
    ]

    return JsonResponse({"CarModels": cars})
