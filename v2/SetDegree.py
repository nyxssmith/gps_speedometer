try:
    import RPi.GPIO as GPIO
except:
    print("not running on pi")
    pass
import time
import copy


class SetDegree:
    def __init__(self, pin):
        self.pin_number = pin
        self.running = True

        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin_number, GPIO.OUT)
            self.pwn_pin = GPIO.PWM(pin, 50)  # GPIO 17 for PWM with 50Hz
        except:
            print("not running on pi or failed to set mode of pin")
            pass

        self.degree = float(0)
        self.last_degree = float(0)
        self.delay = 0.1
        return

    def to(self, degree, pin_on=True, pin_off=True):
        # print("degree set to {}".format(degree))
        duty = self.degree / 18 + 2.5
        try:
            if pin_on:
                GPIO.output(self.pin_number, True)
            self.pwn_pin.ChangeDutyCycle(duty)
            if pin_off:
                GPIO.output(self.pin_number, False)
        except:
            pass
        time.sleep(self.delay)
        if int(self.last_degree) != int(self.degree):
            print("degree changed from {} to {}".format(self.last_degree, self.degree))
            self.last_degree = copy.copy(self.degree)

    def hold(self):
        try:
            GPIO.output(self.pin_number, True)
        except:
            pass
        # TODO maybe if turns off the pin output so it would set output to true and not back to false
        while self.running:
            self.to(self.degree, pin_on=False, pin_off=False)
        return

    def set_degree(self, degree):
        self.last_degree = copy.copy(self.degree)
        self.degree = float(degree)
        return

    def stop(self):
        self.running = False
        self.hold_thread.join()
        return
