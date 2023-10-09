import sys
import os
sys.path.append(os.getcwd())


from selenium.webdriver.common.by import By
from paper.paper_downloader.reader.pdf_reader import dose_have_new_pdf, read_pdf

def get_research_gate_content_by_url(url, driver, data_path):

    driver.get(url)
    initial_files = set(os.listdir(data_path)) 
    
    # span.gtm-download-fulltext-btn-header
    try:
        driver.find_element(By.CSS_SELECTOR, 'span.gtm-download-fulltext-btn-header').click()
    except:
        pass

    content = ""
    new_files = dose_have_new_pdf(data_path,initial_files)
    if new_files:
        content = read_pdf(new_files, data_path)

    return content