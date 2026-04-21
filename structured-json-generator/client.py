from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL")

client = OpenAI(api_key=api_key)
def json_generator(user_input, retries=3):
    prompt = f"""
              Extract structured information from the following text.
              Return ONLY VALID JSON. Do not include explanations or additional text.
              Schema:
                {{
                "name": "string",
                "skills": ["string"],
                "experience": "string"
                }}

                Text: {user_input}
             """
    for attempt in range(retries):
        try:
            response = client.responses.create(
                model=model,
                input=prompt,
                temperature=0
            )
            content = response.output[0].content[0].text
            parsed = json.loads(content)
            return parsed
        except Exception as e:
            if retries == attempt + 1:
                print("❌ Failed to parse JSON after retries")
                print("Raw response:", content if 'content' in locals() else "No response")

    return None
