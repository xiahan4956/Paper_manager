
import json
import anthropic
import time
import dotenv
import os
dotenv.load_dotenv()


CLAUDE_KEY = os.getenv("CLAUDE_KEY")
MODEL = os.getenv("MODEL")

from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

def ask_claude(content):
    client = Anthropic(api_key = CLAUDE_KEY)    
    prompt=f"{HUMAN_PROMPT}{content}{AI_PROMPT}"
    
    while True:
        try:
            response = client.completions.create(
                prompt=prompt,
                model=MODEL,
                temperature = 0,
                max_tokens_to_sample = 500
            )
            break
        except Exception as e:
            time.sleep(3)
            print(e)
            
    print(response.completion)

    return response.completion
