

class Profile:
    name = 'profile'

    def __init__(self, profile):
        self.light = profile[1]
        self.heatMin = profile[2]
        self.heatMax = profile[3]
        self.moistMin = profile[4]
        self.moistMax = profile[5]
        self.location = profile[6]
        self.fix_doors = profile[7]
        self.fix_lamp = profile[8]
        self.fix_pump = profile[9]

    def get_profile(self):
        profile = {}
        profile['light'] = self.light
        profile['heatMin'] = self.heatMin
        profile['heatMax'] = self.heatMax
        profile['moistMin'] = self.moistMin
        profile['moistMax'] = self.moistMax
        profile['location'] = self.location
        profile['fix_doors'] = self.fix_doors
        profile['fix_lamp'] = self.fix_lamp
        profile['fix_pump'] = self.fix_pump

        return profile
