import sys
import os

sys.path.append(os.getcwd())
from paper.paper_downloader.reader.pdf_reader import dose_have_new_pdf, read_pdf, read_pdf_by_url

from selenium.webdriver.common.by import By

def get_arxiv_content_by_url(url, driver, data_path):

    driver.get(url)
    try:
        # find  //a[text() ="PDF"]
        pdf_url = driver.find_element(By.XPATH,"//a[text() ='PDF']").get_attribute("href")
    except:
        pdf_url = driver.current_url
    
    content = read_pdf_by_url(pdf_url,data_path)

    return content