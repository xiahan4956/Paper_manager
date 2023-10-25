import os
import sys
import sqlite3
import pandas as pd
from tqdm import tqdm

sys.path.append(os.getcwd())
from utils.driver import load_driver
from utils.claude import *
import dotenv
dotenv.load_dotenv(dotenv.find_dotenv())

PAPER_TABLE = os.getenv("PAPER_TABLE")  

# 读取sqllite数据库
conn = sqlite3.connect("data/paper.db")
df = pd.read_sql_query("SELECT * FROM {} LIMIT -1  offset 130".format(PAPER_TABLE), conn)

# 把字段导入到obsidian
def clean_limited_filename(title, max_length=200):
    """清洗标题，去掉不能作为文件名的字符,并限制文件名的长度"""
    # 清洗非法字符
    limited_filename = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]
    for c in limited_filename:
        title = title.replace(c, "")
    
    # 如果标题长度超过最大长度，我们将其截断到最后一个空格
    if len(title) > max_length:
        title = title[:max_length].rsplit(' ', 1)[0]
    
    return title



# %% 写入到obsidian
# 先清洗标题
for i in tqdm(range(len(df))):
    clean_title = df.loc[i]["title"]
    clean_title = clean_limited_filename(clean_title)
    df.loc[i,"clean_title"] = clean_title

# 清洗年份
df["clean_year"] = df.publish_year.fillna(0).astype("int",errors="ignore")


for i in tqdm(range(len(df))):

    doi = df.loc[i]["doi"]
    journal = df.loc[i]["journal"]
    abstract = str(df.loc[i]["abstract"]).replace("#","")
    clean_year = df.loc[i]["clean_year"]
    publisher = df.loc[i]["publisher"]
    sci = df.loc[i]["sci"]
    sciif = df.loc[i]["sciif"]
    citations = df.loc[i]["citations"]
    content = str(df.loc[i]["content"]).replace("#","")
    content_words = df.loc[i]["content_words"]
    idea = df.loc[i]["idea"]
    title_cn = df.loc[i]["title_cn"]
    clean_title = df.loc[i]["clean_title"]
    
    source = df.loc[i]["source"]

    
    if content:
        with open(rf"C:\Users\xiahan\Documents\BaiduSyncdisk\4_xiahan.life\爬虫论文\temp\{clean_year} {clean_title}.md", "w+", encoding="utf-8") as f:
            # yaml
            f.write(f"---\n")
            f.write(f"aliases: {title_cn}\n")
            f.write(f"source: {source}\n")
            f.write(f"sci: {sci}\n")
            f.write(f"sciif: {sciif}\n")
            f.write(f"citations: {citations}\n")
            f.write(f"doi: {doi}\n")
            f.write(f"journal: {journal}\n")
            f.write(f"year: {clean_year}\n")
            f.write(f"publisher: {publisher}\n")
            f.write(f"---\n")

            # content
            f.write(f"# meta\n")
            f.write(f"abstract: {abstract}\n")

            f.write(f"{idea}\n")

            f.write(f"# content\n")
            f.write(f"## content_words\n{content_words}\n")
            f.write(f"## full_content\n{content}\n")

