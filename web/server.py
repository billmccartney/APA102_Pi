from threading import Thread
from time import sleep
running = True

WAKE_ON_LAN = "/usr/bin/wakeonlan"

def background(arg):
  global running
  while running:
    print( "running")
    sleep(1)

from flask import Flask
import subprocess
app = Flask(__name__, static_url_path="/static", static_folder="static")

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/wakeonlan/<mac>")
def wakeonlan(mac):
  print("mac = ",mac)
  subprocess.call(WAKE_ON_LAN, mac)
  return "sent packet"


if __name__ == "__main__":
  thread = Thread(target = background, args = (10, ))
  thread.start()
  app.run(host= '0.0.0.0', threaded=True)
  running = False
  thread.join()
#    app.run()
