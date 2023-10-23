import random
import re
import pandas as pd 
import sys
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from paper.paper_downloader.reader.pdf_reader import dose_have_new_pdf, read_pdf, read_pdf_by_url
sys.path.append(os.getcwd())

def get_scihub_content(doi,driver):
    content = ""

    # Access scihub website to download paper
    try:
        mirror_url = random.choice(["sci-hub.se","sci-hub.st","sci-hub.ru"])
        driver.get(f"https://{mirror_url}/{doi}")
        time.sleep(5)
        
        if "http://library.lol/" in driver.current_url:
            return None

        # if the pdf is directly shown in the browser,dowload it
        try:
            href = driver.find_element(By.CSS_SELECTOR,"a[href='#']").get_attribute("href")
            # Regular expression, parse herf=(.pdf)
            pdf_url = re.search(r'href=(.*?pdf)', href).group(1)
            content = read_pdf_by_url(pdf_url)
            print("Obtained content from SciHub using Selenium.")
            return content
            
        except:
            pass
        
        # anthor type of showing
        try:
            href = driver.find_element(By.XPATH,"//button[text() =  '↓ save']").get_attribute("href")
            pdf_url = re.search(r'href=(.*?pdf)', href).group(1)
            content = read_pdf_by_url(pdf_url)
            print("Obtained content from SciHub using Selenium.")        
            return content
        except:
            pass
        
        # anthor type of showing
        try:
            pdf_url = driver.find_element(By.XPATH,"//a[text() =  'GET']").get_attribute("href")
            content = read_pdf_by_url(pdf_url)
            print("Obtained content from SciHub using Selenium.")
            return content
        except Exception as e:
            print(f"Failed to fetch content from SciHub using Selenium. Error: {type(e).__name__}")
            return content

    except Exception as e:
        print("Failed to download from SciHub:", e)

    return content
