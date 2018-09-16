#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import time
import re
import sys

moneySpent, itemsBought = 0, 0


def ReductionInit():
    global per
    init = input("Reduct price by, %: ")
    try:
        if int(init) > 100 or int(init) < 1:
            print('\n>>> Must be in range from 1 to 100\n')
            ReductionInit()
        else:
            per = int(init) + 100
    except ValueError:
        print('\n>>> Number is required\n')
        ReductionInit()


def login():
    driver.get("http://store.steampowered.com")
    driver.find_element_by_class_name("global_action_link").click()
    driver.find_element_by_id("input_username").send_keys(usr)
    elem = driver.find_element_by_id("input_password")
    elem.send_keys(pwd)
    elem.send_keys(Keys.RETURN)
    time.sleep(10)
    loginWaiter = WebDriverWait(driver, 60 * 5)
    loginWaiter.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="account_pulldown"]')))
    print('Successfully logged in')


def OpenNewTab():
    ActionChains(driver) \
        .key_down(Keys.CONTROL) \
        .click(open_tab) \
        .key_up(Keys.CONTROL) \
        .perform()


def RegexSearch():
    global priceList, priceListLength
    # Search by type 00000,00
    priceRegex = re.compile(r'\d?\d?\d?\d?\d?\,\d?\d?')
    prices = priceRegex.findall(listings)
    prices = [w.replace(',', '.') for w in prices]
    prices = list(map(float, prices))
    priceList = sorted(list(set(prices)))
    # print(priceList)
    priceListLength = len(priceList)


def PriceConverter():
    global itemsBought
    global moneySpent
    global optimalPrice
    finalCalculatedPrice_buy = round((finalCalculatedPrice / per * 100), 2)
    # Range of allowed prices (from 0.25 to 1.00)
    if finalCalculatedPrice_buy < 0.25:  # or finalCalculatedPrice_buy > 1.00:
        finalCalculatedPrice_buy = 0
        optimalPrice = str(finalCalculatedPrice_buy)
    itemName = driver.find_element_by_xpath(
        '//*[@id="largeiteminfo_item_name"]').text
    if finalCalculatedPrice_buy > 0:
        print(">>> Optimal price for [{}] is: {} \n".format(itemName, finalCalculatedPrice_buy))
        optimalPrice = str(finalCalculatedPrice_buy)
        itemsBought += 1
        moneySpent += round((float(optimalPrice) * int(itemsAmount)), 2)
    else:
        print(">>> Price is unacceptable\n")


def PriceCalculator():
    global finalCalculatedPrice
    RegexSearch()
    for i in range(priceListLength):
        try:
            global calculatedPrice
            calculatedPrice=((100 - ((priceList[i] * 100) / priceList[i + 1])))
            if calculatedPrice >= 20:
                finalCalculatedPrice=priceList[i + 1]
                PriceConverter()
                break
        except IndexError:
            finalCalculatedPrice=priceList[0]
            PriceConverter()
            break
        calculatedPrice=((100 - ((priceList[i] * 100) / priceList[i + 1])))
        if calculatedPrice < 20:
            test1=priceList[i - 1]  # last element
            test2=priceList[i]  # first element
            test_result=((100 - ((test2 * 100) / test1)))
            if test_result > 15 < 48:
                finalCalculatedPrice=priceList[i]
                PriceConverter()
            else:
                if test_result < 15 > 5:
                    finalCalculatedPrice=priceList[i]
                    PriceConverter()
                else:
                    # if crap above doesn't do his job => (last / first)
                    finalCalculatedPrice=priceList[i - 1]
                    PriceConverter()
            break


def BuyItems():
    global open_tab
    global listings
    for i in range(10):
        open_tab=driver.find_element_by_xpath(
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
            elem=driver.find_element_by_xpath(
                '//*[@id="market_commodity_buyrequests"]/span[1]')
            ordersAmount=int(elem.text)
        except:
            ordersAmount=0
        try:
            myOrders=driver.find_element_by_xpath(
                '//*[@id="my_market_buylistings_number"]')
            buyOrdersAmount=int(myOrders.text)
            if buyOrdersAmount > 0:
                ordersAmount=0
        except:
            pass
        if ordersAmount < 100:
            # print("Not enough people wants this item or you've already ordered it")
        else:
            # Calculating optimal price
            print('Orders amount is {}'.format(ordersAmount))
            try:
                elem=driver.find_element_by_id('searchResultsRows')
                listings=elem.text
            except:
                elem=driver.find_element_by_id(
                    'market_commodity_forsale_table')
                listings=elem.text
            PriceCalculator()
            # time.sleep(1)
            try:
                driver.find_element_by_xpath(
                    '//*[@id="market_buyorder_info"]/div[1]/div[1]/a').click()
            except:
                driver.find_element_by_xpath(
                    '//*[@id="market_commodity_order_spread"]/div[1]/div/div[1]/a').click()
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


ReductionInit()

usr=input('Enter username: ')
pwd=input('Enter password: ')
itemsPage=input('Enter items page: ')
itemsAmount=input('Enter items amount: ')  # amount of items to buy
print('\nLaunching browser...')

driver=webdriver.Firefox()

wait=WebDriverWait(driver, 3)
sys.setrecursionlimit(10000)

login()
# items list page
driver.get(
    'https://steamcommunity.com/market/search?appid=730&q=Graffiti#p{}_price_asc'.format(str(itemsPage)))

wait.until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="result_0"]/div[2]')))


while True:
    BuyItems()
    # closing tabs
    for i in range(1, 11):
        driver.switch_to_window(driver.window_handles[1])
        try:
            error=driver.find_element_by_id(
                'market_buyorder_dialog_error_text')
            orderLimit=error.text
            RUS_Limit=orderLimit.startswith(
                "Этот запрос на покупку не может быть размещен")
            ENG_Limit=orderLimit.startswith(
                "This buy order cannot be placed")
            if RUS_Limit or ENG_Limit:
                print("Can't buy any more items, press <Enter> to exit")
                print("Money spent in total: ", '\t', moneySpent)
                print("Items bought in total: ", '\t', itemsBought)
                input()
                driver.quit()
        except:
            pass
        driver.close()
    # pressing "next(>)" button
    driver.switch_to_window(driver.window_handles[0])
    driver.find_element_by_xpath('//*[@id="searchResults_btn_next"]').click()
    time.sleep(1.5)

input()
driver.close()
