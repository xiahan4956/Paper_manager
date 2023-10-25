import sqlite3
import pandas as pd
import os
import sys
from tqdm import tqdm
from dotenv import load_dotenv
import time

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
        if "idea" in df.columns:
            if pd.notnull(df.loc[i,"idea"]):
                continue
        
        if "content" in df.columns:
            if pd.isnull(df.loc[i,"content"]):
                continue
        # Claude could input 10k works,so we could input the paper's meta data or content
        # But GPT could only input limited words,so we could only input the paper's meta data
        if "gpt" in MODEL:
            paper_info = df.iloc[i][["title","abstract"]].to_csv(escapechar='\\')
        if "claude" in MODEL:
            paper_info = df.iloc[i][["title","abstract","cont uent"]].to_csv(escapechar='\\')[0:80000]
            
        # get ai idea

        q1 = "请详细的说明,文章最想表达的观点是什么,结果是什么,举出具体的数据."
        idea1 = get_paper_idea(paper_info,q1)
        q2 = '''具体说说要解决的问题和实现方案吧.
                - 先用面向新手的描述,再用专业的描述论文实现过程.
                - 面向新手的描述是 简单容易懂的话,一点专业术语都不加
                - 专业的话指论文使用的描述手法
                - 结合文中的游戏例子描述,要足够生动'''
        idea2 = get_paper_idea(paper_info,q2)
        q3 = '''请详细的说明,文章的方法的名字,如何运作.并且指出最关键的方法'''
        idea3 = get_paper_idea(paper_info,q3)
        idea = "## " + q1 + "\n" + idea1 + '\n' + "## " + q2 + "\n" + idea2 + '\n' + "## " + q3 + "\n" + idea3

        
        # save to db
        # df.to_sql(PAPER_TABLE,conn,if_exists="replace",index=False)
        while True:
            try:
                cursor = conn.cursor()
                cursor.execute(f"UPDATE {PAPER_TABLE} SET idea = ?  WHERE title = ?",
                            (idea, df.loc[i].get('title')))
                conn.commit()
                break
            except Exception as e:
                print("database may deadlock", e)
                time.sleep(10)

        
    print(f"add ai idea to paper done")
    
if __name__ == "__main__":
    while True:
        run_add_ai_idea()


        