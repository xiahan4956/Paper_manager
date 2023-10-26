import sqlite3
import pandas as pd
import os
import sys
from tqdm import tqdm
from dotenv import load_dotenv
import time


sys.path.append(os.getcwd())
from utils.claude import ask_claude
from paper.ai_info_adder.ai_idea import get_paper_idea

load_dotenv()
MODEL = os.getenv("MODEL")
PAPER_TABLE = os.getenv("PAPER_TABLE")

def run_translation():

    # read the paper
    conn = sqlite3.connect("data/paper.db")
    df = pd.read_sql(f"select * from {PAPER_TABLE}",conn)
    
    # Then,add ai idea to each paper
    for i in tqdm(range(len(df))):
        # get paper info. 
        if "content_cn" in df.columns:
            if pd.notnull(df.loc[i,"content_cn"]):
                continue
        
        # 翻译摘要
        abstarct_en = str(df.loc[i,"abstract"])
        pmt = '''   
        <abstarct_en>
        {abstarct_en}
        </abstarct_en>
        
        以上是论文的摘要,请直接翻译为中文,不要说多余的话,直接给结果
        '''.format(abstarct_en=abstarct_en)
        abstract_cn = ask_claude(pmt,model="claude-instant-1.2")

        # 翻译内容
        content_en = str(df.loc[i,"content"])
        if len(content_en) > 80000:
            continue

        
        # 分段翻译,每段500字
        content_cn = ""
        for j in tqdm(range(0,len(content_en),3000)):
            pmt = '''   
            <content_en>
            {content_en}
            </content_en>
            
            以上是论文的内容,请直接翻译为中文,不要说多余的话,直接给结果,可能有乱码,这种直接跳过
            '''.format(content_en=content_en[j:j+2500])
            content_cn += ask_claude(pmt,model="claude-instant-1.2")
        
        # update到数据库
        while True:
            try:
                sql = "UPDATE {PAPER_TABLE} SET content_cn=?, abstract_cn=? WHERE title=?".format(PAPER_TABLE=PAPER_TABLE)
                params = (content_cn, abstract_cn, df.loc[i, "title"])
                cursor = conn.cursor()
                cursor.execute(sql, params)
                conn.commit() 
                print("保存了一条数据")
                break
            except Exception as e:
                print("数据库可能死锁",e)
                time.sleep(10)


if __name__ == "__main__":
    while True:
        run_translation()


        