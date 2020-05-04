try:
    import RPi.GPIO as GPIO
    import pigpio
except:
    print("not running on pi")
    pass
import time
import copy


class SetDegree:

    def __init__(self, pin):
        self.pin_number = pin
        self.running = True
        #TODO make a cleanup method for multiple runs w/o reboot

        try:
            self.pi = pigpio.pi() # Connect to local Pi.
        except:
            print("not running on pi or failed to set mode of pin")
            pass

        self.degree = float(0)
        self.last_degree = float(0)
        self.delay = 0.1

    def get_pulsewidth_from_degree(self,degree):
        """
        500 is 0
        2500 is 180

        a\ =\ \frac{100}{9}b+500
        """
        pulsewidth = (float(100)/float(9))*float(degree) + float(500)

        return pulsewidth

    def to(self, degree):
        # print("degree set to {}".format(degree))
        pulsewidth = self.get_pulsewidth_from_degree(degree)
        try:
            self.pi.set_servo_pulsewidth(self.pin_number, pulsewidth)
        except:
            print("failed to set servo to degree")
            pass
        time.sleep(self.delay)
        if int(self.last_degree) != int(self.degree):
            print("degree changed from {} to {}".format(self.last_degree, self.degree))
            self.last_degree = copy.copy(self.degree)

    def hold(self):
        while self.running:
            self.to(self.degree)
        return

    def set_degree(self, degree):
        self.last_degree = copy.copy(self.degree)
        self.degree = float(degree)
        return

    def stop(self):
        self.running = False
        self.pi.stop()
        self.hold_thread.join()

        return
