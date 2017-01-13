from threading import Thread
from time import sleep
running = True
new_data = True
lights = [1,1,1,1]

WAKE_ON_LAN = "/usr/bin/wakeonlan"
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import colorschemes


numLEDs = 100
def background(arg):
  global running, lights, new_data
  strip = apa102.APA102(numLEDs=200, globalBrightness=4, order="rgb") # Initialize the strip
  strip.clearStrip()
  strip.show()
  while running:
    if(new_data):
      try:
        for i in xrange(0, 4):
          if(lights[i]):
            strip.setPixelRGB(i,0xff,0xff,0xff)
          else:
            strip.setPixelRGB(i,0,0,0)
        new_data = False
        strip.show()
      except:
        print "Failed to run"

title = "Rainbow"
"""
def background(arg):
  global running
  while running:
    sceme = eval("colorschemes."+title)
    print("title = ",title)
    try:
      myCycle = sceme(numLEDs=numLEDs, pauseValue=0.00001, numStepsPerCycle = 255, numCycles = 2, globalBrightness=10)
      myCycle.start()
    except:
      print "Failed to run"
    #sleep(0.001)
"""
from flask import Flask
import subprocess
app = Flask(__name__, static_url_path="/static", static_folder="static")

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/leds/<number>/<value>")
def leds(number, value):
  global new_data
  global lights
  lights[number] = value
  new_data = True
  return "success"

@app.route("/wakeonlan/<mac>")
def wakeonlan(mac):
  print("mac = ",mac)
  subprocess.call([WAKE_ON_LAN, mac])
  return "sent packet"

#Here's a full set of arguments we could add
#numLEDs, pauseValue = 0, numStepsPerCycle = 100, numCycles = -1, globalBrightness = 4
@app.route("/light/<name>/<value>")
def setLight(name, value):
  print("setting = ",name, value)
  global title
  title = name
  return "sent packet"


if __name__ == "__main__":
  thread = Thread(target = background, args = (10, ))
  thread.start()
  app.run(host= '0.0.0.0', threaded=True)
  running = False
  thread.join()
#    app.run()
