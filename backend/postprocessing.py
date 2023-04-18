from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

from dotenv import load_dotenv

from typing import List, Union

from knowledge_store import MarqoKnowledgeStore

load_dotenv()

LLM = ChatOpenAI(temperature=0.8, model_name="gpt-3.5-turbo")

QUESTIONER = """
Given the conversation, write the best possible question for a domain expert. Don't answer the human - just write a question that would best allow a domain expert to then answer on your behalf.
Assume that the domain expert can always answer the question and will help the human.
If there is no question that is related to last message from the human then just say "PASS".
"""

ANSWERER = """
You are a helpful and friendly AI assistant, your goal is to provide factual responses to the human.
The conversation will contain system messages that begin with "CONTEXT:", these messages contain truthful information that should be used to answer the human.
If you cannot find the answer in CONTEXT then apologise to the human and help them to refine their question.
"""


def make_query(conversation: List[Union[AIMessage, HumanMessage]]) -> str:
    conversation = conversation + [SystemMessage(content=QUESTIONER)]
    ai_message = LLM(conversation)
    return ai_message.content


def make_answer(conversation: List[Union[SystemMessage, AIMessage, HumanMessage]]) -> str:
    conversation = [SystemMessage(content=ANSWERER)] + conversation
    ai_message = LLM(conversation)
    return ai_message.content


def converse(user_input: str, conversation: List[str], mks: MarqoKnowledgeStore, limit: int) -> str:
    llm_conversation = []
    for i in range(len(conversation[-16:])):
        if i % 2:
            msg = AIMessage(content=conversation[i])
        else:
            msg = HumanMessage(content=conversation[i])
        llm_conversation.append(msg)

    llm_conversation.append(HumanMessage(content=user_input))

    query = make_query(llm_conversation)
    print("QUERY:")
    print(query)
    print()

    if not query.startswith("PASS"):
        context = mks.query_for_content(query, "text", limit if limit else 10)
        llm_conversation.append(SystemMessage(content="CONTEXT: " + ". ".join(context)))

    answer = make_answer(llm_conversation)

    return answer
