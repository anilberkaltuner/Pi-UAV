
import RPi.GPIO as GPIO
from .misc import ratio


class Servo:
        FREQ = 50
        MAX_WIDTH = 12.0
        MIN_WIDTH = 1.0

        def __init__(self, pin):
                GPIO.setup(pin, GPIO.OUT)
                self.pin = pin
                self.pulse = 0
                self.pwm = GPIO.PWM(self.pin, self.FREQ)
                start_width = ratio(0.5, 0, 1, self.MIN_WIDTH, self.MAX_WIDTH)
                self.pwm.start(self.pulse)

        def set(self, val):
                '''val between 0 and 255'''
                pulse = ratio(val, 0, 255, self.MIN_WIDTH, self.MAX_WIDTH)
                if (pulse != self.pulse):
                    self.pulse = pulse
                    self.pwm.ChangeDutyCycle(self.pulse)


class Esc(Servo):
    '''Electronic speed controler
    '''
    MIN_WIDTH = 5.0
    MAX_WIDTH = 10.0


class Controler:
    STOP = 50

    def __init__(self, sr, sl, esc):
        '''sr: servo right
        sl: servo left
        esc: electronic speed controler
        '''
        GPIO.setmode(GPIO.BCM)
        self.servo_right = Servo(sr)
        self.servo_left = Servo(sl)
        self.esc = Esc(esc)

    def control(self, pitch, roll, throttle):
        self.esc.set(throttle)
        left = ratio(pitch, 0, 255, self.STOP, 255 - self.STOP)
        right = ratio(pitch, 255, 0, self.STOP, 255 - self.STOP)

        sleft = ratio(roll + left, 0, 255 * 2, 0, 255)
        sright = ratio(roll + right, 0, 255 * 2, 0, 255)
        # WIP for testing
        sleft *= 1.5
        sright *= 1.5
        if (sleft > 255):
            sleft = 255
        if (sright > 255):
            sright = 255
        self.servo_right.set(sright)
        self.servo_left.set(sleft)
