import alpaca_trade_api as tradeapi
import keep_alive
import numpy as np
import time
import algotest
keep_alive.keep_alive()



SEC_KEY = '' 
PUB_KEY = '' 
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(key_id= PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)
#stock ticker that is being traded
symb = "ETHUSD"
time.sleep(1)
tradeortest = "trade"
if tradeortest == "test":
  hours = input("How many hours would you like to test for?")
  hours = int(hours)
  algotest.algotest(api, symb, hours)

elif tradeortest == "trade":
  confirm = input("Type confirm to trade:")
  if confirm == "confirm":
    account = api.get_account()
    
    position = api.get_position(symb)
    
 
    
    # if account has money and does not have stock
    if float(account.buying_power)/float(account.multiplier) > 0 and not float(position.qty) > 0:
      pos_held = False
    else:
      pos_held = True
    if pos_held == True:
      print("Currently Holding")
    

    
    

    while True:
      print("")
      print("Checking Price")

      #Get 1 bar object for each of the past 5 minutes.
      market_data = api.get_crypto_bars(symb, "1Min", exchanges='CBSE').df
    
      market_data = market_data.to_numpy()
      # print(market_data)
      # print(type(market_data))

      #stores closing prices from last 5 minutes
      close_list = []
      for i in range(1,6):
        #appends closing price from pandas dataframe table.
        close_list.append( market_data[-i][4])
      # print(close_list)
      
      #turns close_list into a numpy array
      close_list = np.array(close_list, dtype=np.float64)
      
      #Moving Average
      ma = np.mean(close_list)
      print("Moving Average " + str(ma))
      
      # most recent closing price
      
      last_price = close_list[0]
      print("Last Price " + str(last_price))

      # If the MA is more than 10 cents under price and has not been bought yet
      if ma + 1 < last_price and not pos_held:
        print("Buy")
        api.submit_order(
          symbol = symb,
          qty = 0.01,
          side= 'buy',
          type = 'market',
          time_in_force='day'
        )
        pos_held = True
      
      #if MA is more than 10 cents above price, and we have bought it
      elif ma - 1 > last_price and pos_held:
        print("Sell")
        api.submit_order(
          symbol=symb,
          qty=0.01,
          side='sell',
          type='market',
          time_in_force='day'
        )
        pos_held = False

      time.sleep(60)
