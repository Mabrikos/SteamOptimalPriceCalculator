from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import sys
import os

usr = input('Enter username: ')
pwd = input('Enter password: ')
print('\nLaunching browser...')
# connect Steam Trader Helper extension
directory = os.getcwd()
path = str(os.path.join(directory, 'Steam-Inventory-Helper_v1.15.0.crx'))
chrome_options = Options()
chrome_options.add_extension(path)
driver = webdriver.Chrome(chrome_options=chrome_options)
# -----------------------------------------------------------
wait = WebDriverWait(driver, 10)
waiter = WebDriverWait(driver, 60 * 5)
item_wait = WebDriverWait(driver, 60)
sys.setrecursionlimit(10000)
Percentage = '-5'


def login():
    driver.get("http://store.steampowered.com")
    driver.find_element_by_class_name("global_action_link").click()
    driver.find_element_by_id("input_username").send_keys(usr)
    elem = driver.find_element_by_id("input_password")
    elem.send_keys(pwd)
    elem.send_keys(Keys.RETURN)
    time.sleep(10)
    waiter.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="account_pulldown"]')))
    print('Successfully logged in')


login()
driver.get('https://steamcommunity.com/')
driver.get('https://steamcommunity.com/market/')
waiter.until(EC.invisibility_of_element_located((
    By.XPATH, '//*[@id="_priceQueueCont"]')))
driver.find_element_by_xpath('//*[@id="my_listing_pagesize_100"]').click()
time.sleep(10)
price_checker_box = driver.find_element_by_xpath('//*[@id="_priceQueueCont"]')
while price_checker_box.is_displayed():
    print('Box appears')
    waiter.until(EC.invisibility_of_element_located((
        By.XPATH, '//*[@id="_priceQueueCont"]')))
    print('Box invisible')
    driver.find_element_by_xpath(
        '//*[@id="tabContentsMyActiveMarketListingsTable"]/div[1]/div/div[3]/a[1]/span[2]').click()
    driver.find_element_by_xpath(
        '//*[@id="tabContentsMyActiveMarketListingsTable"]/div[1]/div/div[3]/a[2]').click()

else:
    driver.find_element_by_xpath(
        '//*[@id="tabContentsMyActiveMarketListingsTable"]/div[1]/div/div[3]/a[1]/span[2]').click()
    driver.find_element_by_xpath(
        '//*[@id="tabContentsMyActiveMarketListingsTable"]/div[1]/div/div[3]/a[2]').click()
time.sleep(5)
# open inventory
driver.find_element_by_xpath(
    '//*[@id="global_header"]/div/div[2]/a[3]').click()
driver.find_element_by_xpath(
    '//*[@id="friendactivity_right_column"]/div/div[3]/div[7]/a/span').click()
# opening dota 2 inventory
driver.find_element_by_xpath('//*[@id="inventory_link_570"]').click()
driver.set_window_size(891, 1006)
# waiting for items to load
driver.find_element_by_xpath(
    '//*[@id="inventory_76561198339646027_570_2"]/div[1]/div[1]').click()
time.sleep(1)
waiter.until(EC.invisibility_of_element_located((
    By.XPATH, '//*[@id="iteminfo1_item_market_actions"]/div/div[2]/img')))
driver.find_element_by_xpath('/html/body/div[8]/div/div[2]').click()

waiter.until(EC.visibility_of_element_located((
    By.XPATH, '//*[@id="Lnk_Sellall"]')))
driver.find_element_by_xpath('//*[@id="Lnk_Sellall"]').click()
driver.find_element_by_xpath('//*[@id="Lnk_ShowSellMulti"]').click()
wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="autosell"]')))
driver.find_element_by_xpath('//*[@id="autosell"]').click()
driver.find_element_by_xpath(
    '//*[@id="market_sell_dialog_accept_ssa"]').click()
driver.find_element_by_xpath('//*[@id="ck_autoadjust"]').click()
driver.find_element_by_xpath('//*[@id="cb_adtype"]').click()
driver.find_element_by_xpath('//*[@id="cb_adtype"]/option[2]').click()
driver.find_element_by_xpath('//*[@id="Txt_adjust"]').click()
ActionChains(driver) \
    .send_keys(Keys.ARROW_RIGHT) \
    .send_keys(Keys.BACKSPACE) \
    .perform() \

driver.find_element_by_xpath('//*[@id="Txt_adjust"]').send_keys(Percentage)
driver.find_element_by_xpath(
    '//*[@id="market_sell_dialog_accept"]/span').click()
wait.until(EC.visibility_of_element_located((
    By.XPATH, '//*[@id="market_sell_dialog_ok"]/span')))
driver.find_element_by_xpath('//*[@id="market_sell_dialog_ok"]/span').click()
waiter.until(EC.invisibility_of_element_located(
    (By.XPATH, '//*[@id="market_sell_dialog"]/div[2]/div')))
print('Finished')
input()
