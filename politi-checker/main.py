from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import deepseek
import json

app = FastAPI()

# Initialize DeepSeek API client (replace with your DeepSeek R1 API credentials)
deepseek_client = deepseek.get_client(api_key="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")

class TextInput(BaseModel):
    text: str

class LinkInput(BaseModel):
    url: str

@app.post("/fact-check-text")
async def fact_check_text(input: TextInput):
    text = input.text
    # Process the text for extremity, subjectivity, and accuracy
    result = fact_check_text_data(text)
    return result

@app.post("/fact-check-link")
async def fact_check_link(input: LinkInput):
    url = input.url
    text = get_text_from_url(url)
    # Process the extracted text for extremity, subjectivity, and accuracy
    result = fact_check_text_data(text)
    return result

def get_text_from_url(url: str) -> str:
    """Extract text content from a URL"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, "html.parser")

        # Assuming that the article content is inside <article> tags or similar
        paragraphs = soup.find_all('p')
        text_content = " ".join([p.get_text() for p in paragraphs])
        return text_content
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching URL: {str(e)}")

def fact_check_text_data(text: str) -> dict:
    """Analyze text for extremity, subjectivity, and fact-checking"""
    # Using DeepSeek API to analyze the text
    try:
        # Call DeepSeek API for the analysis of the text
        analysis = deepseek_client.analyze(text=text)

        # Extract relevant information from the response
        extremity = analysis.get("extremity", "Not available")
        subjectivity = analysis.get("subjectivity", "Not available")
        accuracy = analysis.get("accuracy", "Not available")

        # You could add a separate fact-checking process if required here (e.g., comparing with a database of known facts)

        return {
            "extremity": extremity,
            "subjectivity": subjectivity,
            "accuracy": accuracy,
            "source_text": text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")
