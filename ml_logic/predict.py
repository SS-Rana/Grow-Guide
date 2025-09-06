import pickle
import numpy as np

# --- 1. Load Model, Scaler, and Crop Dictionary ---
# This happens only once when the module is imported, making the app efficient.
try:
    # The file path is relative to the root directory where app.py is run.
    model = pickle.load(open('pickle/model.pkl', 'rb'))
    scaler = pickle.load(open('pickle/scaler.pkl', 'rb'))
except FileNotFoundError:
    print("Error: Model or scaler file not found. Make sure 'model.pkl' and 'scaler.pkl' are in a 'pickle' directory.")
    model = None
    scaler = None

crop_dict = {
    1: 'rice', 2: 'maize', 3: 'jute', 4: 'cotton', 5: 'coconut',
    6: 'papaya', 7: 'orange', 8: 'apple', 9: 'muskmelon', 10: 'watermelon',
    11: 'grapes', 12: 'mango', 13: 'banana', 14: 'pomegranate', 15: 'lentil',
    16: 'blackgram', 17: 'mungbean', 18: 'mothbeans', 19: 'pigeonpeas',
    20: 'kidneybeans', 21: 'chickpea', 22: 'coffee'
}

def get_crop_recommendation(features: list) -> str:
    """
    Takes a list of 7 features, scales them, and returns a crop recommendation.
    """
    if not model or not scaler:
        return "Model not loaded. Cannot make a prediction."

    try:
        # Create a numpy array and reshape it for the model
        input_data = np.array([features])
        
        # Scale the input data to match the model's training data
        scaled_data = scaler.transform(input_data)
        
        # Make a prediction using the machine learning model
        result = model.predict(scaled_data)
        
        # Map the numerical result to a human-readable crop name
        crop_name = crop_dict.get(result[0], "Unknown Crop")
        
        return crop_name

    except Exception as e:
        print(f"Error during prediction: {e}")
        return "An error occurred during prediction."