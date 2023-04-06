from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

from typing import List 

load_dotenv()


TEMPLATE = """
Please provide a response to the user's prompt (USER_PROMPT) using only the information from the conversation history (CONVERSATION) and context from the knowledge management database (CONTEXT). Do not use any external knowledge sources.

CONTEXT:
{context}

CONVERSATION:
{conversation}

USER_INPUT:
{user_input}

Provide your response here:
"""

def converse(
    user_input: str,
    conversation: List[str],
    knowledges: List[str], 
) -> str:
    
    context = '. \n'.join(knowledges)

    conversation = '\n'.join(conversation)

    prompt = PromptTemplate(template=TEMPLATE, input_variables=["context", "conversation", "user_input"])
    llm = OpenAI(temperature=0.9,  model_name="text-davinci-003")
    chain_qa = LLMChain(llm=llm, prompt=prompt)
    llm_results = chain_qa(
        {"context": context, "conversation": conversation, "user_input": user_input}, 
        return_only_outputs=True
    )
    return llm_results['text']
