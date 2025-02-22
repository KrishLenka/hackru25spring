from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import requests
from bs4 import BeautifulSoup
import logging
import re

# Initialize FastAPI app
app = FastAPI()

# Allow CORS from frontend React app (localhost:3000)
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set your OpenAI API Key
OPENAI_API_KEY = "<API-KEY>"

# Initialize OpenAI API client
openai.api_key = OPENAI_API_KEY

# Define Pydantic models for input validation
class TextInput(BaseModel):
    text: str

class LinkInput(BaseModel):
    url: str

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Poli API!"}

# Endpoint to fact-check text
@app.post("/fact-check-text")
async def fact_check_text(input: TextInput):
    text = input.text
    if not text:
        raise HTTPException(status_code=400, detail="Text input cannot be empty")
    result = fact_check_text_data(text)
    return result

# Endpoint to fact-check a URL
@app.post("/fact-check-link")
async def fact_check_link(input: LinkInput):
    url = input.url
    if not url:
        raise HTTPException(status_code=400, detail="URL input cannot be empty")
    text = get_text_from_url(url)
    result = fact_check_text_data(text)
    return result

# Function to extract text content from a URL
def get_text_from_url(url: str) -> str:
    """Extract text content from a URL"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract text from <p> tags
        paragraphs = soup.find_all('p')
        text_content = " ".join([p.get_text() for p in paragraphs])
        return text_content
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching URL: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error fetching URL: {str(e)}")

# Function to analyze text extremity
def analyze_extremity(phrase: str) -> str:
    """Analyze extremity of a phrase."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in analyzing text extremity."},
                {"role": "user", "content": f"Analyze the following phrase and give a numerical rating (1-10) for extremity, along with a brief explanation:\n\n{phrase}"}
            ],
            max_tokens=500
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing extremity analysis: {str(e)}")

# Function to analyze text subjectivity
def analyze_subjectivity(phrase: str) -> str:
    """Analyze subjectivity of a phrase."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in analyzing text subjectivity."},
                {"role": "user", "content": f"Analyze the following phrase and give a numerical rating (1-10) for subjectivity/bias, along with a brief explanation:\n\n{phrase}"}
            ],
            max_tokens=500
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing subjectivity analysis: {str(e)}")

# Function to analyze factual accuracy
def analyze_accuracy(phrase: str) -> str:
    """Analyze factual accuracy of a phrase."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in analyzing factual accuracy."},
                {"role": "user", "content": f"Analyze the following phrase and give a numerical rating (1-10) for factual accuracy, along with a brief explanation:\n\n{phrase}"}
            ],
            max_tokens=500
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing accuracy analysis: {str(e)}")

# Function to provide an overall text analysis
def analyze_phrase(phrase: str) -> dict:
    """Analyze a phrase for extremity, subjectivity, and accuracy, and provide an overall summary."""
    try:
        extremity = analyze_extremity(phrase)
        subjectivity = analyze_subjectivity(phrase)
        accuracy = analyze_accuracy(phrase)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in analyzing text meaning and educational value."},
                {"role": "user", "content": f"Provide an overall analysis of the following phrase, including what it can educate about the topic:\n\n{phrase}"}
            ],
            max_tokens=500
        )
        overall_analysis = response['choices'][0]['message']['content'].strip()

        return {
            "phrase": phrase,
            "extremity": extremity,
            "subjectivity": subjectivity,
            "accuracy": accuracy,
            "overall_analysis": overall_analysis
        }
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing overall phrase analysis: {str(e)}")

# Function to extract key phrases from the text
def extract_key_phrases(text: str) -> list:
    """Extract key phrases or sentences from the text."""
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    return sentences[:10]  # Limit to first 10 sentences/phrases

# Function to analyze text for extremity, subjectivity, and factual accuracy
def fact_check_text_data(text: str) -> dict:
    """Analyze text for extremity, subjectivity, and fact-checking."""
    try:
        key_phrases = extract_key_phrases(text)
        analysis_results = [analyze_phrase(phrase) for phrase in key_phrases]

        return {
            "summary": "Overall analysis of provided text with key phrase evaluations.",
            "phrase_analysis": analysis_results,
            "source_text": text
        }
    except Exception as e:
        logger.error(f"Error processing text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")
