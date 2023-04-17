from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from dotenv import load_dotenv

from typing import List 

load_dotenv()

BACKGROUND = """
You are a helpful assistant that aims to answer questions factually and accurately.

You can do one of two things:
    Respond: You can send a message back to the user to answer their question or continue the conversation
    Query: Send a query to your database to get more information. Queries can be in natural language - to indicate that you want to query you must preceed your message with QUERY, this will give you more information to work with.

It is important to know that you cannot query more than twice in a row
"""


def converse(
    user_input: str,
    conversation: List[str],
) -> str:

    llm_conversation = [SystemMessage(BACKGROUND)]
    for i in range(len(conversation)):
        if i%2:
            msg = AIMessage(conversation[i])
        else:
            msg = HumanMessage(conversation[i])
        llm_conversation.append(msg)

    llm_conversation.append(HumanMessage(user_input))

    llm = ChatOpenAI(temperature=0.8,  model_name="gpt-3.5-turbo")

    ai_message = llm(llm_conversation)

    content = ai_message.content
    
    return content