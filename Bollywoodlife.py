from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
import json
chromePath = ('D:\selenium\chromedriver_win32\chromedriver.exe')
driver = webdriver.Chrome(chromePath)
driver.maximize_window()
data_list = []
for j in range(1,4):
    url = 'https://www.bollywoodlife.com/hollywood/page/'+str(j)
    page = driver.get(url)
    time.sleep(6)
    div = driver.find_elements(By.CSS_SELECTOR, '.story_content')
    for i in div:
        data = {}
        data["headline"] = i.find_element(By.CSS_SELECTOR, '.story_heading_alink').text
        data["topic"] = i.find_element(By.CSS_SELECTOR,".catName").text
        source=i.find_element(By.CSS_SELECTOR, '.story_heading_alink')
        data["source"] = source.get_attribute("href")
        times = i.find_element(By.CSS_SELECTOR, '.story_date')
        data["date"] = times.text[:-12]
        new = requests.get(data["source"])
        soup = BeautifulSoup(new.content, "html.parser")
        try:
            data["thumbnail_url"] = soup.select(".art_main_img_alink img")[0].get('data-src')
        except:
            data["thumbnail_url"]= None
        desc=""
        a=soup.select("p")
        for q in a:
            desc += q.text
        data["description"] = desc
        data_list.append(data)
print(data_list)
print(len(data_list))

json_obj = json.dumps(data_list,indent=4,ensure_ascii=False)
json.loads(json_obj)
with open('Bolly.json',"w",encoding="utf-8") as f:
    f.write(json_obj)
    
driver.quit()