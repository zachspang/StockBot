import alpaca_trade_api as tradeapi
import keep_alive
import numpy as np
import time
import algotest
keep_alive.keep_alive()



SEC_KEY = 'PVZEOg56YlMyxUlxcLVJte0iBO7a1x68RrXla058' 
PUB_KEY = 'PKX2IDT410UF4PRQTFM0' 
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(key_id= PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)
#stock ticker that is being traded
symb = "MSFT"
time.sleep(1)
tradeortest = input("Input test or trade:")
if tradeortest == "test":
  hours = input("How many hours would you like to test for?")
  hours = int(hours)
  algotest.algotest(api, symb, hours)

elif tradeortest == "trade":
  confirm = input("Type confirm to trade:")
  if confirm == "confirm":
    pos_held = False

    while True:
      print("")
      print("Checking Price")

      #Get 1 bar object for each of the past 5 minutes.
      market_data = api.get_barset(symb, 'minute', limit=5)

      #stores closing prices from last 5 minutes
      close_list = []
      for bar in market_data[symb]:
        #bar.c is the closing price of that bar's time interval
        close_list.append(bar.c)
      
      #turns close_list into a numpy array
      close_list = np.array(close_list, dtype=np.float64)
      #Moving Average
      ma = np.mean(close_list)
      # most recent closing price
      last_price = close_list[4]

      print("Moving Average " + str(ma))
      print("Last Price " + str(last_price))

      # If the MA is more than 10 cents under price and has not been bought yet
      if ma + 0.1 < last_price and not pos_held:
        print("Buy")
        api.submit_order(
          symbol = symb,
          qty = 0.0316,
          side= 'buy',
          type = 'market',
          time_in_force='day'
        )
        pos_held = True
      
      #if MA is more than 10 cents above price, and we have bought it
      elif ma - 0.1 > last_price and pos_held:
        print("Sell")
        api.submit_order(
          symbol=symb,
          qty=0.0316,
          side='sell',
          type='market',
          time_in_force='day'
        )
        pos_held = False

      time.sleep(60)
