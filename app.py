from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import time
from openai import OpenAI

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Configure OpenAI client for LM Studio
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="sk-no-key-required"
)

def safe_generate_completion(prompt: str, max_retries=3) -> str:
    """Safely generate completion with retry logic"""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="llama-2-7b-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(1)
    return "Error generating response."

def generate_movie_concept(concept: str, genre: str):
    """Generate a movie concept"""
    title_prompt = f"Create a catchy title for a {genre} movie about: {concept}"
    synopsis_prompt = f"Write a short synopsis for a {genre} movie about: {concept}"
    character_prompt = f"Create a main character for a {genre} movie about: {concept}"

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
    """Serve the front-end HTML"""
    return render_template("index.html")

@app.route("/generate-movie", methods=["POST"])
def generate_movie():
    """API endpoint to receive concept & genre, return movie details"""
    data = request.json
    concept = data.get("concept")
    genre = data.get("genre")

    if not concept or not genre:
        return jsonify({"error": "Missing concept or genre"}), 400

    movie_details = generate_movie_concept(concept, genre)
    return jsonify(movie_details)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
