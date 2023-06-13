from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import marqo
from ai_chat import converse, summarise
from typing import List
from knowledge_store import MarqoKnowledgeStore
import document_processors
from document_processors import simple_chunker
app = Flask(__name__)
CORS(app)

INDEX_NAME = "knowledge-management"
CLIENT = marqo.Client("http://localhost:8882")
KNOWLEDGE_ATTR = "knowledge"
CHUNK_SIZE = 1024

document_processors.CHUNK_SIZE = CHUNK_SIZE

MKS = MarqoKnowledgeStore(CLIENT, INDEX_NAME, document_chunker=simple_chunker)
MKS.reset_index()


def get_document_text(url: str) -> str:
    # Get the HTML content of the webpage
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # Extract the text from the HTML
    text = soup.get_text()
    return text


@app.route("/getKnowledge", methods=["POST"])
def get_knowledge():
    data = request.get_json()
    q: str = data.get("q")
    conversation: List[str] = data.get("conversation")
    limit = data.get("limit")
    # Generate an eloquent response using the extracted text and the current conversation
    # for delta in converse(q, conversation, MKS, limit):
    #     print(delta)

    # eloquent_response = "LLM did stuff"
    # print(data)
    # print(eloquent_response)
    # return {"text": "This is a reponse for the frontend"}
    return Response(
        stream_with_context(converse(q, conversation, MKS, limit)),
        mimetype="text/plain",
    )


@app.route("/summarise", methods=["POST"])
def condense_conversation():
    data = request.get_json()
    conversation: List[str] = data.get("conversation")
    summary = summarise(conversation)
    return {"text": summary}


@app.route("/addKnowledge", methods=["POST"])
def add_knowledge():
    data = request.get_json()

    # Add the document to the knowledge index
    document = data.get("document")
    MKS.add_document(document)

    return {"message": "Knowledge added successfully"}


@app.route("/addWebpage", methods=["POST"])
def add_webpage():
    data = request.get_json()
    url = data["URL"]

    # Extract the text from the webpage and add it to the knowledge index
    document = get_document_text(url)
    MKS.add_document(document)

    return {"message": "Knowledge added successfully"}
