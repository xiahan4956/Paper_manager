import os
import sys

sys.path.append(os.getcwd())

from utils.google_search import get_google_serach_list
from paper.paper_downloader.reader.pdf_reader import *
from paper.paper_downloader.reader.research_gate import *
from paper.paper_downloader.reader.scihub import *
from paper.paper_downloader.reader.arxiv import *
from scihub_cn.scihub import *



def download_content(df, i, driver, data_path = os.path.join(os.getcwd(),"temp")):
    # 定义字段
    doi = df.loc[i, 'doi']
    title = df.loc[i, 'title']
    
    # 清空data_path
    while True:
        try:
            for file in os.listdir(data_path):
                os.remove(os.path.join(data_path,file))
            break
        except Exception as e:
            time.sleep(10)
            print(e)
            pass

    # 先尝试直接用doi下载scihub
    content = ""
    if pd.notnull(doi):
        content = get_scihub_content_by_doi(doi,data_path,driver)
    if content:
        print("scihub download succuess:",str(len(content)))
        return content

    # 不行再尝试用谷歌搜索
    driver.get(f'https://www.google.com/search?q={title}')
    search_list = get_google_serach_list(driver)
    
    for search_res in search_list:
       # 解析本身的pdf
        if search_res["url"].endswith(".pdf"):
            content = read_pdf_by_url(search_res["url"],data_path)
            if content:
                print("pdf通过url下载成功:",str(len(content)))
                return content
 
         # 再看get_arxiv_content_by_url
        if "arxiv" in search_res["url"]:
            content = get_arxiv_content_by_url(search_res["url"],driver,data_path)
            if content:
                print("arxiv下载成功:",str(len(content)))
                return content 
     
    print("content没有能够下载",title)
    return ""