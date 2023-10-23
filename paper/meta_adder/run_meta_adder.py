import os
import sys
import sqlite3
from tqdm import tqdm
sys.path.append(os.getcwd())

import pandas as pd
from paper.meta_adder.meta_data import *

import dotenv
dotenv.load_dotenv()
PAPER_TABLE = os.getenv("PAPER_TABLE")


def meta_adder_run():
    '''
    Get meta data(doi,abstarct,publish year,journal),citation data, if factor by paper title
    Use scite.ai, crossref,easysholar api
    
    you should 
    1. In data/paper.db,use navicate to create a table and fill titles
    2. Set PAPER_TABLE name in config.py 
    
    The result will be saved in paper.db
    '''
    print("start add meta data to paper")

    # read paper data    
    conn = sqlite3.connect("data/paper.db")
    df = pd.read_sql(f"select * from {PAPER_TABLE}",con=conn)

    for i in tqdm(range(len(df))):
        if "publish_year" in df.columns:
            if pd.notnull(df.loc[i,"publish_year"]):
                continue

        df = add_meta_data(df,i)
        df = add_if_factor(df,i)

        df.to_sql(f"{PAPER_TABLE}",con=conn,if_exists="replace",index=False)
   
    # add citation
    df = add_citations(df)

    # save
    df.to_sql(f"{PAPER_TABLE}",con=conn,if_exists="replace",index=False)
    
    print("meta data save to db")
  
if __name__ == "__main__":
    meta_adder_run()
