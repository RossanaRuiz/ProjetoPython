import time
from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

time.sleep(2)
driver.get('https://bra.ifsp.edu.br/servidores')


lista  = driver.find_element(By.XPATH, '//*[@id="content-section"]/div/div[1]/ul')
linhas  = lista.find_elements(By.TAG_NAME, "li")

for l in linhas:
  print(l.text)
