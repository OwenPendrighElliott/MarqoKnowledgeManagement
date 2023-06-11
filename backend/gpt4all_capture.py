from gpt4all import GPT4All
import sys

model = GPT4All("ggml-gpt4all-j-v1.3-groovy")
message = sys.argv[1]
messages = []
print( "Prompt: " + message )
messages.append({"role": "user", "content": message})
full_prompt = model._build_prompt(messages, True, True)
response_tokens = []
token_ids = []
def local_callback(token_id, response):
    decoded_token = response.decode('utf-8')
    response_tokens.append( decoded_token )
    token_ids.append(token_id)
    # yield 
    # Do whatever you want with decoded_token here.
    print("Got token:", response)

    return True

model.model._response_callback = local_callback
model.model.generate(full_prompt, streaming=False)
response = ''.join(response_tokens)
print ( "Response: " + response )
messages.append({"role": "assistant", "content": response})
print(token_ids)
# At this point, you can get another prompt from the user, re-run "_build_prompt()", and continue the conversation.