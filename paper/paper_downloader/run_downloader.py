import os
import sys
import time
import sqlite3
import pandas as pd
from tqdm import tqdm
from multiprocessing import Pool

sys.path.append(os.getcwd())
from utils.driver import load_driver
from utils.claude import *
from paper.paper_downloader.reader.downloader import download_content
import dotenv
dotenv.load_dotenv()

MODEL = os.getenv("MODEL")
PAPER_TABLE = os.getenv("PAPER_TABLE")
PROCESS_NUM = int(os.getenv("PROCESS_NUM"))


def skip(df, i):
    if "content" in df.columns:
        if pd.notnull(df.loc[i, 'content']):
            return True
    return False


def save_content_to_database(conn, df, i, content):
    content_words = len(content)

    while True:
        try:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {PAPER_TABLE} SET content = ? , content_words = ? WHERE title = ?",
                           (content, content_words, df.loc[i].get('title')))
            conn.commit()
            break
        except Exception as e:
            print("database may deadlock", e)
            time.sleep(10)


def process_paper(i):
    conn = sqlite3.connect('data/paper.db')

    df = pd.read_sql_query(f'select * from {PAPER_TABLE}', conn)
    if skip(df, i):
        return
   
    driver = load_driver()
   
    content = download_content(df, i, driver)
    if content:
        save_content_to_database(conn, df, i, content)
    conn.close()
    driver.quit()


def cheak_and_add_content_colums_in_table(conn, df):
    df = pd.read_sql_query(f'select * from {PAPER_TABLE}', conn)
    if ("content" not in df.columns) or ("content_words" not in df.columns):
        cursor = conn.cursor()
        cursor.execute(f"ALTER TABLE {PAPER_TABLE} ADD COLUMN content TEXT")
        cursor.execute(f"ALTER TABLE {PAPER_TABLE} ADD COLUMN content_words INT")
        conn.commit()
        print("add content column to database")


def run_paper_downloader():
    print("now download paper text")

    conn = sqlite3.connect('data/paper.db')
    df = pd.read_sql_query(f'select * from {PAPER_TABLE}', conn)
    cheak_and_add_content_colums_in_table(conn, df)
    
    with Pool(PROCESS_NUM) as pool:
        indices = range(len(df))
        list(tqdm(pool.imap(process_paper, indices), total=len(df)))

    print("paper text download finish")


if __name__ == "__main__":
    run_paper_downloader()
