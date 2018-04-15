from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

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
input()

driver.close()
