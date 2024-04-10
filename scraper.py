# scraper.py adjustments for handling list return type from loader.load()
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader

# Assuming the UCI EECS department URL
url = "https://www.eecs.uci.edu/"

loader = WebBaseLoader(url)

# Set request parameters if needed, e.g., to bypass SSL verification errors
loader.requests_kwargs = {'verify': False}

# Load the webpage content; expecting a list of documents back
documents = loader.load()

# Assuming the first document in the list is the one we want
document = documents[0] if documents else None

if document:
    # Now we use BeautifulSoup to parse the page content
    soup = BeautifulSoup(document.page_content, 'html.parser')

    # Example of extracting and printing paragraph texts
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        print(paragraph.text)

# Adjust the parsing as needed based on the web page structure to extract relevant info
