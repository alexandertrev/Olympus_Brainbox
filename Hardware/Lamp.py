from random import randint
import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class Lamp:
    pin_num = None

    def __init__(self, pin, lamp_status):
        self.pin_num = int(pin)
        self.is_on = lamp_status
        GPIO.setup(self.pin_num, GPIO.OUT)
        GPIO.output(self.pin_num, GPIO.HIGH)

    def lamp_off(self):
        print('Turning lamp off...')
        self.is_on = False
        GPIO.output(self.pin_num, GPIO.HIGH)

    def lamp_on(self):
        print('Turning lamp on...')
        self.is_on = True
        GPIO.output(self.pin_num, GPIO.LOW)
