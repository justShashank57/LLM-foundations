from dotenv import load_dotenv
from openai import OpenAI
from schema import tools
from tools import TOOLS_MAP
import os
import json

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
        output_item = response.output[0]
        
        # Check if this is a tool call by checking the type name or attributes
        if type(output_item).__name__ == 'ResponseFunctionToolCall' or hasattr(output_item, 'name'):
            tool_name = output_item.name
            call_id = output_item.call_id
            # Parse tool arguments if they're a JSON string
            if isinstance(output_item.arguments, str):
                tool_args = json.loads(output_item.arguments)
                arguments_str = output_item.arguments
            else:
                tool_args = output_item.arguments
                arguments_str = json.dumps(tool_args)
            print(f"[INFO] Tool call: {tool_name} with args {tool_args}")
            result = TOOLS_MAP[tool_name](**tool_args)

            messages.append({
                "type":"function_call",
                "name": tool_name,
                "arguments": arguments_str,
                "call_id": call_id
            })

            messages.append({
                "type":"function_call_output",
                "name": tool_name,
                "output": str(result),
                "call_id": call_id
            })
        else:
            # final answer from the agent
            if hasattr(output_item, 'content') and output_item.content:
                return output_item.content[0].text
            elif hasattr(output_item, 'text'):
                return output_item.text
            else:
                return str(output_item)

        
