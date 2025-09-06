from flask import Flask, render_template, request, jsonify, session, Response
import os

# Import all of our custom logic functions from the ml_logic folder
from ml_logic.predict import get_crop_recommendation
from ml_logic.chat import get_chat_response_stream 
from ml_logic.crop_data import IDEAL_CROP_CONDITIONS


# --- 1. Initialize the Flask Application ---
app = Flask(__name__)
# A secret key is required to securely manage user sessions
app.secret_key = os.urandom(24)

# --- 2. Route Definitions for Web Pages ---

@app.route('/')
def home():
    """Renders the homepage."""
    return render_template('index.html', active_page='home')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Handles prediction and remembers the last result using the session."""
    prediction_text = ""
    if request.method == 'POST':
        try:
            features = {
                'N': float(request.form.get('N')), 'P': float(request.form.get('P')),
                'K': float(request.form.get('K')), 'temperature': float(request.form.get('temperature')),
                'humidity': float(request.form.get('humidity')), 'ph': float(request.form.get('ph')),
                'rainfall': float(request.form.get('rainfall'))
            }
            session['last_input'] = features
            prediction_text = get_crop_recommendation(list(features.values()))
            session['last_prediction'] = prediction_text
        except (ValueError, TypeError):
            prediction_text = "Invalid input. Please enter valid numbers."
            session.pop('last_prediction', None)
    else:
        prediction_text = session.get('last_prediction', None)

    return render_template('predict.html', active_page='predict', prediction=prediction_text)

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    """Handles the reverse crop analysis feature."""
    last_input = session.get('last_input')
    last_prediction = session.get('last_prediction')
    all_crops = sorted(IDEAL_CROP_CONDITIONS.keys())
    report = None
    selected_crop = None

    if request.method == 'POST':
        selected_crop = request.form.get('crop_name')
    elif last_input:
        selected_crop = last_prediction

    if selected_crop and last_input:
        ideal_conditions = IDEAL_CROP_CONDITIONS.get(selected_crop)
        report_data = []
        if ideal_conditions:
            for feature, user_value in last_input.items():
                ideal_low, ideal_high = ideal_conditions[feature]
                status = "Ideal"
                if user_value < ideal_low:
                    status = "Low"
                elif user_value > ideal_high:
                    status = "High"
                
                report_data.append({
                    'feature': feature.title(), 'user_value': user_value,
                    'ideal_range': f"{ideal_low} - {ideal_high}", 'status': status
                })
        report = report_data
    
    return render_template('analysis.html', active_page='analysis', 
                           last_input=last_input, all_crops=all_crops, 
                           last_prediction=last_prediction,
                           selected_crop=selected_crop, report=report)


@app.route('/about')
def about():
    """Renders the about/model details page."""
    return render_template('about.html', active_page='about')

# --- 3. API Endpoint for the Streaming Chatbot ---

@app.route('/chat', methods=['POST'])
def chat():
    """Handles the AJAX request from the chatbot and returns a streaming response."""
    data = request.json
    crop_name = data.get('crop')
    question = data.get('question')
    return Response(get_chat_response_stream(crop_name, question), mimetype='text/event-stream')

# --- 4. Run the Application ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

