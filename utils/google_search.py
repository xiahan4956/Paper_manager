from selenium.webdriver.common.by import By

def get_google_serach_list(driver):
    '''in google scholar page, get the first paper url'''
    eles = driver.find_elements(By.XPATH,"//div[@lang]")
    
    res_d_list = []
    for i in range(len(eles)):
        try:
            eles = driver.find_elements(By.XPATH,"//div[@lang]")
            ele = eles[i]
            try:
                url = ele.find_element(By.XPATH, ".//a").get_attribute("href")
            except:
                url = ""
            
            try:
                title = ele.find_element(By.XPATH, ".//h3").text
            except:
                title = ""

            try:
                abstract = ele.find_element(By.XPATH, ".//div[@data-sncf]").text
            except:
                abstract = ""
            
            d = {
                "url":url,
                "title":title,
                "abstract":abstract
            }
            res_d_list.append(d)

        except Exception as e:
            print(f"get google one url error: {e}")
            continue

    return res_d_list