#! python3
# SPC.py - Steam Price Calculator

import re
import pyperclip
from itertools import groupby
#---------------------------------
per = 140  # Price reduction in % |
#---------------------------------


def PriceConverter():
    cpp_buy = cpp / per * 100
    if cpp_buy < 0.25 or cpp_buy > 1.00:
        cpp_buy = 0
    pyperclip.copy(str(cpp_buy))
    print(">>> Optimal price", "[",cpp_buy,"]", "is copied to your clipboard\n")
    start()


def PriceCalculator():
    global cpp
    while True:
        priceRegex = re.compile(r'\d?\d\,\d?\d?')  # Search by type 00,00
        prices = priceRegex.findall(pyperclip.paste())
        prices = [w.replace(',', '.') for w in prices]
        prices = list(map(float, prices))
        ps = [el for el, _ in groupby(prices)]
        ps.sort()
        psl = len(ps)
        if psl < 2:  # if list contains only 1 element
            try:
                cpp = ps[0]
                PriceConverter()
            except:
                start()
        try:
            for i in range(psl):
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
        except:
            start()

        start()


def start():  # Launch by pressing Enter
    go = input("Copy list of lots from market, then press Enter\n")
    if go == '':
        PriceCalculator()
    else:
        start()


start()
