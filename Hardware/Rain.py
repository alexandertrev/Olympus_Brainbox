from random import randint
import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class Rain:
    pin_num = None
    sleep_time = 0.2

    def __init__(self, pin):
        self.pin_num = int(pin)
        GPIO.setup(self.pin_num, GPIO.IN)

    def get_status2(self):
        return randint(0, 10)

    def get_status(self):
        drop_counter = 0
        try:
            for i in range(0, 10):  # 3 out of 10 checks found water drops
                state = GPIO.input(self.pin_num)
                if state != 1:
                    drop_counter += 1
                if drop_counter == 3:
                    return 1  # rainy
                time.sleep(self.sleep_time)
            return 0

        except Exception as err:
            return -1
