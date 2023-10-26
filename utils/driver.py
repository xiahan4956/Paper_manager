import time
from selenium import webdriver
import random

def load_driver():
    
    for _ in range(5):
        try:
            driver = webdriver.Chrome()

            driver.set_window_size(1200,900)
            driver.set_window_position(0,0)
            break
        except Exception as e:
            print("Lunch chrome fail.Retry",e)
            continue
    return driver

def scroll_down_to_bottom(driver):
    try:
        for _ in range(50):
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(0.1)
            current_scroll_position = driver.execute_script("return window.pageYOffset;")
            page_height = driver.execute_script("return document.body.scrollHeight")
            if current_scroll_position/page_height > 0.9:
                break
    except Exception as e:
        print("scroll fail",e)

