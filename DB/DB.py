import sqlite3
import sys
import os as os
import iPlant.profile
import time


class PiDB:
    conn = None
    c = None

    def __init__(self):
        if not os.path.exists('piDB'):
            print('iPlant DB exists? --> Doesnt exist')
            self.create_db()
        else:
            print('iPlant DB exists? --> Exist')

        self.conn = sqlite3.connect('piDB')
        self.c = self.conn.cursor()

    def __del__(self):
        self.c.close()
        self.conn.close()

    # ............................SENSORS...............................................................
    # ................................................................................................

    def insert_sensors_log(self, data):
        light = data['light']
        heat = data['heat']
        moist = data['moist']
        water_lvl = data['water_lvl']
        doors = data['doors']
        lamp = data['lamp']

        with self.conn:
            self.c.execute("INSERT INTO sensors_log values (:prob_date,:light,:heat,:moist,:water_lvl,:doors,:lamp)",
                           {'prob_date': time.time(), 'light': light, 'heat': heat, 'moist': moist,
                            'water_lvl': water_lvl, 'doors': doors, 'lamp': lamp})

    def get_sensors_log(self):
        self.c.execute("""SELECT * 
                          FROM sensors_log 
                          WHERE prob_date = (SELECT MAX(prob_date) FROM sensors_log)
                      """)
        return self.c.fetchone()

    def get_many_sensors_logs(self, arg):
        self.c.execute("""SELECT * 
                          FROM sensors_log 
                          ORDER BY prob_date desc
                      """)
        return self.c.fetchmany(arg)

    # ............................LAST-SENSOR-LOG...............................................................
    # ................................................................................................

    def insert_last_sensors_log(self, data):
        light = data['light']
        heat = data['heat']
        moist = data['moist']
        water_lvl = data['water_lvl']
        doors = data['doors']
        lamp = data['lamp']

        with self.conn:
            self.c.execute("INSERT INTO last_sensors_log values (:prob_date,:light,:heat,:moist,:water_lvl,:doors,:lamp)",
                           {'prob_date': time.time(), 'light': light, 'heat': heat, 'moist': moist,
                            'water_lvl': water_lvl, 'doors': doors, 'lamp': lamp})

    def get_last_sensors_log(self):
        self.c.execute("""SELECT * 
                          FROM last_sensors_log 
                          WHERE prob_date = (SELECT MAX(prob_date) FROM last_sensors_log)
                      """)
        return self.c.fetchone()

    def remove_last_sensors_log(self):
        with self.conn:
            self.c.execute("DELETE FROM last_sensors_log")

    # ..............................PROFILE...........................................................
    # ................................................................................................

    def set_profile(self, arg_profile):
        with self.conn:
            self.c.execute("INSERT INTO profile values (:name,:light,:heatMin,:heatMax,:moistMin,:moistMax,:location,"
                           ":fix_doors,:fix_lamp,:fix_pump)",
                           {'name': 'profile',
                            'light': arg_profile['light'],
                            'heatMin': arg_profile['heatMin'],
                            'heatMax': arg_profile['heatMax'],
                            'moistMin': arg_profile['moistMin'],
                            'moistMax': arg_profile['moistMax'],
                            'location': arg_profile['location'],
                            'fix_doors': arg_profile['fix_doors'],
                            'fix_lamp': arg_profile['fix_lamp'],
                            'fix_pump': arg_profile['fix_pump']
                            })

    def delete_profile(self):
        with self.conn:
            self.c.execute("DELETE FROM profile WHERE name = 'profile'")

    def get_profile(self):
        self.c.execute("""SELECT * 
                          FROM profile
                      """)
        return self.c.fetchone()

    def update_profile(self, arg_profile):
        with self.conn:
            arg_light = arg_profile['light']
            arg_heatMin = arg_profile['heatMin']
            arg_heatMax = arg_profile['heatMax']
            arg_moistMin = arg_profile['moistMin']
            arg_moistMax = arg_profile['moistMax']
            arg_location = arg_profile['location']
            arg_fix_doors = arg_profile['fix_doors']
            arg_fix_lamp = arg_profile['fix_lamp']
            arg_fix_pump = arg_profile['fix_pump']

            self.c.execute("""UPDATE profile
                              SET light = ?, heatMin = ?, heatMax = ?,
                                  moistMin = ?, moistMax = ?, location = ?, fix_doors = ?, fix_lamp = ?, fix_pump = ?
                              WHERE name='profile';
                          """, (arg_light, arg_heatMin, arg_heatMax, arg_moistMin, arg_moistMax, arg_location,
                                arg_fix_doors, arg_fix_lamp, arg_fix_pump))

    # ..............................WATERING............................................................
    # ................................................................................................

    def insert_water(self, arg_val):
        with self.conn:
            self.c.execute("INSERT INTO water values (:wateredTime,:amount)",
                           {'wateredTime': time.time(), 'amount': arg_val})

    def get_last_waterTime(self):
        self.c.execute("""SELECT * 
                          FROM water
                          WHERE wateredTime = (SELECT MAX(wateredTime) FROM water)
                      """)
        return self.c.fetchone()

    def get_many_waterTimes(self, arg):
        self.c.execute("""SELECT * 
                          FROM water 
                          ORDER BY wateredTime desc
                      """)
        return self.c.fetchmany(arg)

    # ..............................CONFIG............................................................
    # ................................................................................................

    def set_config(self, arg_config):
        with self.conn:
            self.c.execute("INSERT INTO pi_config values (:name,:light,:water_lvl,:moist,:heat,:rain,:pump,:lamp,"
                           ":door_left,:door_right)",
                           {'name': 'config',
                            'light': arg_config[1],
                            'water_lvl': arg_config[2],
                            'moist': arg_config[3],
                            'heat': arg_config[4],
                            'rain': arg_config[5],
                            'pump': arg_config[6],
                            'lamp': arg_config[7],
                            'door_left': arg_config[8],
                            'door_right': arg_config[9]
                            })

    def get_config(self):
        self.c.execute("""SELECT * 
                          FROM pi_config
                      """)
        return self.c.fetchone()

    def update_config(self, arg_config):
        with self.conn:
            arg_light = arg_config[1]
            arg_water_lvl = arg_config[2]
            arg_moist = arg_config[3]
            arg_heat = arg_config[4]
            arg_rain = arg_config[5]
            arg_pump = arg_config[6]
            arg_lamp = arg_config[7]
            arg_door_left = arg_config[8]
            arg_door_right = arg_config[9]

            self.c.execute("""UPDATE pi_config
                              SET light = ?, moist = ?, water_lvl = ?, heat = ?,
                                  rain = ?, pump = ?, lamp = ?, door_left = ?, door_right = ?
                              WHERE name='config';
                          """, (arg_light, arg_water_lvl, arg_moist, arg_heat, arg_rain, arg_pump, arg_lamp,
                                arg_door_left, arg_door_right))

    # .............................DB-CREATION........................................................
    # ................................................................................................

    def create_db(self):

        print("----------Begin DB creation-------------")
        try:
            self.conn = sqlite3.connect('piDB')
            self.c = self.conn.cursor()

            self.c.execute("""CREATE TABLE profile(
                                name text primary key,
                                light text,
                                heatMin INTEGER,
                                heatMax INTEGER,
                                moistMin INTEGER,
                                moistMax INTEGER,
                                location text,
                                fix_doors boolean,
                                fix_lamp boolean,
                                fix_pump boolean
                            )""")
            self.c.execute("""CREATE TABLE sensors_log(
                                prob_date text primary key,
                                light INTEGER,
                                heat INTEGER,
                                moist INTEGER,
                                water_lvl INTEGER,
                                doors boolean,
                                lamp boolean
                            )""")
            self.c.execute("""CREATE TABLE last_sensors_log(
                                prob_date text primary key,
                                light INTEGER,
                                heat INTEGER,
                                moist INTEGER,
                                water_lvl INTEGER,
                                doors boolean,
                                lamp boolean
                            )""")
            self.c.execute("""CREATE TABLE water(
                                wateredTime text primary key,
                                amount INTEGER 
                         )""")
            self.c.execute("""CREATE TABLE pi_config(
                                name text primary key,
                                light INTEGER,
                                water_lvl INTEGER,
                                moist INTEGER,
                                heat INTEGER,
                                rain INTEGER,
                                pump INTEGER,
                                lamp INTEGER,
                                door_left text,
                                door_right text
                         )""")

            self.conn.commit()
            self.c.close()
            self.conn.close()
            print('Creation completed successfully without errors!')
        except sqlite3.OperationalError as err:
            print("Error occurred while creating DB: ", err)

        print("----------End DB creation---------------")
