import os
import sys

sys.path.append(os.getcwd())

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





def is_paper_link(title, page_title):
    pmt  = '''
            I am using the  paper title to download paper content by google search.
            Please help me to check whether the  search title is mapping the paper.
            Please think in <think></think> xml tag fisrt then answer 
            if you think the search title is mapping the paper, please answer True, otherwise False

            <page_title>
            {page_title}
            </page_title>

            <title>
            {title}
            </title>

            Return 
            ```
            res: True of False
            ```

            '''.format(page_title=page_title,title=title)
    
    if  "claude" in MODEL:
        idea = ask_claude(pmt)
    elif "gpt" in MODEL:
        idea = ask_gpt(pmt)

    try:
        idea = re.search("res: (.*)", idea).group(1)
    except Exception as e:
        print("claude answer error",e)

    # if claude answer False, skip this paper
    if "False" in idea:
        return False
    else:
        return True



def download_content(df, i, driver):
    doi = df.loc[i, 'doi']
    title = df.loc[i, 'title']
    content = ""
    
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
        page_title = search_res["title"]
       # Google have some special results which are pdf url 
        if search_res["url"].endswith(".pdf"):
            
            # cheak pdf page is acutally mapping title
            if not is_paper_link(title, page_title):
                continue
            
            content = read_pdf_by_url(search_res["url"])
            if content:
                print("pdf download success",str(len(content)))
                return content
 
         # arxiv also have pdf url
        if "arxiv" in search_res["url"]:
            # cheak pdf page is acutally mapping title
            if not is_paper_link(title, page_title):
                continue

            content = get_arxiv_content_by_url(search_res["url"],driver)
            if content:
                print("arxiv download success",str(len(content)))
                return content 
                 

    return content
