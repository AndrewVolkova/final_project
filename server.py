from flask import Flask, request, jsonify
import pickle
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load the model from the file
with open('data/model.pkl', 'rb') as pkl_file:
    model = pickle.load(pkl_file)

# Create the Flask application
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        logging.debug(f"Received data: {data}")

        # Validate input data
        if not isinstance(data, list) or len(data) != 19:
            raise ValueError("Input data should be a list of 19 elements.")

        features = np.array(data, dtype=float).reshape(1, -1)
        logging.debug(f"Features reshaped: {features}")

        prediction = model.predict(features)
        logging.debug(f"Prediction: {prediction}")

        return jsonify({'prediction': float(prediction[0])})

    except ValueError as e:
        logging.error(f"ValueError: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logging.error(f"Exception: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run('localhost', 8888)
