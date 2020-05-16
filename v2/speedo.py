import SetDegreePIGPIO
import gpsd
import time
import threading


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
    fails_before_waggle = 100
    fails = 0
    while 1:
        try:
            packet = gpsd.get_current()
            speed = packet.speed()
            speed = float(speed) * 2.237
            speed = round(speed)
            print("speed",speed)
            degree = degree_from_speed(speed)
            setdegree.set_degree(degree)
        except:
            print("failed to get speed")
            fails+=1
        if fails > fails_before_waggle:
            zero_to_hundred()
            time.sleep(10)
            fails-=900
        else:
            time.sleep(0.1)


def zero_to_hundred():
    d = degree_from_speed(0)
    setdegree.to(d)

    d = degree_from_speed(100)
    setdegree.to(d)

    d = degree_from_speed(0)
    setdegree.to(d)


if __name__ == "__main__":
    pin = 17
    setdegree = SetDegreePIGPIO.SetDegree(pin)

    setdegree.to(0)

    zero_to_hundred()

    input_thread = threading.Thread(target=get_speed)
    input_thread.start()

    setdegree.hold()

"""
180 degrees is 115mph


3.5 degree is 5 mph
0 degree is 0 mph
"""

# TODO make read from speed file?
# TODO move all to v2 repo
