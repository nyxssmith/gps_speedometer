import gpsd

global debug
#set debug to true for manual entry, this way it doesnt have to be moving
debug = True


def get_speed():
    if debug:
        speed = input("Enter a debug speed (m/s)")
    else:
        packet = gpsd.get_current()
        speed = packet.speed()

    speed = float(speed) * 2.237
    speed = round(speed)
    return speed

#takes the speed, uses it and past speed to make line, based on line, returns the state of the car
def find_state(speed):
    #three states of increasing speed, staying same speed, decresing speed
    states = ["accelerating","traveling","decelerating"]

    return states[0]


if __name__ == '__main__':


    try:
        gpsd.connect()

        packet = gpsd.get_current()
    except:
        print("cant connect to gpsd")
        exit(1)

    last_speed = -1

    while True:

        speed = get_speed()
        print("speed: " + str(speed)+" mph")
        print(find_state(speed))
        last_speed = speed
