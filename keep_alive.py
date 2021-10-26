from flask import Flask
from threading import Thread

#creates web sever
app = Flask('')

#route to handle https requests 

@app.route('/')
def main():
  return "Your bot is alive!"

def run():
  app.run(host="0.0.0.0", port=8080)

#call and ping server
def keep_alive():
  server= Thread(target=run)
  server.start()

