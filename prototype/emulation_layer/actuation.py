import sys
import nintaco
import pandas as pd
import numpy as np
from kafka import KafkaProducer
import json

print("run with python, not python3")

frameCount = 0;

nintaco.initRemoteAPI("localhost", 9998)
'''
Since this is in python 2.7 due to constraints imposed by nintaco, I want to keep my engagement here to a minimum

This system gets the pixels from the API and Puts them untouched on a kafka queue to be used in the state synthesis layer

I also imagine that this is the point where commands are input once the integration hits that point
'''
producer = KafkaProducer(bootstrap_servers='localhost:9092')
api = nintaco.getAPI()



def launch():
  api.addFrameListener(renderFinished)
  # api.addStatusListener(statusChanged)
  api.addActivateListener(apiEnabled)
  api.addDeactivateListener(apiDisabled)
  api.addStopListener(dispose)
  api.run()

def apiEnabled():
  print("Connection to emulator enabled")

def apiDisabled():
  print("Connection to emulator disabled")

def dispose():
  print("Connection to emulator stopped")

def statusChanged(message):
  print("frameCount: %s" % frameCount)
  print("Status message: %s" % message)

def renderFinished():
    global frameCount
    if frameCount % (64*10) == 0:
        pixels = get_pixels_raw()
        """
        First attempt to send messages to topic from actuation layer

        Imagine this will fail without some initial setup
        """
        result = producer.send('emulator_to_environment', json.dumps(pixels))
        print('Sent message to emulator_to_environment with result: ', result)
        frameCount = 0
    frameCount += 1

def get_pixels_raw():
    pixels = [0] * (256*240)
    api.getPixels(pixels)
    return pixels


if __name__ == "__main__":
    launch()
