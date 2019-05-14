import gpsd
import RPi.GPIO as GPIO
import time

global last_speed
last_speed = -1

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
#GPIO.setup(1, GPIO.OUT)
#GPIO.setup(6, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz

global current_pwm,init_done,current_degree
current_degree = 0
current_pwm = 2.5
init_done = False


# convert the d
def set_pwm_from_degree(degree):
    """
    0 2.5
    90 7.5
    180 12.5
    """
    degree = float(degree)
    #print(degree)

    duty = degree / 18 + 2.5

    #print("pwm out " + str(duty))

    return duty

# finds coset value of speed to list of speeds
def find_closest_value(num, values):
    best_dist_away = 99999
    best_value = None
    for value in values:
        dist_away = abs(num - value)
        # print("value",value,"dist away",dist_away)
        if dist_away < best_dist_away:
            best_dist_away = dist_away
            best_value = value

    return best_value


def set_degree_from_speed(speed):
    speed = float(speed)
    """
    deg mph
    ,0:0
    ,5:10
    ,13:15
    ,20:20
    ,30:25
    ,38:30
    ,45:35
    ,55:40
    ,63:45
    ,72:50
    ,82:55
    ,90:60
    ,100:65
    ,108:70
    ,125:80
    ,143:90
    ,160:100
    ,180:106.5

    180

    """

    degree_to_speed = {0: 0, 5: 10, 13: 15, 20: 20, 30: 25, 38: 30, 45: 35, 55: 40, 63: 45, 72: 50, 82: 55, 90: 60,
                       100: 65, 108: 70, 125: 80, 143: 90, 160: 100, 180: 106.5}
    degree_to_multiplier = {0: 1,
                            5: 1.1,
                            13: 1.1,
                            20: 1.1,
                            30: 1.2,
                            38: 1.2,
                            45: 1.2,
                            55: 1.2,
                            63: 1.2,
                            72: 1.2,
                            82: 1.2,
                            90: 1.2,
                            100: 1.2,
                            108: 1.2,
                            125: 1.2,
                            143: 1.1,
                            160: 1.1,
                            180: 1}

    # print(degree_to_speed.keys())
    # finds the closest speed to the one given
    closest_value = find_closest_value(speed, degree_to_speed.values())
    for key in degree_to_speed.keys():
        if degree_to_speed[key] == closest_value:
            closest_key = key
            break
    #gets the degree that the closest speed is at
    print("speed", speed, "closest key is", closest_key)
    speed_at_key = degree_to_speed[closest_key]
    print("speed at that key is", speed_at_key)
    #gets the dist away from the base speed for actual speed
    dist_away = speed - speed_at_key

    print("dist away", dist_away)
    if dist_away < 0:
        pass
    #gets the multiper to use for degree modification
    multiplier = degree_to_multiplier[closest_key]
    #sets the degree to set to based on the distance speed is away from base/known speed and its multiper
    degree = closest_key + dist_away * multiplier
    # print("speed*1/.5944", speed * (1 / .594444444))
    print("degree to set", degree)
    return degree

#starts gpsd and set s vars
def init():
    global current_pwm, current_degree, last_speed,init_done
    if init_done:
        return
    try:
        print("Trying to connect to gpsd")
        gpsd.connect()
        last_speed = 0
        p.start(2.5)
        current_degree = 0
        current_pwm = 2.5
    except:
        print("Couldnt connect to gps, trying again in 1 second")
        time.sleep(1)
        init()


    init_done = True
    print("Connected to gpsd and set speed to 0")

#gets the speed from gpsd as a float
def get_speed():
    global last_speed
    try:
        packet = gpsd.get_current()
        speed = packet.speed()
        speed = float(speed) * 2.237
        speed = round(speed)
    except:
        return last_speed

    return speed

#check that speed is at least 2 mph away from last speed
def speed_far_enough_away(speed,last_speeds):
    if abs(speed-last_speed) > 2.5:
        return True
    """
    for l_speed in last_speeds:
        if abs(l_speed-speed) < 2:
            return False
    """
    return False

def add_to_last_speeds(speed,last_speeds):
    if len(last_speeds) == 2:#number of last speeds to keep
        last_speeds.pop()
        last_speeds.append(speed)
    else:
        last_speeds.append(speed)
    return last_speeds

def degree_far_enough_away(degree):
    degree_away = abs(current_degree-degree)
    if degree_away >= 2:
        return True
    return False

def set_pins(on):
    if on:
        GPIO.output(servoPIN, True)
        #GPIO.output(1, True)
        #GPIO.output(6, True)
    else:
        GPIO.output(servoPIN, False)
        #GPIO.output(1, False)
        #GPIO.output(6, False)


def main():
    global last_speed,current_degree

    last_speeds = []
    try:
        while True:
            #get speed
            speed = get_speed()
            #if speed has changed by enough
            if (speed != last_speed and speed_far_enough_away(speed,last_speeds) or (speed <1 and last_speed < 1)):
                print("speed: " + str(speed))
                print("last speed", last_speed)

                print("speed different enough")

                #get the degree to set
                degree_to_set = set_degree_from_speed(speed)
                if degree_far_enough_away(degree_to_set):
                    #if the degree has changed enough
                    print("degree different enough")
                    current_degree = degree_to_set
                    print("Changing speed to point to",speed)
                    pwm_set = set_pwm_from_degree(degree_to_set)
                    set_pins(True)
                    #GPIO.output(servoPIN, True)
                    p.ChangeDutyCycle(pwm_set)
                    set_pins(False)
                    #GPIO.output(servoPIN, False)
                    time.sleep(0.25)
            #turn off servo pin
            #GPIO.output(servoPIN, False)
            set_pins(False)
            time.sleep(0.25)
            last_speed = speed
            last_speeds = add_to_last_speeds(speed,last_speeds)

    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()

#run
init()
main()
