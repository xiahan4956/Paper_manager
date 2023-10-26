import os
import sys

sys.path.append(os.getcwd())

from paper.paper_downloader.reader.ieee import get_ieee_content_by_url
from paper.paper_downloader.reader.springer import get_springer_content_by_url
from utils.claude import ask_claude
from utils.gpt import ask_gpt
from utils.google_search import get_google_serach_list
from paper.paper_downloader.reader.pdf_reader import *
from paper.paper_downloader.reader.research_gate import *
from paper.paper_downloader.reader.scihub import *
from paper.paper_downloader.reader.arxiv import *
from scihub_cn.scihub import *

import dotenv
dotenv.load_dotenv()
MODEL = os.getenv("MODEL")


def download_content(df, i, driver):
    doi = df.loc[i, 'doi']
    title = df.loc[i, 'title']
    
    
    # Try to download from scihub by doi
    if pd.notnull(doi):
        content = get_scihub_content(doi,driver)
    if content:
        print("scihub download succuess:",str(len(content)))
        return content

    # If scihub fails, try to download from google search to find some avilaible soucre
    driver.get(f'https://www.google.com/search?q={title}')
    search_list = get_google_serach_list(driver)
    
    for search_res in search_list:
       # Google have some special results which are pdf url 
        if search_res["url"].endswith(".pdf"):
                        
            content = read_pdf_by_url(search_res["url"])
            if title.lower() in content[:3000]: # To ensure content is really mapping the paper 
                print("pdf download success",str(len(content)))
                return content
 
         # arxiv also have pdf url
        if "arxiv" in search_res["url"]:

            content = get_arxiv_content_by_url(search_res["url"],driver)
            if title.lower() in content[:3000]: # To ensure content is really mapping the paper 
                print("arxiv download success",str(len(content)))
                return content

        # Use beihang carsi to download content
        # IEEE
        if "ieee" in search_res["url"]:
            content = get_ieee_content_by_url(search_res["url"],driver)
            if title.lower() in content[:3000]: # To ensure content is really mapping the paper 
                print("ieee下载成功:",str(len(content)))
                return content

        # springer
        if "springer" in search_res["url"]:   
            content = get_springer_content_by_url(search_res["url"],driver)
            if title.lower() in content[:3000]: # To ensure content is really mapping the paper 
                print("springer下载成功:",str(len(content)))
                return content
  

    return "" #if there are no souce
