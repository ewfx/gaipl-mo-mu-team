from openai import OpenAI
import openai
import requests
from bs4 import BeautifulSoup
import os

# Set up your OpenAI API key
client = OpenAI()

# Function to scrape data from a website
def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except requests.exceptions.RequestException as e:
        print(f"Error scraping website: {e}")
        return None

# Function to process scraped data with OpenAI
def process_with_openai(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": "summarize the content of :"+text
                }
            ]
        )
        
            # instructions="You are a coding assistant that talks like a pirate.",
            # input="How do I check if a Python object is an instance of a class?",
        
    except openai.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
    except openai.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
    except openai.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)
    return response.choices[0].message.content

# Example usage
url = 'https://www.geeksforgeeks.org/python-web-scraping-tutorial/'
scraped_data = scrape_website(url)
if scraped_data:
    processed_data = process_with_openai(scraped_data)
    print(processed_data)
else:
    print("Failed to scrape the website.")