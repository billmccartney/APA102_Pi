from threading import Thread
from time import sleep
running = True
new_data = True
numLEDs = 100
lights = [0xffffff] * numLEDs

WAKE_ON_LAN = "/usr/bin/wakeonlan"
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import colorschemes
import apa102


def background(arg):
  global running, lights, new_data
  strip = apa102.APA102(numLEDs=200, globalBrightness=4, order="rgb") # Initialize the strip
  strip.clearStrip()
  strip.show()
  while running:
    if(new_data):
      try:
        for i in range(0, 4):
          strip.setPixelRGB(i,lights[i])
        new_data = False
        strip.show()
      except:
        import traceback
        print(traceback.format_exc())
        print("Failed to run")
    else:
      sleep(0.03)
  strip.cleanup()
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
  lights[int(number)] = int(value)
  new_data = True
  return "success"

@app.route("/multiple_leds/<start>/<end>/<value>")
def multiple_leds(start, end, value):
  global new_data
  global lights
  if(start > end):
    return "Failed"
  for index in xrange(start, end+1):
    lights[int(index)] = int(value)
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
