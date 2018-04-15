from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pickle

usr = input('Enter username: ')
pwd = input('Enter password: ')
driver = webdriver.Chrome()


def login():
    driver.get("http://store.steampowered.com")
    driver.find_element_by_class_name("global_action_link").click()
    driver.find_element_by_id("input_username").send_keys(usr)
    elem = driver.find_element_by_id("input_password")
    elem.send_keys(pwd)
    elem.send_keys(Keys.RETURN)
    time.sleep(15)
    driver.find_element_by_id('twofactorcode_entry').send_keys(Keys.RETURN)
    time.sleep(20)


login()
driver.get('https://steamcommunity.com/market/search?appid=570#p180_price_asc')
# for i in range 10:
# driver.find_element_by_xpath('//*[@id="result_{}"]/div[2]'.format(i)).send_keys(Keys.CONTROL + 't')
lot_wait = WebDriverWait(driver, 10)
lot_wait.until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="result_0"]/div[2]')))
driver.find_element_by_xpath(
    '//*[@id="result_0"]/div[2]').click()  # send_keys(Keys.CONTROL + 't')
# Sourcecode scraping
with open("file.txt", 'w', encoding='utf-8') as f:
    f.write(driver.page_source)
f.close()
input()
driver.close()
