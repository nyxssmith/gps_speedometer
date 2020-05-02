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


# p.start(2.5) # Initialization
zero()

#pwm_set = set_degree(raw_input("[enter a degree 0-180]"))
def servo_to_degree(degree):
    pwm_set = set_degree(degree)
    GPIO.output(servoPIN, True)
    p.ChangeDutyCycle(pwm_set)
    GPIO.output(servoPIN, False)
    time.sleep(0.1)


d = 0
servo_to_degree(d)
d=45
servo_to_degree(d)
d=90
servo_to_degree(d)
d=0
servo_to_degree(d)

p.stop()
GPIO.cleanup()
