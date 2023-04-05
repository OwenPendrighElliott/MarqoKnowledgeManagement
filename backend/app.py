from flask import Flask
from flask import request
from flask_cors import CORS 

import marqo 

from postprocessing import converse

from typing import List

app = Flask(__name__)
CORS(app)

INDEX_NAME = "knowledge-management"
CLIENT = marqo.Client("http://localhost:8882")
KNOWLEDGE_ATTR = "knowledge"

@app.route("/getKnowledge", methods=["POST"])
def get_knowledge():
    data = request.get_json()

    q: str = data.get('q')
    conversation: List[str] = data.get('conversation')
    limit = data.get('limit')

    results = CLIENT.index(INDEX_NAME).search(q=q, limit=limit if limit else 3)

    texts = [r[KNOWLEDGE_ATTR] for r in results['hits']]

    eloquent_response = converse(q, conversation, texts)

    return {"text": eloquent_response}

@app.route("/addKnowledge", methods=["POST"])
def add_knowledge():
    data = request.get_json()

    document = data.get('document')

    CLIENT.index(INDEX_NAME).add_documents([
        {KNOWLEDGE_ATTR: document}
    ])

    return {"message": "Knowledge added successfully"}
