# from langchain.chat_models import ChatOpenAI
# from langchain.chains import LLMChain
# from langchain.prompts import PromptTemplate
# from langchain.schema import (
#     AIMessage,
#     HumanMessage,
#     SystemMessage
# )

# from dotenv import load_dotenv

# from typing import List

# from knowledge_store import MarqoKnowledgeStore

# load_dotenv()

# BACKGROUND = """
# You are a helpful assistant that aims to answer questions factually and accurately. 
# If asked any question then you must query for information. 
# DO NOT attempt to answer anything without using your 'QUERY:' capability described below.
# Failure to use your database will result in an unhappy user which is against your core directive.
# You can do one of three things:
#     Respond: You can send a message back to the user to answer their question or ask for clarification.
#     Query: Send a query to your database to get more information. Queries can be in natural language - to indicate that you want to query you must preceed your message with 'QUERY:', this will give you more information to work with.

# You cannot query more than twice in a row, this is very important.
# """

# POST_QUERY = """
# You have received information, not more QUERY is allowed. You cannot do it.
# You if the information is available then you may answer, otherwise you must let the user know that you are sorry but you don't have the required information.
# """

# def converse(
#     user_input: str,
#     conversation: List[str],
#     mks: MarqoKnowledgeStore,
#     limit: int
# ) -> str:

#     llm_conversation = [SystemMessage(content=BACKGROUND)]
#     for i in range(len(conversation)):
#         if i%2:
#             msg = AIMessage(content=conversation[i])
#         else:
#             msg = HumanMessage(content=conversation[i])
#         llm_conversation.append(msg)

#     llm_conversation.append(HumanMessage(content=user_input))

#     llm = ChatOpenAI(temperature=0.8,  model_name="gpt-3.5-turbo")

#     ai_message = llm(llm_conversation)

#     content = ai_message.content

#     while content.startswith("QUERY:"):
#         query = content.replace("QUERY:", "")
#         print("QUERY")
#         print(query)
#         print()
#         context = mks.query_for_content(query, "text", limit if limit else 4)
#         print("CONTEXT")
#         print(context)
#         print()
#         llm_conversation.append(SystemMessage(content="CONTEXT: " + '. '.join(context)))
#         llm_conversation.append(SystemMessage(content=POST_QUERY))
#         ai_message = llm(llm_conversation)
#         content = ai_message.content
    
#     return content


from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from dotenv import load_dotenv

from typing import List, Union

from knowledge_store import MarqoKnowledgeStore

load_dotenv()

LLM = ChatOpenAI(temperature=0.8,  model_name="gpt-3.5-turbo")

QUESTIONER = """
Given the conversation, write the best possible question for a domain expert. Don't answer the human - just write a question that would best allow a domain expert to then answer on your behalf.
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

def converse(
    user_input: str,
    conversation: List[str],
    mks: MarqoKnowledgeStore,
    limit: int
) -> str:
    llm_conversation = []
    for i in range(len(conversation)):
        if i%2:
            msg = AIMessage(content=conversation[i])
        else:
            msg = HumanMessage(content=conversation[i])
        llm_conversation.append(msg)

    llm_conversation.append(HumanMessage(content=user_input))

    query = make_query(llm_conversation)
    print("QUERY:")
    print(query)
    print()

    context = mks.query_for_content(query, "text", limit if limit else 4)

    llm_conversation.append(SystemMessage(content="CONTEXT: " + '. '.join(context)))

    answer = make_answer(llm_conversation)

    return answer
