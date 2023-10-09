import os
import sys
from tqdm import tqdm

sys.path.append(os.getcwd())
import pandas as pd
from utils.driver import load_driver
from utils.claude import *
from paper.paper_downloader.reader.downloader import download_content
import sqlite3

import dotenv
dotenv.load_dotenv()

MODEL = os.getenv("MODEL")
PAPER_TABLE = os.getenv("PAPER_TABLE")


def skip(df, i):
    # skip if there is paper text
    if "content" in df.columns:
        if pd.notnull(df.loc[i, 'content']):
            return True
    return False

def save_content_to_database(conn, df, i, content):
    # use paper text words to identify if the paper is downloaded normally
    content_words = len(content)
    
    # save to database
    while True:
        try:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {PAPER_TABLE} SET content = ? , content_words = ? WHERE title = ?", (content,content_words ,df.loc[i].get('title')))
            conn.commit()
            break
        except Exception as e:
            print("database may deadlock",e)
            time.sleep(10)


def run_paper_downloader():
    '''
    Download paper text.
    You should have titles or dois in paper.db
    
    The paper text will be saved in paper.db
    The text of paper help AI to extract paper information
    '''
    
    print("now download paper text")
    # read paper data from database
    conn = sqlite3.connect('data/paper.db')
    driver = load_driver()
    df = pd.read_sql_query(f'select * from {PAPER_TABLE}', conn)
    
    # if there is paper text, skip
    for i in tqdm(range(0,len(df))):    
        if skip(df, i):
            continue

        # check database whether has the content column
        cheak_and_add_content_column(conn, df)

        # download paper text.if success, save to database
        content = download_content(df, i, driver)
        if content:
            save_content_to_database(conn, df, i, content)
            
            
    print("paper text download finish")

def cheak_and_add_content_column(conn, df):
    df = pd.read_sql_query(f'select * from {PAPER_TABLE}', conn)
    if ("content" not in df.columns) or ("content_words" not in df.columns) :
        cursor = conn.cursor()
        cursor.execute(f"ALTER TABLE {PAPER_TABLE} ADD COLUMN content TEXT")
        cursor.execute(f"ALTER TABLE {PAPER_TABLE} ADD COLUMN content_words INT")
        conn.commit()
        print("add content column to database")

if __name__ == "__main__":
    run_paper_downloader()