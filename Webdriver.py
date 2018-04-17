from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import time
import re

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


def PriceConverter():
    cpp_buy = round((cpp / per * 100), 2)
    # Range of allowed prices (from 0.25 to 1.00)
    if cpp_buy < 0.25 or cpp_buy > 1.00:
        cpp_buy = 0
    if cpp_buy > 0:
        print(
            ">>> Optimal price [%s] has copied to your clipboard"
            % cpp_buy, '\n')
        pyperclip.copy(str(cpp_buy))
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
    while True:
        RegexSearch()
        if ps_length < 2:  # if list contains only 1 element
            try:
                cpp = ps[0]
                PriceConverter()
            except IndexError:
                print('Something went wrong...')

        for i in range(ps_length):
            cp = ((100 - ((ps[i] * 100) / ps[i + 1])))
            if cp >= 20:
                cpp = ps[i + 1]
                PriceConverter()

            if cp < 20:
                test1 = ps[i - 1]  # last element
                test2 = ps[i]  # first element
                test_result = ((100 - ((test2 * 100) / test1)))
                if test_result > 15 < 48:
                    cpp = ps[i]
                    PriceConverter()
                if test_result < 15 > 5:
                    cpp = ps[i]
                    PriceConverter()
                else:
                    # if crap above doesn't do his job => (last / first)
                    cpp = ps[i - 1]
                    PriceConverter()


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
    elem = driver.find_element_by_id('searchResultsRows')
    listings = elem.text
    RegexSearch()
    PriceCalculator()
    # close tab function
    time.sleep(1)

SourceScrapping()
input()
driver.close()
