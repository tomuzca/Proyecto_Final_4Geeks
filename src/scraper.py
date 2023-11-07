# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from time import sleep
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait 
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup
# import re
# import pandas as pd
# import numpy as np

# # Set Chrome options and the user-agent
# opts = Options()
# opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

# # Initialize the ChromeDriver
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)


# origin = "ZRH"
# destination = "MXP"
# startdate = "2023-11-07"
# enddate = "2023-11-14"
# url = f"https://www.kayak.cl/flights/{origin}-{destination}/{startdate}/{enddate}?sort=bestflight_a"


# # Open the Kayak website
# driver.get(url)
# sleep(13)


# boton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//div[@role="button" and @class="ULvh-button show-more-button"]'))).click()
# boton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//div[@role="button" and @class="ULvh-button show-more-button"]'))).click()
# boton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//div[@role="button" and @class="ULvh-button show-more-button"]'))).click()
# boton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//div[@role="button" and @class="ULvh-button show-more-button"]'))).click()



# sleep(20)


# soup=BeautifulSoup(driver.page_source, 'lxml')

# #get the arrival and departure times
# deptimes = soup.find_all('div', attrs={'class': "vmXl vmXl-mod-variant-large"})
# arrtimes = soup.find_all('div', attrs={'class': "vmXl vmXl-mod-variant-large"})


# deptime = []
# for div in deptimes:
#     deptime.append(div.getText()[:-1])    
    
# arrtime = []
# for div in arrtimes:
#     arrtime.append(div.getText()[:-1])   

    
# deptime = np.asarray(deptime)
# deptime = deptime.reshape(int(len(deptime)/2), 2)

# arrtime = np.asarray(arrtime)
# arrtime = arrtime.reshape(int(len(arrtime)/2), 2)      



