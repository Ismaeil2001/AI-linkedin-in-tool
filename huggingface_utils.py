import os
import requests
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"

HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
}

LABELS = ["HR", "Learning and Development", "Recruitment", "Leadership", "Employee Training"]

def score_relevance(text):
    payload = {
        "inputs": text,
        "parameters": {
            "candidate_labels": LABELS,
            "multi_class": True
        }
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        print(f"Error from Hugging Face API: {response.status_code} — {response.text}")
        return None

    result = response.json()
    scores = result.get("scores", [])
    avg_score = sum(scores) / len(scores) if scores else 0
    scaled_score = round(avg_score * 5, 2)  # Convert to 1–5 scale
    print(f"Relevance score (1–5): {scaled_score}")
    return scaled_score
