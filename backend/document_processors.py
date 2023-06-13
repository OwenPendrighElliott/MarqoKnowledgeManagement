import re
import nltk
from typing import List

CHUNK_SIZE = 1024


def simple_chunker(document: str):
    return [
        {"text": document[i : i + CHUNK_SIZE]}
        for i in range(0, len(document), CHUNK_SIZE)
    ]


def sentence_chunker(text: str) -> List[dict]:
    """Breaks the text at sentence boundaries.

    Args:
        text (str): The input text.

    Returns:
        List[dict]: A list of dictionaries containing text chunks.

    """
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= CHUNK_SIZE:
            current_chunk += sentence
        else:
            chunks.append({"text": current_chunk.strip()})
            current_chunk = sentence

    if current_chunk:
        chunks.append({"text": current_chunk.strip()})

    return chunks


def punctuation_smart_chunker(text: str) -> List[dict]:
    """Breaks the text at appropriate boundaries.

    Args:
        text (str): The input text.

    Returns:
        List[dict]: A list of dictionaries containing text chunks.

    """
    chunks = []
    current_chunk = ""
    pattern = re.compile(r"[\n.;,!?]")

    for line in text.splitlines():
        if len(current_chunk) + len(line) <= CHUNK_SIZE:
            current_chunk += line
        else:
            chunks.append({"text": current_chunk.strip()})
            current_chunk = line

        if pattern.search(line):
            chunks.append({"text": current_chunk.strip()})
            current_chunk = ""

    if current_chunk:
        chunks.append({"text": current_chunk.strip()})

    return chunks

def paragraph_chunker(text: str) -> List[dict]:
    """Breaks the text at paragraph boundaries.

    Args:
        text (str): The input text.

    Returns:
        List[dict]: A list of dictionaries containing text chunks.

    """
    paragraphs = re.split(r'\n\s*\n', text)  # Split by empty lines to identify paragraphs
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) <= CHUNK_SIZE:
            current_chunk += paragraph
        else:
            chunks.append({"text": current_chunk.strip()})
            current_chunk = paragraph

    if current_chunk:
        chunks.append({"text": current_chunk.strip()})

    return chunks


