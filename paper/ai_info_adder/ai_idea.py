
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
    
    以上是论文的信息,请你回答下面的问题.
    问题是:{question}
    回答时,详细的写出答案,中文回答
    '''.format(paper_info=paper_info,question=quesion)


    # Then ask 
    print("pmt:"+str(len(pmt)))
    if "claude" in MODEL:
        answer = ask_claude(pmt)
    if "gpt" in MODEL:
        answer = ask_gpt(pmt)
    

    return answer
    

