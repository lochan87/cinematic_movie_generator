from openai import OpenAI
from dataclasses import dataclass
from typing import List, Dict, Optional
import json
import time

# Configure OpenAI client for LM Studio
client = OpenAI(
    base_url="http://localhost:1234/v1",  # LM Studio default port
    api_key="sk-no-key-required"  # LM Studio doesn't need a real key but expects this format
)

def test_api_connection():
    """Test the connection to LM Studio API"""
    try:
        response = client.chat.completions.create(
            model="llama-2-7b-chat",  # LM Studio uses this as default
            messages=[
                {"role": "user", "content": "Hi, are you working?"}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        print("API Test Response:", response.choices[0].message.content)
        return True
    except Exception as e:
        print(f"API Connection Test Failed: {e}")
        return False

def safe_generate_completion(prompt: str, max_retries=3) -> str:
    """Safely generate completion with retry logic and error handling"""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="llama-2-7b-chat",
                messages=[
                    {"role": "system", "content": "You are a creative movie development assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000,
                top_p=0.95,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(1)  # Wait before retry
    return ""

# Test the connection when the script starts
print("Testing API connection...")
if not test_api_connection():
    raise Exception("Failed to connect to LM Studio API. Please check if the server is running on port 1234.")

# Simple test to generate a movie title
test_prompt = "Generate a title for a sci-fi movie about time travel. Just return the title, nothing else."
print("\nTesting title generation...")
test_response = safe_generate_completion(test_prompt)
print(f"Test title generated: {test_response}")

# Now create a simple function to generate a movie concept
def generate_movie_concept(concept: str, genre: str) -> Dict:
    """Generate a simple movie concept using LM Studio's API"""
    
    # Generate title
    title_prompt = f"Create a short, catchy title for a {genre} movie about: {concept}\nRespond with just the title, nothing else."
    title = safe_generate_completion(title_prompt)
    
    # Generate synopsis
    synopsis_prompt = f"Write a brief, engaging synopsis (2-3 sentences) for a {genre} movie about: {concept}"
    synopsis = safe_generate_completion(synopsis_prompt)
    
    # Generate main character
    character_prompt = f"Create one main character for a {genre} movie about: {concept}\nInclude name and brief description."
    character = safe_generate_completion(character_prompt)
    
    return {
        "title": title,
        "genre": genre,
        "synopsis": synopsis,
        "main_character": character,
        "concept": concept
    }

if __name__ == "__main__":

    # Test the movie concept generator
    try:
        concept = "A scientist discovers a way to communicate with plants and learns they have been planning something big"
        genre = "Sci-Fi"
        
        print("\nGenerating movie concept...")
        movie = generate_movie_concept(concept, genre)
        
        print("\nGenerated Movie Concept:")
        print(json.dumps(movie, indent=2))
        
    except Exception as e:
        print(f"Error in main execution: {e}")