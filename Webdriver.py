from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import time

usr = input('Enter username: ')
pwd = input('Enter password: ')
print('\nLaunching browser...')
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)


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
    p_source = driver.page_source
    print(p_source)
#    with open("file.txt", 'w', encoding='utf-8') as f:
#    f.write(driver.page_source)
#    f.close()


def CheckOrdersAmount():
    wait.until(EC.presence_of_element_located((
        By.XPATH, '//*[@id="market_commodity_buyrequests"]/span[1]')))
    elem = driver.find_element_by_xpath(
        '//*[@id="market_commodity_buyrequests"]/span[1]')
    ordersAmount = int(elem.text)
    if ordersAmount < 100:
        print('Not enough people wants this item')
    else:
        print('Orders amount is {}'.format(ordersAmount))


login()
driver.get('https://steamcommunity.com/market/search?appid=570#p180_price_asc')
wait.until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="result_0"]/div[2]')))
# Opening tabs
for i in range(10):
    open_tab = driver.find_element_by_xpath(
        '//*[@id="result_{}"]/div[2]'.format(i))
    OpenNewTab()
time.sleep(20)
# Switching between tabs from last to second
for i in range(1, 11):
    driver.switch_to.window(driver.window_handles[i])
    CheckOrdersAmount()
    time.sleep(1)

SourceScrapping()
input()
driver.close()
