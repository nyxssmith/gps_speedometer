import SetDegree

import threading

pin = 17
setdegree = SetDegree.SetDegree(pin)


def get_input():
    while 1:
        a = input("enter a degree")
        setdegree.set_degree(a)
    setdegree.stop()

print("im here")
setdegree.to(1)
#TODO figure out why this isnt setting the pin
input_thread = threading.Thread(target=get_input)
input_thread.start()

setdegree.hold()
