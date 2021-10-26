import alpaca_trade_api as tradeapi

SEC_KEY = '' 
PUB_KEY = '' 
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(key_id= PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)

#buys qty# of symbol stock
api.submit_order(
  symbol='SPY',
  qty=1,
  side='buy',
  type='market', 
  time_in_force='gtc' # Good 'til cancelled
)

#sells qty# of symbol stock
api.submit_order(
  symbol='SPY',
  qty=1,
  side='sell',
  type='market',
  time_in_force='gtc'
)