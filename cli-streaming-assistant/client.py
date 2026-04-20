from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL")

client = OpenAI(api_key=api_key)

def stream_chat(prompt):
    stream = client.responses.stream(
                    model="gpt-5.4",
                    input=prompt
                )
    full_response = ""
    
    with stream as s:
        for event in s:
             if event.type == "response.output_text.delta":
                token = event.delta
                print(token, end="", flush=True)
                full_response += token
    print()
    return full_response