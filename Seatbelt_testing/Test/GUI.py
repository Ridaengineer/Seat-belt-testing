#Graphical user interface
import tkinter as tk
from tkinter import messagebox
import Seatbelt_methods as seatbelt
import threading
import time
import pygame

class SeatBeltGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Seat Belt System")
        self.blinking = False  # Variable to track blink status

        # Initialize pygame for alarm sound
        pygame.mixer.init()
        self.alarm_sound = pygame.mixer.Sound("alarm_sound.wav")  # Make sure we have the 'alarm_sound.wav' file in the same directory

        # Seat Belt Fastened Button and Scale
        self.fasten_var = tk.IntVar()
        self.fasten_var.set(0)  # Initial state: unfastened

        self.fasten_button = tk.Checkbutton(root, text="Seat Belt Fastened", variable=self.fasten_var, command=self.update_seatbelt_state, onvalue=1, offvalue=0)
        self.fasten_button.grid(row=0, column=0, padx=5, pady=5)

        self.fasten_scale = tk.Scale(root, from_=0, to=1, orient=tk.HORIZONTAL, variable=self.fasten_var, label="Seat Belt State", command=self.update_seatbelt_state)
        self.fasten_scale.grid(row=0, column=1, padx=5, pady=5)

        # People Inside Button
        self.people_inside_var = tk.IntVar()
        self.people_inside_var.set(0)  # Initial state: nobody inside

        self.people_inside_button = tk.Checkbutton(root, text="People Inside", variable=self.people_inside_var, command=self.update_people_inside, onvalue=1, offvalue=0)
        self.people_inside_button.grid(row=1, column=0, padx=5, pady=5)

        # Engine On Button
        self.engine_on_var = tk.IntVar()
        self.engine_on_var.set(0)  # Initial state: engine off

        self.engine_on_button = tk.Checkbutton(root, text="Engine On", variable=self.engine_on_var, command=self.update_engine_on, onvalue=1, offvalue=0)
        self.engine_on_button.grid(row=1, column=1, padx=5, pady=5)

        # Vehicle Speed Scale
        self.speed_label = tk.Label(root, text="Vehicle Speed (km/hr):")
        self.speed_label.grid(row=2, column=0, padx=5, pady=5)

        self.speed_var = tk.DoubleVar()
        self.speed_var.set(0)  # Initial speed: 0 km/hr

        self.speed_scale = tk.Scale(root, from_=0, to=200, orient=tk.HORIZONTAL, variable=self.speed_var, label="Vehicle Speed", command=self.update_speed)
        self.speed_scale.grid(row=2, column=1, padx=5, pady=5)

        # Light Status Indicators
        self.light_label = tk.Label(root, text="Light Status:")
        self.light_label.grid(row=3, column=0, padx=5, pady=5)

        self.light_green_canvas = tk.Canvas(root, width=30, height=30, bg="white", highlightthickness=0)
        self.light_green_canvas.grid(row=3, column=1, padx=5, pady=5)
        self.light_green = self.light_green_canvas.create_oval(5, 5, 25, 25, fill="gray")

        self.light_yellow_canvas = tk.Canvas(root, width=30, height=30, bg="white", highlightthickness=0)
        self.light_yellow_canvas.grid(row=3, column=2, padx=5, pady=5)
        self.light_yellow = self.light_yellow_canvas.create_oval(5, 5, 25, 25, fill="gray")

        self.light_red_canvas = tk.Canvas(root, width=30, height=30, bg="white", highlightthickness=0)
        self.light_red_canvas.grid(row=3, column=3, padx=18, pady=5)
        self.light_red = self.light_red_canvas.create_oval(5, 5, 25, 25, fill="gray")

        # Alarm Indicator
        self.alarm_canvas = tk.Canvas(root, width=30, height=30, bg="white", highlightthickness=0)
        self.alarm_canvas.grid(row=3, column=4, padx=5, pady=5)
        self.alarm_indicator = self.alarm_canvas.create_oval(5, 5, 25, 25, fill="black")

        # Check Status Button
        self.check_status_button = tk.Button(root, text="Check Status", command=self.check_status)
        self.check_status_button.grid(row=4, column=0, columnspan=5, padx=5, pady=5)

    def update_seatbelt_state(self, *args):
        state = self.fasten_var.get()
        if state == 0:
            seatbelt.unfasten_seatbelt()
        else:
            seatbelt.fasten_seatbelt()
        self.update_status()

    def update_people_inside(self):
        state = self.people_inside_var.get()
        seatbelt.set_people_inside(state)
        self.update_status()

    def update_engine_on(self):
        state = self.engine_on_var.get()
        seatbelt.set_engine_on(state)
        self.update_status()

    def update_speed(self, speed):
        seatbelt.set_vehicle_speed(float(speed))
        self.update_status()

    def check_status(self):
        status_message = (
            f"Seat Belt Fastened: {seatbelt.seatbelt_system.seatbelt_fastened}\n"
            f"Light Status: {seatbelt.seatbelt_system.light_color}\n"
            f"Sound Alarm: {seatbelt.seatbelt_system.sound_alarm}\n"
            f"People Inside: {seatbelt.seatbelt_system.people_inside}\n"
            f"Engine On: {seatbelt.seatbelt_system.engine_on}\n"
            f"Vehicle Speed: {seatbelt.seatbelt_system.vehicle_speed} km/hr"
        )
        messagebox.showinfo("Seat Belt Status", status_message)

    def update_status(self):
        light_color = seatbelt.seatbelt_system.light_color.capitalize()
        if light_color == "Green":
            self.stop_blinking()
            self.light_green_canvas.itemconfig(self.light_green, fill="green")
            self.light_yellow_canvas.itemconfig(self.light_yellow, fill="gray")
            self.light_red_canvas.itemconfig(self.light_red, fill="gray")
        elif light_color == "Yellow":
            self.stop_blinking()
            self.light_green_canvas.itemconfig(self.light_green, fill="gray")
            self.light_yellow_canvas.itemconfig(self.light_yellow, fill="yellow")
            self.light_red_canvas.itemconfig(self.light_red, fill="gray")
        elif light_color == "Red":
            self.light_green_canvas.itemconfig(self.light_green, fill="gray")
            self.light_yellow_canvas.itemconfig(self.light_yellow, fill="gray")
            self.start_blinking()
        else:
            self.stop_blinking()

        if seatbelt.is_sound_alarm_on():
            self.alarm_canvas.itemconfig(self.alarm_indicator, fill="red")
            pygame.mixer.Sound.play(self.alarm_sound)
        else:
            self.alarm_canvas.itemconfig(self.alarm_indicator, fill="black")
            pygame.mixer.Sound.stop(self.alarm_sound)

    def start_blinking(self):
        if not self.blinking:
            self.blinking = True
            self.blink_thread = threading.Thread(target=self.blink_red_light)
            self.blink_thread.start()

    def stop_blinking(self):
        self.blinking = False
        self.light_red_canvas.itemconfig(self.light_red, fill="white")

    def blink_red_light(self):
        while self.blinking:
            self.light_red_canvas.itemconfig(self.light_red, fill="red")
            time.sleep(0.5)
            self.light_red_canvas.itemconfig(self.light_red, fill="black")
            time.sleep(0.5)

if __name__ == "__main__":
    root = tk.Tk()
    app = SeatBeltGUI(root)
    root.mainloop()
