import openai
import time
import dotenv
import os
dotenv.load_dotenv()


CLAUDE_KEY = os.getenv("OPENAI_KEY")
MODEL = os.getenv("MODEL")

def ask_gpt(pmt):
    pmt = [{"role": "user","content":pmt}]
    
    while True:
        try:
            res =  openai.ChatCompletion.create(
            model=MODEL,
            messages=pmt,
            temperature=0,
            timeout = 10
            )
            idea =   res["choices"][0]["message"]["content"]
            
            return idea
        
        except Exception as e:
            print(e)
            time.sleep(1)

