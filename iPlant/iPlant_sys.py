from Hardware import Heat, Light, Moist, Rain, WaterLvl, Pump, Doors, Lamp
from . import profile


class IPlantSys:
    profile = None
    num_of_forced_pumps = 1

    def __init__(self, mac, arg_config):
        print('Current config: ', arg_config)

        self.mac = mac
        self.light = Light.Light(arg_config[1])
        self.water_lvl = WaterLvl.WaterLvl(arg_config[2])
        self.moist = Moist.Moist(arg_config[3])
        self.heat = Heat.Heat(arg_config[4])
        self.rain = Rain.Rain(arg_config[5])
        self.pump = Pump.Pump(arg_config[6])
        self.lamp = Lamp.Lamp(arg_config[7], False)
        self.doors = Doors.Doors(arg_config[8], arg_config[9], False)

    # Finished
    def set_pins_config(self, arg_config):
        self.light = Light.Light(arg_config[1])
        self.water_lvl = WaterLvl.WaterLvl(arg_config[2])
        self.moist = Moist.Moist(arg_config[3])
        self.heat = Heat.Heat(arg_config[4])
        self.rain = Rain.Rain(arg_config[5])
        self.pump = Pump.Pump(arg_config[6])
        self.lamp = Lamp.Lamp(arg_config[7], False)
        self.doors = Doors.Doors(arg_config[8], arg_config[9], False)

    # Finished
    def set_profile_from_db(self, newProfile):
        self.profile = profile.Profile(newProfile)

    # Finished
    def set_profile_from_server(self, newProfile):
        arr_sensors = []
        arr_sensors.append('profile')
        arr_sensors.append(newProfile['light'])
        arr_sensors.append(int(newProfile['heatMin']))
        arr_sensors.append(int(newProfile['heatMax']))
        arr_sensors.append(int(newProfile['moistMin']))
        arr_sensors.append(int(newProfile['moistMax']))
        arr_sensors.append(newProfile['location'])
        arr_sensors.append(newProfile['fix_doors'])
        arr_sensors.append(newProfile['fix_lamp'])
        arr_sensors.append(newProfile['fix_pump'])
        self.profile = profile.Profile(arr_sensors)

    # Finished
    def get_sensors_status(self):
        print('Checking current sensors status...')
        arr_sensors = {
            'mac': self.mac,
            'heat': self.check_heat(),
            'light': self.check_light(),
            'moist': self.check_moist(),
            'water_lvl': self.check_water_lvl(),
            'doors': self.check_doors(),
            'rain': self.check_rain(),
            'lamp': self.check_lamp()
        }

        return arr_sensors

    # Finished
    def return_def_pump_amount(self):
        return self.pump.def_pump_amount

    # Finished Sts
    def check_rain(self):
        return self.rain.get_status()

    # Finished Sts
    def check_heat(self):
        return self.heat.get_status()

    # Finished Sts
    def check_light(self):
        return self.light.get_status()

    # Finished Sts
    def check_moist(self):
        return self.moist.get_status()

    # Finished Sts
    def check_water_lvl(self):
        return self.water_lvl.get_water_lvl()

    # Finished Sts
    def check_doors(self):
        return self.doors.isDoorsOpen()

    # Finished Sts
    def check_lamp(self):
        return self.lamp.is_on

    # Finished
    def check_if_enough_water_lvl(self):
        return self.water_lvl.is_enough_water()

    # TODO: Started - need to finish
    def water_now(self):
        num_of_pumps = 0

        print("Watering in progress!")
        self.pump.pump_now()
        num_of_pumps = num_of_pumps + 1

        pump_amount = num_of_pumps * self.pump.def_pump_amount
        return pump_amount

    # TODO: Started - in progress
    def water_now_forced(self):
        print("Forced Watering in progress!")
        for i in range(self.num_of_forced_pumps):
            self.pump.pump_now()

        pump_amount = self.num_of_forced_pumps*self.pump.def_pump_amount
        return pump_amount

    # TODO: Started - need to do
    def check_if_need_water(self):
        curMoist = self.moist.get_status()
        print('Current moist: ', curMoist, '| Profile moistMin: ', self.profile.moistMin)

        if self.profile.moistMin <= curMoist:
            return False
        return True

    # Finished Sts
    def check_fix_door(self):
        return self.profile.fix_doors

    # Finished Sts
    def check_fix_lamp(self):
        return self.profile.fix_lamp

    # Finished Sts
    def check_fix_pump(self):
        return self.profile.fix_pump
