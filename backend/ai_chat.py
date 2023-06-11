from gpt4all import GPT4All

from dotenv import load_dotenv

from typing import List, Union

from knowledge_store import MarqoKnowledgeStore

load_dotenv()

class Message():
    role: str
    content: str

LLM = GPT4All("ggml-gpt4all-j-v1.3-groovy")

def make_answer(
    conversation: List[Message]
) -> str:
    resp = LLM.chat_completion(conversation, n_predict=512, n_ctx=2048)
    ai_message = resp["choices"][0]["message"]["content"]

    return ai_message


def converse(
    user_input: str, conversation: List[str], mks: MarqoKnowledgeStore, limit: int
) -> str:
    llm_conversation = []
    for i in range(len(conversation)):
        if i % 2:
            msg = {"role": "assistant", "content": conversation[i]}
        else:
            msg = {"role": "user", "content": conversation[i]}
        llm_conversation.append(msg)

    llm_conversation.append({"role": "user", "content": user_input})

    # context = mks.query_for_content(user_input, "text", limit if limit else 3)
    context = mks.query_for_content(user_input, "text", 2)
    print(len(context))
    llm_conversation.append({"role": "system", "content": "CONTEXT: " + ". ".join(context)})
    answer = make_answer(llm_conversation)
    print(answer)
    return answer


def summarise(conversation: List[str]) -> str:
    llm_conversation = []
    for i in range(len(conversation)):
        if i % 2:
            msg = {"role": "assistant", "content": conversation[i]}
        else:
            msg = {"role": "user", "content": conversation[i]}
        llm_conversation.append(msg)

    llm_conversation.append({"user": "system", "content": "Generate a 3 sentence summary of the conversation before this message."})

    resp = LLM.chat_completion(llm_conversation, n_predict=256, n_ctx=2048)
    ai_message = resp["choices"][0]["message"]["content"]
    return ai_message