import RPi.GPIO as GPIO
import time

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz

current_degree = 0
global current_pwm
current_pwm =2.5

def zero():
    global current_pwm,current_degree
    p.start(2.5)
    current_degree = 0
    current_pwm = 2.5
def set_degree(degree):
    """
    0 2.5
    90 7.5
    180 12.5



    """
    degree = float(degree)
    print(degree)

    pwm_out = (degree/45)+2.5
    duty = degree / 18 + 2.5

    print("pwm out "+str(duty))

    return duty


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

    closest_value = find_closest_value(speed, degree_to_speed.values())
    for key in degree_to_speed.keys():
        if degree_to_speed[key] == closest_value:
            closest_key = key
            break
    print("speed", speed, "closest key is", closest_key)
    speed_at_key = degree_to_speed[closest_key]
    print("speed at that key is", speed_at_key)
    dist_away = speed - speed_at_key
    print("dist away", dist_away)
    if dist_away < 0:
        pass

    multiplier = degree_to_multiplier[closest_key]
    degree = closest_key + dist_away * multiplier
    # print("speed*1/.5944", speed * (1 / .594444444))
    print("degree to set", degree)
    return degree


# p.start(2.5) # Initialization
zero()
try:
    while True:


        #pwm_set = set_degree(raw_input("[enter a degree 0-180]"))
        degree_to_set = set_degree_from_speed(raw_input("[enter a speed]"))
        pwm_set = set_degree(degree_to_set)
        GPIO.output(servoPIN, True)
        p.ChangeDutyCycle(pwm_set)
        GPIO.output(servoPIN, False)
        time.sleep(0.1)
        """
        
        p.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        p.ChangeDutyCycle(10)
        time.sleep(0.5)
        p.ChangeDutyCycle(12.5)
        time.sleep(0.5)
        p.ChangeDutyCycle(10)
        time.sleep(0.5)
        p.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        p.ChangeDutyCycle(5)
        time.sleep(0.5)
        p.ChangeDutyCycle(2.5)
        time.sleep(0.5)
        """
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
