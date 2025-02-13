import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re

OLLAMA_API_URL = "http://localhost:11434/api/generate"

@csrf_exempt
def generate_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt", "")

            if not prompt:
                return JsonResponse({"error": "Prompt is required"}, status=400)

            ollama_request = {
                "model": "jeritjoshy/recipegenv2",  # Change to your actual model name
                "prompt": prompt,
                "stream": False
            }

            response = requests.post(OLLAMA_API_URL, json=ollama_request)

            if response.status_code != 200:
                return JsonResponse({"error": "Ollama API request failed", "details": response.text}, status=500)

            try:
                ollama_response = response.json()
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON response from Ollama API"}, status=500)

            # Extract response text
            raw_text = ollama_response.get("response", "")

            # Process and structure the response
            structured_data = extract_sections(raw_text)

            return JsonResponse({"response": structured_data})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format in request"}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": f"Ollama request failed: {str(e)}"}, status=500)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def extract_sections(text):
    """
    Extracts different sections from the recipe response.
    Splits the text into 'Title', 'Ingredients', and 'Instructions'.
    """
    sections = {
        "title": [],
        "ingredients": [],
        "instructions": []
    }

    # Find title (first line)
    lines = text.strip().split("\n")
    if lines:
        sections["title"] = [lines[0]]  # Title as an array

    # Extract Ingredients and Instructions using regex
    ingredients_pattern = re.search(r"(?i)Ingredients:\n(.*?)(?:\n\n|$)", text, re.DOTALL)
    instructions_pattern = re.search(r"(?i)Instructions:\n(.*)", text, re.DOTALL)

    # Process Ingredients
    if ingredients_pattern:
        ingredients_text = ingredients_pattern.group(1).strip()
        sections["ingredients"] = [line.strip("- ") for line in ingredients_text.split("\n") if line.strip()]

    # Process Instructions
    if instructions_pattern:
        instructions_text = instructions_pattern.group(1).strip()
        sections["instructions"] = [line.strip("1234567890. ") for line in instructions_text.split("\n") if line.strip()]

    return [sections]  # Wrap the dictionary inside a list
