import pandas as pd
import numpy as np
import os
import sys
import sqlite3
from tqdm import tqdm
sys.path.append(os.getcwd())
from utils.claude import ask_claude
from utils.gpt import ask_gpt
from ast import literal_eval
import re

import dotenv
dotenv.load_dotenv()
MODEL = os.getenv("MODEL")
PAPER_TABLE = os.getenv("PAPER_TABLE")


# extract ai answer to keyword
def _extract_keyword(x):
    """Extract content between [] and return None if not found."""
    match = re.search(r"\[(.*?)\]", str(x))
    return match.group(0) if match else None

def _safe_literal_eval(x):
    """Safely apply literal_eval. If it fails, return None."""
    try:
        return literal_eval(x)
    except:
        return None 
    
def read_paper_table():
    """Read paper table from database."""
    conn  = sqlite3.connect('data/paper.db')
    df = pd.read_sql(f'select * from {PAPER_TABLE}', conn)
    
    return df


def extract_keyword(df):
    '''
    Extract the keyword from title,abstarct
    Use AI to extract keyword
    '''
     
    df = df[["title","publish_year","abstract"]]
    df['keywords'] = ""
    
    for i in tqdm(range(len(df))):
        info = df.iloc[i].to_json(orient="index")
        
        question = '''
        Please extract more important keywords from the paper <info>
        The keywords should include nouns, verbs, and phrases.
        Try to provide professional phrases.
        Try to provide more keywords.
        Do not make up words.

        You should return the keywords in a list.

        Return example:
        ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5",....]
        '''
        pmt = '''
        <info>
        {info}
        </info>
        
        {question}
        '''.format(info=info,question=question)
        
        if "claude" in MODEL:
            answer = ask_claude(pmt)
        if "gpt" in MODEL:
            answer = ask_gpt(pmt)            
        answer = _extract_keyword(answer)     

        keywords = _safe_literal_eval(answer)
    
        df.at[i,"keywords"] = keywords # the keywords is a list
        

    return df


def build_keyword_time_table(paper_keyword_df):
    '''
    In order to understand the development of keyword
    Get the variouse year of keyword.
    '''
    
    # groupby后,计算 min_year first_quartile_year median_year third_quartile_year max_year
    paper_keyword_df['publish_year'] = paper_keyword_df['publish_year'].astype(int)
    keyword_time_df = paper_keyword_df.groupby("keyword").agg({"publish_year": [np.min, lambda x: np.quantile(x, 0.25), np.median, lambda x: np.quantile(x, 0.75),np.max]})
    # 重命名列名 min_year first_quartile_year median_year third_quartile_year max_year
    keyword_time_df.columns = ["min_year", "first_quartile_year", "median_year", "third_quartile_year", "max_year"]

    return keyword_time_df

def build_paper_keyword_table(df):
    '''
    Make keyword map a single pulibsh year.
    It is for the keyword years analysis
    '''
    
    paper_keyword_df = df[['title', 'keywords',"publish_year"]]
    paper_keyword_df = paper_keyword_df.set_index('title').explode('keywords')
    paper_keyword_df.rename(columns={"keywords": "keyword"}, inplace=True)

    return paper_keyword_df

def merge_importance_year(keyword_degree_df, keyword_time_df):
    '''
    In order to save in the database,
    merge the importance and year of keywords 
    '''
    keyword_degree_df = pd.merge(keyword_degree_df, keyword_time_df, left_index=True, right_index=True, how='left')
    keyword_degree_df.reset_index(inplace=True)
    keyword_degree_df.rename(columns={"index": "keyword"}, inplace=True)
    
    return keyword_degree_df