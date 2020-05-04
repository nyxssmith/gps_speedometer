import RPi.GPIO as GPIO
import time
import copy

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

servo = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
global current_pwm,last_pwm
current_pwm = 2.5
last_pwm = 2.5

#def zero():
#    global current_pwm, current_degree
#    servo.start(2.5)
#    current_degree = 0
#    current_pwm = 2.5


def get_pwm_from_degree(degree):
    degree = float(degree)
    # print(degree)
    pwm = degree / 18 + 2.5
    # print("pwm out " + str(duty))
    return pwm


def send_pwm_to_servo(pwm, servo):
    global last_pwm,current_pwm
    # if theres a change to the pwm
    if float(pwm) != float(last_pwm):
        print("sending pwm to servo old:new",current_pwm,pwm)
        last_pwm = copy.copy(current_pwm)
        current_pwm = pwm
        GPIO.output(servoPIN, True)
        servo.ChangeDutyCycle(pwm)
        GPIO.output(servoPIN, False)
        time.sleep(0.1)




# p.start(2.5) # Initialization
#zero()
servo.start(2.5) #init servo
try:
    while True:
        # pwm_set = set_degree(raw_input("[enter a degree 0-180]"))
        degree_to_set = raw_input("[enter a degree]")
        pwm_to_send = get_pwm_from_degree(degree_to_set)
        send_pwm_to_servo(pwm_to_send, servo)

except KeyboardInterrupt:
    servo.stop()
    GPIO.cleanup()
