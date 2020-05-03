try:
    import RPi.GPIO as GPIO
except:
    pass
import time
import threading
import copy


class SetDegree:
    def __init__(self, pin):
        self.pin_number = pin

        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin_number, GPIO.OUT)
            self.pwn_pin = GPIO.PWM(pin, 50)  # GPIO 17 for PWM with 50Hz
        except:
            pass

        self.degree = float(0)
        self.last_degree = float(0)
        self.delay = 0.1

        self.hold_thread = threading.Thread(target=self.hold)
        self.hold_thread.start()

        return

    def to(self, degree):
        self.last_degree = copy.copy(self.degree)
        self.degree = float(degree)
        # print("degree set to {}".format(degree))
        duty = degree / 18 + 2.5
        try:
            GPIO.output(self.pin_number, True)
            self.pwn_pin.ChangeDutyCycle(duty)
            GPIO.output(self.pin_number, False)
        except:
            pass
        time.sleep(self.delay)
        if self.last_degree != self.degree:
            print("degree changed from {} to {}".format(self.last_degree, self.degree))

    def hold(self):
        while 1:
            self.to(self.degree)
        return
