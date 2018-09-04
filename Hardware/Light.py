from random import randint
import Adafruit_ADS1x15


class Light:
    pin_num = None
    try:
        adc = Adafruit_ADS1x15.ADS1115()
    except Exception as err:
        print(err)

    def __init__(self, pin):
        self.pin_num = int(pin)

    def get_status(self):
        try:
            raw_data = self.adc.read_adc(self.pin_num, gain=1)
            if raw_data > 30700:
                return 100
            if raw_data == 0:
                return 0
            return int(raw_data * 100 / 30700)

        except Exception as err:
            return 0

    def convert_to_string(self, arg_val):
        light_val = int(arg_val)
        if 90 <= light_val <= 100:
            return 'Full sun'
        elif 75 <= light_val <= 89:
            return 'Partial sun'
        elif 30 <= light_val <= 74:
            return 'Shady'
        elif 0 <= light_val <= 29:
            return 'Full Shade'
