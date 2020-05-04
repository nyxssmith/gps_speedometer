import SetDegreePIGPIO

import threading

pin = 17
setdegree = SetDegreePIGPIO.SetDegree(pin)


def get_input():
    while 1:
        a = input("enter a degree")
        setdegree.set_degree(a)
    setdegree.stop()

setdegree.to(0)
#TODO figure out why this isnt setting the pin
input_thread = threading.Thread(target=get_input)
input_thread.start()

setdegree.hold()
