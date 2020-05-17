import SetDegreePIGPIO

#import gpsd
#import time
#import threading

import os
from gps import *
from time import *
import time
import threading

gpsd = None #seting the global variable

os.system('clear') #clear the terminal (optional)

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer


def degree_from_speed(speed):
    """
    y=110/177x+185/59
    """
    # ignore speeds below 5 and above 110, dont care about speedo at those speeds
    if speed < 5:
        return 0
    elif speed > 110:
        return 110
    degree = (float(110) / float(117)) * float(speed) + (float(185) / float(59))
    return degree


def get_input():
    while 1:
        a = input("enter a speed")
        b = degree_from_speed(a)
        setdegree.set_degree(b)

    setdegree.stop()


def get_speed():
    last_speeds = [0,0,0,0,0]
    while 1:
        #os.system('clear')
        speed = gpsd.fix.speed
        try:
            t = int(speed)
        except:
            print(speed)
            speed = sum(last_speeds) / 5
            #speed = 0
            
        speed = float(speed) * 2.237
        speed = round(speed)
        last_speeds.append(speed)
        last_speeds.pop(0)
        #print("speed",speed)
        degree = degree_from_speed(speed)
        setdegree.set_degree(degree)
       


def zero_to_hundred():
    d = degree_from_speed(0)
    setdegree.to(d)
    time.sleep(1)
    d = degree_from_speed(100)
    setdegree.to(d)
    time.sleep(1)
    d = degree_from_speed(0)
    setdegree.to(d)
    time.sleep(1)

if __name__ == "__main__":
    pin = 17
    setdegree = SetDegreePIGPIO.SetDegree(pin)
    gpsp = GpsPoller()
    gpsp.start()
    try:

        setdegree.to(0)

        zero_to_hundred()

        input_thread = threading.Thread(target=get_speed)
        input_thread.start()

        setdegree.hold()
        
    except (KeyboardInterrupt, SystemExit):
        print "\nKilling Thread..."
        gpsp.running = False
        gpsp.join()
        input_thread.join()
        

"""
180 degrees is 115mph


3.5 degree is 5 mph
0 degree is 0 mph
"""

# TODO make read from speed file?
# TODO move all to v2 repo
