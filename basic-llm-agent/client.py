from dotenv import load_dotenv
from openai import OpenAI
from schema import tools
from tools import TOOLS_MAP
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL")
client = OpenAI(api_key=api_key)

def run_agent(user_input):
    messages = [{"role": "user", "content": user_input}]
    while True:
        response = client.responses.create(
                        model=model,
                        input=messages,
                        tools=tools,
                )
        if response.output[0].type == "tool_call":
            tool_call = response.output[0].tool_calls[0]
            tool_name = tool_call.name
            tool_args = tool_call.arguments
            print(f"[INFO] Tool call: {tool_name} with args {tool_args}")
            result = TOOLS_MAP[tool_name](**tool_args)

            messages.append({
                "type":"tool_call",
                "name": tool_name,
                "arguments": tool_args
            })

            messages.append({
                "type":"tool_result",
                "name": tool_name,
                "content": result
            })
        else:
            #final answer from the agent
            return response.output[0].content[0].text

        
