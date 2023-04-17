from flask import Flask, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import marqo
from postprocessing import converse
from typing import List

app = Flask(__name__)
CORS(app)

INDEX_NAME = "knowledge-management"
CLIENT = marqo.Client("http://localhost:8882")
KNOWLEDGE_ATTR = "knowledge"
CHUNK_SIZE = 1024 

def add_document(document: str):
    # Add the document to the knowledge index in chunks
    CLIENT.index(INDEX_NAME).add_documents([
        {KNOWLEDGE_ATTR: document[i:i+CHUNK_SIZE]} for i in range(0, len(document), CHUNK_SIZE)
    ])

def get_document_text(url: str) -> str:
    # Get the HTML content of the webpage
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')    
    
    # Extract the text from the HTML
    text = soup.get_text()
    
    return text

@app.route("/getKnowledge", methods=["POST"])
def get_knowledge():
    data = request.get_json()

    q: str = data.get('q')
    conversation: List[str] = data.get('conversation')
    limit = data.get('limit')

    # Search for relevant knowledge in the index
    results = CLIENT.index(INDEX_NAME).search(q=q, limit=limit if limit else 3)

    # Extract the text from the knowledge results
    texts = [r[KNOWLEDGE_ATTR] for r in results['hits']]

    # Generate an eloquent response using the extracted text and the current conversation
    eloquent_response = converse(q, conversation, texts)

    return {"text": eloquent_response}

@app.route("/addKnowledge", methods=["POST"])
def add_knowledge():
    data = request.get_json()

    # Add the document to the knowledge index
    document = data.get('document')
    add_document(document)

    return {"message": "Knowledge added successfully"}

@app.route("/addWebpage", methods=["POST"])
def add_webpage():
    data = request.get_json()
    url = data['URL']

    # Extract the text from the webpage and add it to the knowledge index
    document = get_document_text(url)
    add_document(document)

    return {"message": "Knowledge added successfully"}
