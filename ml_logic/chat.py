import requests
import os
import json
from dotenv import load_dotenv, find_dotenv

# This line finds and loads the API key from your .env file
load_dotenv(find_dotenv('ml_logic/api.env'))

def get_chat_response_stream(crop_name: str, question: str):
    """
    Requests a streaming response from the Gemini API and yields the text chunks
    as they are generated.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        yield "Error: GEMINI_API_KEY not found in your environment file."
        return

    # The '?alt=sse' part of the URL is what enables streaming
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:streamGenerateContent?key={api_key}&alt=sse"
    
    prompt = (
        f"You are a helpful agricultural expert chatbot. A user is asking about growing '{crop_name}'. "
        f"Their question is: '{question}'. Provide a concise, easy-to-understand answer. "
        "Use simple HTML like <strong> for emphasis or <ul> for lists if it helps clarity."
    )
    
    payload = { "contents": [{"parts": [{"text": prompt}]}], "tools": [{"google_search": {}}] }

    try:
        # The 'stream=True' parameter tells the requests library to handle this as a stream
        with requests.post(api_url, json=payload, headers={'Content-Type': 'application/json'}, stream=True) as response:
            response.raise_for_status()
            # Iterate over the incoming response line by line
            for chunk in response.iter_lines():
                if chunk:
                    decoded_chunk = chunk.decode('utf-8')
                    # The API sends data in a specific "Server-Sent Event" format
                    if decoded_chunk.startswith('data: '):
                        # We extract the JSON part of the event
                        json_data = json.loads(decoded_chunk[6:])
                        # And yield just the text content back to the Flask app
                        yield json_data['candidates'][0]['content']['parts'][0]['text']
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        yield "Sorry, I am unable to connect to the information service."
    except Exception as e:
        print(f"Streaming Error: {e}")
        yield "An unexpected error occurred during streaming."