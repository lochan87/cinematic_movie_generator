from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import time
import google.generativeai as genai

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Configure Gemini API
genai.configure(api_key="AIzaSyDZ8otPEiYmxD7lPEmyQLJSzRPYvl-PFEY")

def safe_generate_completion(prompt: str, max_retries=3) -> str:
    """Safely generate completion with retry logic using Gemini API"""
    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)  # No safety settings
            return response.text.strip() if response and response.text else "No response generated."
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(1)
    
    return "Error generating response."


def generate_movie_concept(concept: str, genre: str):
    """Generate a safe movie concept using Gemini API"""
    title_prompt = f"Generate a creative but family-friendly movie title for a {genre} movie about: {concept}."
    synopsis_prompt = f"Write a concise and engaging synopsis for a {genre} movie about: {concept}. Ensure the content is suitable for all audiences."
    character_prompt = f"Create a main character for a {genre} movie about: {concept}. Make sure the description is family-friendly."

    title = safe_generate_completion(title_prompt)
    synopsis = safe_generate_completion(synopsis_prompt)
    character = safe_generate_completion(character_prompt)

    return {
        "title": title,
        "genre": genre,
        "synopsis": synopsis,
        "main_character": character
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate-movie", methods=["POST"])
def generate_movie():
    data = request.json
    concept = data.get("concept")
    genre = data.get("genre")

    if not concept or not genre:
        return jsonify({"error": "Missing concept or genre"}), 400

    movie_details = generate_movie_concept(concept, genre)
    return jsonify(movie_details)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
