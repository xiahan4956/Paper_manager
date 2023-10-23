import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import sys
sys.path.append(os.getcwd())

from utils.driver import scroll_down_to_bottom
from paper.paper_downloader.reader.carsi import CarsiGetter

def get_ieee_content_by_doi(df,i,driver):
    doi = df.loc[i,'doi']

    # GET beihang auth
    driver.get('https://www.buaa.edu.cn/index/CARSI.htm')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[text() = "IEEE (电气电子工程师学会)"]'))).click()
    
    # 看看是否触发carsi
    time.sleep(1)
    carsi = CarsiGetter(driver)
    carsi.get_beihang_auth()

    # https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=doi
    driver.get('https://ieeexplore.ieee.org/search/searchresult.jsp?queryText='+doi)

    # click paper a.fw-bold
    href = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.fw-bold"))).get_attribute('href')
    driver.get(href)

    # when #sec1 div.article-hdr.header show .then get text
    while True:
        e = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#BodyWrapper"))).text
        if len(e) > 5000:
            scroll_down_to_bottom(driver)
            break
            
    content = driver.find_element(By.CSS_SELECTOR,"body").text
    print("content"+str(len(content)))

    df.loc[i,'content'] = content.replace('"',"")
    
    return df



def get_ieee_content_by_url(url,driver):
    ieee_getter = CarsiGetter(driver)
    content = ieee_getter.get_insitituion_content(url,'//a[text() = "IEEE (电气电子工程师学会)"]')

    return content
