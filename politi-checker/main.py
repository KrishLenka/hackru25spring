from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import logging
from openai import OpenAI

# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your actual OpenRouter API key
OPENROUTER_API_KEY = "<API-KEY>"

# Initialize OpenAI client (OpenRouter)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

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

# Function to send text to OpenRouter API (via OpenAI) for analysis
def analyze_text_with_openrouter(text: str) -> dict:
   """Send text to OpenRouter API for analysis."""
   try:
       completion = client.chat.completions.create(
           extra_headers={
               "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional: Site URL for rankings on openrouter.ai.
               "X-Title": "<YOUR_SITE_NAME>",  # Optional: Site title for rankings on openrouter.ai.
           },
           model="deepseek/deepseek-r1:free",  # Specify the DeepSeek model (if necessary)
           messages=[
               {"role": "user", "content": text}
           ]
       )
       result = completion.choices[0].message.content
       return result
   except Exception as e:
       logger.error(f"OpenRouter API error: {str(e)}")
       raise HTTPException(status_code=500, detail=f"OpenRouter API error: {str(e)}")

# Function to analyze text for extremity, subjectivity, and accuracy
def fact_check_text_data(text: str) -> dict:
   """Analyze text for extremity, subjectivity, and fact-checking"""
   try:
       # Call OpenRouter API for the analysis of the text
       analysis_result = analyze_text_with_openrouter(text)

       # Example of a response format (adjust according to the actual response from OpenRouter API)
       # Assuming the response contains extremity, subjectivity, and accuracy.
       extremity = "Moderate"  # Placeholder, replace with actual parsing from the OpenRouter result
       subjectivity = "High"   # Placeholder, replace with actual parsing from the OpenRouter result
       accuracy = "Unverified"  # Placeholder, replace with actual parsing from the OpenRouter result

       return {
           "extremity": extremity,
           "subjectivity": subjectivity,
           "accuracy": accuracy,
           "source_text": text,
           "analysis_result": analysis_result  # Add the detailed analysis result from OpenRouter
       }
   except Exception as e:
       logger.error(f"Error processing text: {str(e)}")
       raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")
