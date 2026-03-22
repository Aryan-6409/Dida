import os
import time
from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("AIzaSyDMOG0We0wCSWuWs4idtzmaidal6XCM20o")

if not api_key:
    raise ValueError("No GOOGLE_API_KEY found. Check your .env file or GitHub Secrets.")

client = genai.Client(api_key=api_key)
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

    for attempt in range(3):
        try:
            prompt = f"You are a friendly friend. Talk in Hinglish. user says: {user_input}"
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt
            )
            if response and response.text:
                return response.text
        except Exception as e:
            print(f"Error on attempt {attempt}: {e}")
            time.sleep(2 ** (attempt + 1))
            continue

    return "Error: System busy. Please try again later."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
