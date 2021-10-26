import numpy as np
import time
import alpaca_trade_api as tradeapi

def algotest(api, symb, hours):
    hours_to_test = hours

    print("Checking Price")
    market_data = api.get_barset(symb, 'minute', limit=(60 * hours_to_test)) # Pull market data from the past 60x minutes

    close_list = []
    for bar in market_data[symb]:
        close_list.append(bar.c)



    print("Open: " + str(close_list[0]))
    print("Close: " + str(close_list[60 * hours_to_test - 1]))


    close_list = np.array(close_list, dtype=np.float64)
    startBal = 2000 # Start out with 2000 dollars
    balance = startBal
    buys = 0
    sells = 0



    for i in range(4, 60 * hours_to_test): # Start four minutes in, so that MA can be calculated
        ma = np.mean(close_list[i-4:i+1])
        last_price = close_list[i]

        print("Moving Average: " + str(ma))
        print("Last Price: " + str(last_price))

        if ma + 0.1 < last_price and not pos_held:
            print("Buy")
            balance -= last_price
            pos_held = True
            buys += 1
        elif ma - 0.1 > last_price and pos_held:
            print("Sell")
            balance += last_price
            pos_held = False
            sells += 1
        print(balance)
        time.sleep(0.01)

    print("")
    print("Buys: " + str(buys))
    print("Sells: " + str(sells))

    if buys > sells:
        balance += close_list[60 * hours_to_test - 1] # Add back your equity to your balance
        

    print("Final Balance: " + str(balance))

    print("Profit if held: " + str(close_list[60 * hours_to_test - 1] - close_list[0]))
    print("Profit from algorithm: " + str(balance - startBal))