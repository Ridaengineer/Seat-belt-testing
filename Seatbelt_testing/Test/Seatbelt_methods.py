#Seatbelt code
import time
import threading

class SeatbeltSystem:
    def __init__(self):
        self.seatbelt_fastened = False
        self.light_color = "off"  # 'off', 'yellow', 'red', 'green'
        self.sound_alarm = False
        self.engine_on = False
        self.people_inside = False
        self.vehicle_speed = 0  # Speed in km/hr

    def fasten_seatbelt(self):
        self.seatbelt_fastened = True
        self.update_alerts()

    def unfasten_seatbelt(self):
        self.seatbelt_fastened = False
        self.update_alerts()

    def update_alerts(self):
        if self.seatbelt_fastened:
            self.light_color = "green"
            self.sound_alarm = False
        else:
            if int(self.engine_on and self.people_inside and self.vehicle_speed) > 40:
                self.light_color = "red"
                self.sound_alarm = True
            else:
                self.light_color = "yellow"
                self.sound_alarm = False

    def is_light_indicator_green(self):  #SC_1
        return self.light_color == "green"

    def is_light_indicator_red(self):     #SC_1
        return self.light_color == "red"

    def is_light_indicator_yellow(self):
        return self.light_color == "yellow"

    def is_sound_alarm_on(self):
        return self.sound_alarm

    def set_engine_on(self, status):
        self.engine_on = status
        self.update_alerts()

    def set_people_inside(self, status):
        self.people_inside = status
        self.update_alerts()

    def set_vehicle_speed(self, speed):
        self.vehicle_speed = speed
        self.update_alerts()

seatbelt_system = SeatbeltSystem()

def fasten_seatbelt():
    seatbelt_system.fasten_seatbelt()

def unfasten_seatbelt():
    seatbelt_system.unfasten_seatbelt()

def is_light_indicator_green():
    return seatbelt_system.is_light_indicator_green()

def is_light_indicator_red():
    return seatbelt_system.is_light_indicator_red()

def is_light_indicator_yellow():
    return seatbelt_system.is_light_indicator_yellow()

def is_sound_alarm_on():
    return seatbelt_system.is_sound_alarm_on()

def set_engine_on(status):
    seatbelt_system.set_engine_on(status)

def set_people_inside(status):
    seatbelt_system.set_people_inside(status)

def set_vehicle_speed(speed):
    seatbelt_system.set_vehicle_speed(speed)

def start_engine():
    set_engine_on(True)

def stop_engine():
    set_engine_on(False)

def person_sits():
    set_people_inside(True)

def person_leaves():
    set_people_inside(False)
