# app.py
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS # Import CORS
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app) # Enable CORS for all origins and all routes. This is crucial for your browser extension.

# Load the trained model
# Ensure 'phishing_model.pkl' is in the same directory as this script
try:
    with open('phishing_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Phishing model loaded successfully!")
except FileNotFoundError:
    print("Error: 'phishing_model.pkl' not found. Please ensure the model file is in the same directory as app.py")
    # You might want to handle this more gracefully in a production app,
    # e.g., by exiting or by using a dummy model.
    exit()
except Exception as e:
    print(f"Error loading the model: {e}")
    exit()

@app.route('/predict', methods=['POST'])
def predict():
    """
    Receives a URL via POST request, extracts features, and returns
    a prediction (whether it's a phishing site) from the loaded model.
    """
    data = request.json
    url_input = data.get('url')

    # Basic input validation
    if not url_input:
        return jsonify({"error": "No URL provided in the request body."}), 400

    try:
        # --- Feature Extraction (as per your original Streamlit code) ---
        parsed_url = urlparse(url_input)

        # Feature 1: URL Length
        url_length = len(url_input)

        # Feature 2: Check for HTTPS
        # This assumes your model expects 1 for HTTPS, 0 otherwise
        https_value = 1 if parsed_url.scheme == "https" else 0

        # Create the feature vector for prediction
        # The model expects a 2D array, even for a single sample
        features = [[url_length, https_value]]

        # --- Model Prediction ---
        prediction = model.predict(features)

        # Convert prediction to a boolean for a clearer API response
        is_phishing = bool(prediction[0])

        # --- Return Prediction as JSON ---
        return jsonify({
            "url": url_input,
            "is_phishing": is_phishing,
            "message": "Warning! This is a Phishing Website." if is_phishing else "This is a Legitimate Website."
        }), 200

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error during prediction for URL '{url_input}': {e}")
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # Run the Flask application
    # host='0.0.0.0' makes the server accessible from external IPs (useful for testing from another device)
    # port=5000 is the default Flask port
    # debug=True enables reloader and debugger, useful during development
    app.run(host='0.0.0.0', port=5000, debug=True)