from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pickle

usr = input('Enter username: ')
pwd = input('Enter password: ')
print('\nLaunching browser...')
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
    print('Successfully logged in')


def OpenNewTab():
    ActionChains(driver) \
        .key_down(Keys.CONTROL) \
        .click(open_tab) \
        .key_up(Keys.CONTROL) \
        .perform()


def SourceScrapping():
    with open("file.txt", 'w', encoding='utf-8') as f:
    f.write(driver.page_source)
    f.close()


login()
driver.get('https://steamcommunity.com/market/search?appid=570#p180_price_asc')
lot_wait = WebDriverWait(driver, 10)
lot_wait.until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="result_0"]/div[2]')))
for i in range(10):
    open_tab = driver.find_element_by_xpath(
        '//*[@id="result_{}"]/div[2]'.format(i))
    OpenNewTab()

SourceScrapping()
input()
driver.close()
