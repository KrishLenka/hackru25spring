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
OPENAI_API_KEY = "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"


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


# Function to send text to OpenAI for analysis
def analyze_text_with_openai(text: str) -> dict:
   """Send text to OpenAI API for analysis."""
   try:
       # Use the ChatGPT model (gpt-3.5-turbo) and the /v1/chat/completions endpoint
       response = openai.ChatCompletion.create(
           model="gpt-3.5-turbo",  # The model you're using
           messages=[
               {"role": "system", "content": "You are referencing external sources to assess the credibility of political claims."},  # You can set the system message
               {"role": "user", "content": f"Analyze the following text for extremity, subjectivity, and factual accuracy:\n\n{text}"}  # The user's query
           ],
           max_tokens=150
       )
       return response['choices'][0]['message']['content'].strip()  # Extract the assistant's response
  
   except openai.error.OpenAIError as e:  # Correctly catching OpenAI API errors
       raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
   except Exception as e:
       raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


# Function to analyze individual phrases/sentences
def analyze_phrase(phrase: str) -> dict:
   """Analyze specific phrases for extremity, subjectivity, and factual accuracy."""
   try:
       # Send each phrase for OpenAI analysis
       response = openai.ChatCompletion.create(
           model="gpt-3.5-turbo",
           messages=[
               {"role": "system", "content": "You are a helpful assistant."},
               {"role": "user", "content": f"Analyze the following phrase and give a numerical rating (1-10) for extremity, subjectivity/bias, and factual accuracy:\n\n{phrase}"}
           ],
           max_tokens=100
       )
       result = response['choices'][0]['message']['content'].strip()
       return result
  
   except openai.error.OpenAIError as e:
       raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
   except Exception as e:
       raise HTTPException(status_code=500, detail=f"Error processing phrase: {str(e)}")


# Function to extract key phrases from the text
def extract_key_phrases(text: str) -> list:
   """Extract key phrases or sentences from the text."""
   # Basic sentence tokenization (you can improve this by using NLP models like Spacy)
   sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
   return sentences[:5]  # Limit to first 5 sentences/phrases for example


# Function to analyze text for extremity, subjectivity, and factual accuracy
def fact_check_text_data(text: str) -> dict:
   """Analyze text for extremity, subjectivity, and fact-checking"""
   try:
       # Extract key phrases from the text
       key_phrases = extract_key_phrases(text)
      
       # Analyze each phrase and store the results
       analysis_results = []
       for phrase in key_phrases:
           analysis = analyze_phrase(phrase)
           analysis_results.append({
               "phrase": phrase,
               "analysis": analysis
           })


       # Prepare a summary of the overall text validity
       summary = ""
      
       return {
           "summary": summary,
           "phrase_analysis": analysis_results,
           "source_text": text
       }


   except Exception as e:
       logger.error(f"Error processing text: {str(e)}")
       raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


