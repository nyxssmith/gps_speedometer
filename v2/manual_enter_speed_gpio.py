import SetDegreePIGPIO

import threading

pin = 17
setdegree = SetDegreePIGPIO.SetDegree(pin)

def degree_from_speed(speed):
    """
    y=110/177x+185/59
    """
    #ignore speeds below 5 and above 110, dont care about speedo at those speeds
    if speed < 5:
        return 0
    elif speed > 110:
        return 110
    degree = (float(110)/float(117))*float(speed)+(float(185)/float(59))
    return degree

def get_input():
    while 1:
        a = input("enter a speed")
        b = degree_from_speed(a)
        setdegree.set_degree(b)
    setdegree.stop()

setdegree.to(0)
input_thread = threading.Thread(target=get_input)
input_thread.start()

setdegree.hold()


"""
180 degrees is 115mph


3.5 degree is 5 mph
0 degree is 0 mph
"""

#TODO make read from speed file?
#TODO move all to v2 repo