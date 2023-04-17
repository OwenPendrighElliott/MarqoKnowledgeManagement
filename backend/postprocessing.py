from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

from typing import List 

load_dotenv()


TEMPLATE = """
You will received USER_INPUT from users, given CONTEXT and CONVERSATION you must respond to the best of your ability. 
CONTEXT will contain information related to USER_INPUT, this should help your respond.
Your conversation so far is contained in CONVERSATION, lines in CONVERSATION beginning with 'system:' are you and lines beginning with 'user:' are the user.
Your goal is to have a conversation with the user and only ever use information you can find in the CONTEXT and CONVERSATION when generating responses.
Your responses should be one to five sentences and you should do your best to sound human.

CONTEXT:
=========
{context}
CONVERSATION:
=========
{conversation}
USER_INPUT:
=========
{user_input}
"""

def converse(
    user_input: str,
    conversation: List[str],
    knowledges: List[str], 
) -> str:
    
    context = '. \n'.join(knowledges)

    conversation = '\n'.join(conversation)

    prompt = PromptTemplate(template=TEMPLATE, input_variables=["context", "conversation", "user_input"])
    llm = OpenAI(temperature=0.9,  model_name="gpt3.5-turbo")
    chain_qa = LLMChain(llm=llm, prompt=prompt)
    llm_results = chain_qa(
        {"context": context, "conversation": conversation, "user_input": user_input}, 
        return_only_outputs=True
    )
    return llm_results['text']