🌱 # Grow Guide - Crop Recommendation System

This repository hosts a Python-based web application built with Flask that provides a crop recommendation system. The application leverages machine learning to suggest optimal crops based on various environmental and soil conditions.

## ✨ Features

*   ** Inteligente Crop Recommendations**: Utilizes a pre-trained machine learning model to provide accurate crop suggestions.
*   **🖥️ User-Friendly Interface**: A web-based interface allows users to input conditions and receive recommendations.
*   **📊 Data Analysis**: Includes tools and notebooks for understanding crop-related data.
*   **🚀 Scalable ML Logic**: Modular machine learning components for easy maintenance and updates.

## 📁 Key Components:

*   **`app.py`**: 🌐 The main Flask application file, responsible for setting up routes, handling HTTP requests, integrating with the ML backend, and rendering HTML templates.
*   **`dataset/`**: 🗃️ This directory stores the raw and processed datasets crucial for the machine learning model.
    *   `crop_feasable_conditions.csv`: 📄 Likely contains data on feasible conditions for various crops.
    *   `Crop_recommendation.xls`: 📊 The primary dataset used for training the crop recommendation model.
*   **`ml_logic/`**: 🧠 Encapsulates all machine learning-related functionalities.
    *   `predict.py`: 🔮 Contains the core logic for loading the trained model and making predictions based on user input.
    *   `crop_data.py`: ⚙️ Handles data preprocessing, feature engineering, and potentially data loading for the machine learning model.
    *   `chat.py`: 💬 Potentially implements an interactive chatbot feature or an interface for conversational data input.
    *   `api.env`: 🔑 Stores environment variables and sensitive API keys required for the application's functionality.
*   **`pickle/`**: 📦 This directory stores the serialized machine learning model and preprocessing tools.
    *   `model.pkl`: 🤖 The pre-trained machine learning model, serialized using Python's `pickle` module.
    *   `scaler.pkl`: ⚖️ A serialized data scaler (e.g., StandardScaler) used to transform input features to match the training data's scale.
*   **`requirements.txt`**: 📜 Lists all Python dependencies required to run the application, ensuring a consistent development and deployment environment.
*   **`SRCNOTEBOOK.ipynb`**: 📓 A Jupyter notebook serving as a workspace for data exploration, model training, evaluation, and experimentation.
*   **`static/`**: 🖼️ Contains all static web assets served by the Flask application.
    *   `js/predict.js`: 💡 JavaScript code to enhance the interactivity and user experience of the prediction interface.
    *   `style.css`: 🎨 Cascading Style Sheets for styling the web application, ensuring a modern and responsive design.
    *   `src/hero.png`: 🏞️ An image asset, likely used as a hero image or banner in the application's user interface.
*   **`templates/`**: 📃 Houses the HTML templates rendered by the Flask application to construct the user interface.
    *   `index.html`: 🏠 The main landing page of the application.
    *   `predict.html`: 📈 The page where users can input data and receive crop recommendations.
    *   `analysis.html`: 🔍 Potentially displays data visualizations or analysis results related to crops.
    *   `about.html`: ℹ️ Provides information about the project, its purpose, and its creators.
    *   `base.html`: 🧱 A base template that defines the common structure and layout for other HTML pages.

## Overall Purpose:

The "Grow Guide" repository delivers a comprehensive system for crop recommendation, encompassing data management, robust machine learning model implementation, and a user-friendly web interface for predictions and information dissemination. It aims to assist farmers and agricultural enthusiasts in making informed decisions about crop cultivation.

## Installation

To set up the project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Grow-Guide.git
    cd Grow-Guide
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up environment variables:**
    Create an `api.env` file in the `ml_logic` directory based on your specific needs.

## Usage

To run the Flask application:

1.  **Activate your virtual environment** (if not already active).
2.  **Run the Flask application:**
    ```bash
    python app.py
    ```
3.  Open your web browser and navigate to `http://127.0.0.1:5000/` (or the address shown in your terminal).

## Project Structure

```
.
├── app.py
├── dataset/
│   ├── crop_feasable_conditions.csv
│   └── Crop_recommendation.xls
├── ml_logic/
│   ├── __init__.py
│   ├── __pycache__/
│   ├── api.env
│   ├── chat.py
│   ├── crop_data.py
│   └── predict.py
├── pickle/
│   ├── model.pkl
│   └── scaler.pkl
├── requirements.txt
├── SRCNOTEBOOK.ipynb
├── static/
│   ├── js/
│   │   └── predict.js
│   ├── src/
│   │   └── hero.png
│   └── style.css
└── templates/
    ├── about.html
    ├── analysis.html
    ├── base.html
    ├── index.html
    └── predict.html
```
