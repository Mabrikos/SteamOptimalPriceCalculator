from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import re
import sys
# import os


def ReductionInit():
    global per
    init = input("Reduct price by, %: ")
    try:
        per = int(init) + 100
    except ValueError:
        print('\n>>> Number is required\n')
        ReductionInit()


ReductionInit()

usr = input('Enter username: ')
pwd = input('Enter password: ')
print('\nLaunching browser...')
# connect Steam Trader Helper extension
chrome_options = Options()
chrome_options.add_extension(
    'D:\\Documents\\Git\\SteamOptimalPriceCalculator\\Steam-Inventory-Helper_v1.15.0.crx')
driver = webdriver.Chrome(chrome_options=chrome_options)
# -----------------------------------------------------------
wait = WebDriverWait(driver, 10)
sys.setrecursionlimit(10000)
itemsAmount = '10'  # amount of items to buy


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


def PriceConverter():
    global optimalPrice
    cpp_buy = round((cpp / per * 100), 2)
    # Range of allowed prices (from 0.25 to 1.00)
    if cpp_buy < 0.25:  # or cpp_buy > 1.00:
        cpp_buy = 0
    if cpp_buy > 0:
        print(
            ">>> Optimal price is [%s]"
            % cpp_buy, '\n')
        optimalPrice = str(cpp_buy)
    else:
        print(">>> Price is unacceptable\n")


def RegexSearch():
    global ps, ps_length
    priceRegex = re.compile(r'\d?\d\,\d?\d?')  # Search by type 00,00
    prices = priceRegex.findall(listings)
    prices = [w.replace(',', '.') for w in prices]
    prices = list(map(float, prices))
    ps = sorted(list(set(prices)))
    print(ps)
    ps_length = len(ps)


def PriceCalculator():
    global cpp
    RegexSearch()
    for i in range(ps_length):
        try:
            global cp
            cp = ((100 - ((ps[i] * 100) / ps[i + 1])))
            if cp >= 20:
                cpp = ps[i + 1]
                PriceConverter()
                break
        except IndexError:
            cpp = ps[0]
            PriceConverter()
            break
        cp = ((100 - ((ps[i] * 100) / ps[i + 1])))
        if cp < 20:
            test1 = ps[i - 1]  # last element
            test2 = ps[i]  # first element
            test_result = ((100 - ((test2 * 100) / test1)))
            if test_result > 15 < 48:
                cpp = ps[i]
                PriceConverter()
            else:
                if test_result < 15 > 5:
                    cpp = ps[i]
                    PriceConverter()
                else:
                    # if crap above doesn't do his job => (last / first)
                    cpp = ps[i - 1]
                    PriceConverter()
            break


login()
driver.get('https://steamcommunity.com/market/search?appid=570#p200_price_asc')
wait.until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="result_0"]/div[2]')))
# Opening tabs

def BuyItems():
    global open_tab
    global listings
    for i in range(10):
        open_tab = driver.find_element_by_xpath(
            '//*[@id="result_{}"]/div[2]'.format(i))
        OpenNewTab()
    # time.sleep(20)
    # Switching between tabs from last to second
    for i in range(1, 11):
        driver.switch_to.window(driver.window_handles[i])
    # Checking orders amount, "try" made because there can be no orders
        try:
            wait.until(EC.presence_of_element_located((
                By.XPATH, '//*[@id="market_commodity_buyrequests"]/span[1]')))
            elem = driver.find_element_by_xpath(
                '//*[@id="market_commodity_buyrequests"]/span[1]')
            ordersAmount = int(elem.text)
        except:
            ordersAmount = 0

        if ordersAmount < 100:
            print('Not enough people wants this item')
        else:
            # Calculating optimal price
            print('Orders amount is {}'.format(ordersAmount))
            elem = driver.find_element_by_id('searchResultsRows')
            listings = elem.text
            PriceCalculator()
            time.sleep(0)
            # small interface
            driver.find_element_by_xpath(
                '//*[@id="market_buyorder_info"]/div[1]/div[1]/a').click()
            driver.find_element_by_xpath(
                '//*[@id="market_buy_commodity_input_price"]').clear()
            driver.find_element_by_xpath(
                '//*[@id="market_buy_commodity_input_price"]').send_keys(optimalPrice)
            driver.find_element_by_xpath(
                '//*[@id="market_buy_commodity_input_quantity"]').click()
            driver.find_element_by_xpath(
                '//*[@id="market_buy_commodity_input_quantity"]').clear()
            driver.find_element_by_xpath(
                '//*[@id="market_buy_commodity_input_quantity"]').send_keys(itemsAmount)
            driver.find_element_by_xpath(
                '//*[@id="market_buyorder_dialog_accept_ssa"]').click()
            driver.find_element_by_xpath(
                '//*[@id="market_buyorder_dialog_purchase"]').click()


while True:
    BuyItems()
    # closing tabs
    for i in range(1, 11):
        driver.switch_to_window(driver.window_handles[1])
        driver.close()
    # pressing "next(>)" button
    driver.switch_to_window(driver.window_handles[0])
    driver.find_element_by_xpath('//*[@id="searchResults_btn_next"]').click()
    time.sleep(1.5)

input()
driver.close()
