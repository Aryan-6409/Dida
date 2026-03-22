import os
import time
from flask import Flask, render_template, request
from genai import Client  # Correct import for the new google-genai SDK
from dotenv import load_dotenv

# 1. Load environment variables for security
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 2. Initialize the Client
if not api_key:
    raise ValueError("No GOOGLE_API_KEY found in environment variables.")

# The new SDK uses a Client-based approach
client = Client(api_key=api_key)
MODEL_ID = "gemini-2.0-flash"

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form.get("msg")
    if not user_input:
        return "Error: Please enter a message."

    # 3. Retry Logic with Exponential Backoff
    for attempt in range(3):
        try:
            prompt = f"You are a friendly friend. Talk in Hinglish. user says: {user_input}"
            
            # Use the new SDK's client.models.generate_content method
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt
            )
            
            if response and response.text:
                return response.text
            
        except Exception as e:
            # Fixed the syntax error in the print statement from your image
            print(f"Error on attempt {attempt}: {e}")
            
            # Wait longer after each failed attempt (2, 4, 8 seconds)
            time.sleep(2 ** (attempt + 1))
            continue

    return "Error: System busy. Please try again later."

if __name__ == "__main__":
    app.run(debug=True)
