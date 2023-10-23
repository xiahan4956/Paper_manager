import sqlite3
import pandas as pd
import os
import sys
from tqdm import tqdm
from dotenv import load_dotenv

sys.path.append(os.getcwd())
from paper.ai_info_adder.ai_idea import get_paper_idea

load_dotenv()
MODEL = os.getenv("MODEL")
PAPER_TABLE = os.getenv("PAPER_TABLE")

def run_add_ai_idea():
    '''
    Add AI idea to the paper by paper's meta data or content
    you could define any question to ask AI    
    '''
    
    print("start add ai idea to paper")
    
    # read the paper
    conn = sqlite3.connect("data/paper.db")
    df = pd.read_sql(f"select * from {PAPER_TABLE}",conn)
    
    # Then,add ai idea to each paper
    for i in tqdm(range(len(df))):
        # get paper info. 
        

        # Claude could input 10k works,so we could input the paper's meta data or content
        # But GPT could only input limited words,so we could only input the paper's meta data
        if "gpt" in MODEL:
            paper_info = df.iloc[i][["title","abstract"]].to_csv()
        if "claude" in MODEL:
            paper_info = df.iloc[i][["title","abstract","content"]].to_csv()
            
        # get ai idea
        idea = get_paper_idea(paper_info,"What is the main idea of this paper?Give detail data if you can.")
        df.loc[i,"idea"] = idea

        """
        # In there you could add more ai info by coy and paste the above code,just change the question and the variable name
        # idea2 = add_paper_idea(paper_info,"What is the idea of this paper?")
        # df.loc[i,"idea2"] = idea2
        """
        
        # save to db
        df.to_sql(PAPER_TABLE,conn,if_exists="replace",index=False)
        
    print(f"add ai idea to paper done")
    
if __name__ == "__main__":
    while True:
        run_add_ai_idea()