from llama_cpp import Llama

from typing import List, Union

from knowledge_store import MarqoKnowledgeStore


class Message:
    role: str
    content: str


# LLM = Llama(model_path="./models/7B/llama-7b.ggmlv3.q4_1.bin", n_ctx=2048)
LLM = Llama(model_path="./models/7B/Wizard-Vicuna-7B-Uncensored.ggmlv3.q4_K_M.bin", n_ctx=2048)
# LLM = Llama(model_path="./models/13B/llama-13b.ggmlv3.q4_1.bin", n_ctx=2048)
# LLM = Llama(model_path="./models/13B/gpt4-x-alpaca-13b-ggml-q4_0.bin", n_ctx=2048)
# LLM = Llama(model_path="./models/13B/stable-vicuna-13B.ggmlv3.q3_K_L.bin", n_ctx=2048)


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

    llm_conversation.append({"role": "user", "content": "Do you need to search for information to respond accurately (answer only yes or no):"})
    decision: str = LLM.create_chat_completion(llm_conversation, stream=False, max_tokens=2, temperature=0.1)["choices"][0]["message"]["content"]
    print("DECISION:", decision)
    llm_conversation = llm_conversation[:-1]
    if decision.strip().lower().startswith("yes"):
        context = mks.query_for_content(user_input, "text", limit if limit else 3)
        print(len(context))
        print(context)
        llm_conversation.append({"role": "system", "content": "BEGIN CONTEXT:\n" + ". ".join(context) + "\n END CONTEXT\nAssistant, use this to inform your response."})

    for resp in LLM.create_chat_completion(
        llm_conversation, stream=True, max_tokens=256, temperature=0.2
    ):
        if resp["choices"][0]["delta"].get("content") is not None:
            yield resp["choices"][0]["delta"].get("content").encode("utf-8")


def summarise(conversation: List[str]) -> str:
    llm_conversation = []
    for i in range(len(conversation)):
        if i % 2:
            msg = {"role": "assistant", "content": conversation[i]}
        else:
            msg = {"role": "user", "content": conversation[i]}
        llm_conversation.append(msg)

    llm_conversation.append(
        {
            "user": "system",
            "content": "Generate a 3 sentence summary of the conversation before this message.",
        }
    )

    # resp = LLM.chat_completion(llm_conversation, n_predict=256, n_ctx=2048)

    # ai_message = resp["choices"][0]["message"]["content"]
    # return ai_message
