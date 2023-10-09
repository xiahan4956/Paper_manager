
import re
import pandas as pd
import os
import sys

sys.path.append(os.getcwd())
from utils.claude import ask_claude
from utils.gpt import ask_gpt

import dotenv
dotenv.load_dotenv()

MODEL = os.getenv("MODEL")


def get_paper_idea(paper_info,quesion):
    '''
    Use AI to add the idea of the paper
    You could change the question to ask AI
    '''
    
    # To ask AI,fistly we need to define the question
    pmt = '''
    <paper_info>
    {paper_info}
    </paper_info>
    
    {question}
    
    Return:
    ```
    <res>
    your answer
    </res>
    ```

    '''.format(paper_info=paper_info,question=quesion)

    # Then ask 
    if "claude" in MODEL:
        answer = ask_claude(pmt)
    if "gpt" in MODEL:
        answer = ask_gpt(pmt)
    
    # Next, we need to parse the answer,mutiline
    try:
        idea = re.search("<res>(.*?)</res>",answer,re.S).group(1)
    except Exception as e:
        print("parse ieas fail")
        idea = ""
    
    return idea
    

