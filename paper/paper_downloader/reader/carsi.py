import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.driver import scroll_down_to_bottom
import os
import dotenv
dotenv.load_dotenv()
BUAA_ACCOUNT = os.getenv("BUAA_ACCOUNT")
BUAA_PASSWORD = os.getenv("BUAA_PASSWORD")






class CarsiGetter:
    def __init__(self,driver):
        self.driver = driver


    def get_beihang_auth(self):
        if "sso.buaa.edu.cn/login" in self.driver.current_url:

            # switch to  iframe id="loginIframe"
            # wait loginIframe show
            while True:
                try:
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "loginIframe")))
                    break
                except Exception as e:
                    self.driver.refresh()
                    print(e)
            self.driver.switch_to.frame("loginIframe")

            #input#unPassword

            self.driver.find_element(By.CSS_SELECTOR, "input#unPassword").clear()
            ele = self.driver.find_element(By.CSS_SELECTOR, "input#unPassword")
            self.driver.execute_script("arguments[0].value = '';", ele)
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, "input#unPassword").send_keys(BUAA_ACCOUNT)

            #input#pwPassword
            self.driver.find_element(By.CSS_SELECTOR, "input#pwPassword").clear()

            self.driver.find_element(By.CSS_SELECTOR, "input#pwPassword").send_keys(BUAA_PASSWORD)

            try:
                WebDriverWait(self.driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a#dialog-btn2']"))).click()
            except:
                pass


            # click input[onclick='loginPassword()']
            self.driver.find_element(By.CSS_SELECTOR, "input[onclick='loginPassword()']").click()

            # switch to default
            self.driver.switch_to.default_content()
            time.sleep(10)

            # ignore not safe input[value='IGNORE ONCE']
            # time.sleep(7)
            # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[value='IGNORE ONCE']"))).click()
            


    def get_insitituion_content(self,url,insitution_xpath):
        # GET beihang auth
        self.driver.get('https://www.buaa.edu.cn/index/CARSI.htm')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, insitution_xpath))).click()
        
        # 看看是否触发carsi
        print("")
        time.sleep(1)
        self.get_beihang_auth()

        # 进入页面,滚到底部
        self.driver.get(url)
        time.sleep(5)
        scroll_down_to_bottom(self.driver)
        content = self.driver.find_element(By.CSS_SELECTOR,"body").text
        print("content"+str(len(content)))
        
        return content