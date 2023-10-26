import sys
import os
sys.path.append(os.getcwd())
from paper.paper_downloader.reader.carsi import CarsiGetter

def get_springer_content_by_url(url,driver):

    getter = CarsiGetter(driver)
    content = getter.get_insitituion_content(url,'//a[text() = "SpringerLink平台"]')

    return content


