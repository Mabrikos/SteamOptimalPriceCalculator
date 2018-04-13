#! python3
# SOPC.py - Steam Optimal Price Calculator

import re
import pyperclip


def ReductionInit():
    global per
    init = input("Reduct price by, %: ")
    try:
        per = int(init) + 100
    except ValueError:
        print('\n>>> Number is required\n')
        ReductionInit()


def PriceConverter():
    cpp_buy = cpp / per * 100
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
    start()


def RegexSearch():
    global ps, ps_length
    priceRegex = re.compile(r'\d?\d\,\d?\d?')  # Search by type 00,00
    prices = priceRegex.findall(pyperclip.paste())
    prices = [w.replace(',', '.') for w in prices]
    prices = list(map(float, prices))
    ps = list(set(prices))
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
                start()
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
            start()

        start()


def start():  # Launch by pressing Enter
    go = input("Copy list of lots from market, then press Enter\n")
    if go == '':
        PriceCalculator()
    else:
        start()


ReductionInit()
start()
