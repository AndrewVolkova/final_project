import requests
from scipy.stats import boxcox
import pickle
from django.shortcuts import render
from .forms import PredictionForm
import logging

# Set up logging
logger = logging.getLogger(__name__)



# BATHS
# Define known values and their corresponding categories
baths_values = ['2.0', '3.0', '4.0', '1.0', '2.5', '3.5', '1.5', '5.0',
                '1.75', '2.25', '1.25', '4.5', '6.0', '7.0', '8.0']
bath_categories = [4, 7, 10, 0, 6, 8, 2, 12, 3, 5, 1, 11, 13, 14, 15]

# Convert known values to float for comparison
baths_values_float = list(map(float, baths_values))

# END BATHS DATA 
# 
# BEDS
# Define known values and their corresponding categories
beds_values = ['3.0', '4.0', '2.0', '5.0', '1.0', '6.0', '0.0',
                '7.0', '8.0']
beds_categories = [3, 4, 2, 5, 1, 6, 0, 7, 8]

# Convert known values to float for comparison
beds_values_float = list(map(float, beds_values))

# END BEDS DATA 
# 


def map_to_closest_category_bath(value):
    threshold = 0.5  # Define a threshold to determine if the value is too far from known values
    closest_category = 17  # Default category if the value is too far
    min_diff = float('inf')

    for i, known_value in enumerate(baths_values_float):
        diff = abs(value - known_value)
        if diff < min_diff:
            min_diff = diff
            closest_category = bath_categories[i]

    if min_diff > threshold:
        closest_category = 17

    return closest_category

def map_to_closest_category_beds(value):
    threshold = 1  # Define a threshold to determine if the value is too far from known values
    closest_category = 10  # Default category if the value is too far
    min_diff = float('inf')

    for i, known_value in enumerate(beds_values_float):
        diff = abs(value - known_value)
        if diff < min_diff:
            min_diff = diff
            closest_category = beds_categories[i]

    if min_diff > threshold:
        closest_category = 10

    return closest_category

with open('../data/boxcox_lambda.pkl', 'rb') as f:
    lambda_sqft = pickle.load(f)

def transform_sqft(input_sqft, lambda_sqft):
    # Apply the Box-Cox transformation
    transformed_sqft = boxcox(input_sqft + 1, lmbda=lambda_sqft)
    return transformed_sqft


def predict(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            baths = map_to_closest_category_bath(data['baths'])
            beds = map_to_closest_category_beds(data['beds'])
            features = [
                int(data['fireplace']),
                int(data['city']),
                int(data['zipcode']),
                int(data['state']),
                int(data['status_category']),
                int(data['private_pool']),
                int(data['property_type']),
                baths,    
                beds,
                int(data['year']),
                int(data['remodeled']),
                
                int(data['heating']),
                int(data['cooling']),
                int(data['parking']),
                int(data['lotsize']),
                int(data['school_distance']),
                int(data['school_quantity']),
                transform_sqft(float(data['sqft']) + 1, lambda_sqft),
                int(data['stories']),


            ]
            try:
                logger.debug(f"Sending data to Flask API: {features}")
                response = requests.post('http://localhost:8888/predict', json=features)
                response.raise_for_status()
                prediction = response.json().get('prediction')
                logger.debug(f"Received prediction: {prediction}")
                return render(request, 'predictor/result.html', {'prediction': prediction})
            except requests.exceptions.RequestException as e:
                logger.error(f"RequestException: {e}")
                if e.response is not None and e.response.json().get('error'):
                    error_message = e.response.json().get('error')
                else:
                    error_message = 'Error occurred during prediction. Check server logs for more details.'
                return render(request, 'predictor/predict.html', {'form': form, 'error': error_message})
            except ValueError as e:
                logger.error(f"ValueError: {e}")
                return render(request, 'predictor/predict.html', {'form': form, 'error': 'Error parsing the response. Check server logs for more details.'})
        else:
            logger.error(f"Form validation failed: {form.errors}")
            return render(request, 'predictor/predict.html', {'form': form, 'error': 'Form validation failed. Please correct the errors and try again.'})
    else:
        form = PredictionForm(initial={
                                        'fireplace':0,
                                        'city':14,
                                        'state':4,
                                        'status_category': 5,
                                        'private_pool': 0,
                                        'property_type' : 7,
                                        'year' : 166,
                                        'remodeled' : 0,
                                        'heating' : 0,
                                        'cooling' : 1,
                                        'parking' : 0,
                                        'school_distance' : 4,
                                        'school_quantity' : 3,
                                        'stories' : 0,
                                        })
    return render(request, 'predictor/predict.html', {'form': form})