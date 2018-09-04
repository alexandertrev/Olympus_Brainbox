import Adafruit_DHT
from random import randint


class Heat:
    pin_num = None

    def __init__(self, pin):
        self.pin_num = int(pin)

    def get_status(self):
        try:
            humidity, temperature = Adafruit_DHT.read_retry(11, self.pin_num)
            # print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format)
            return temperature
        except Exception as err:
            return 0

    def get_status2(self):
        return randint(0, 100)





