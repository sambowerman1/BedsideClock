import tkinter as tk
import requests
from datetime import datetime
from datetime import timedelta
# If using a sensor:
# import Adafruit_DHT

# Setup the main window
root = tk.Tk()
root.title("Smart Clock")

# Add the time display
time_label = tk.Label(root, font=('Helvetica', 48))
time_label.pack()

# Add the temperature display
temp_label = tk.Label(root, font=('Helvetica', 24))
temp_label.pack()

# Add the workout display
workout_label = tk.Label(root, font=('Helvetica', 24))
workout_label.pack()


date_label = tk.Label(root, font=('Helvetica', 24))
date_label.pack()

def update_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    time_label.config(text=current_time)
    root.after(1000, update_time)  # update time every second

def update_temp():
    # Fetch the temperature from an API or sensor
    # For example, using OpenWeatherMap API:
    # response = requests.get('API_URL').json()
    # temperature = response['main']['temp']
    # Or using a sensor:
    # humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    temperature = "76°F"  # Placeholder value
    temp_label.config(text=temperature)
    root.after(180000, update_temp)  # update temperature every minute


def update_date():
    current_date = datetime.now().strftime("%m-%d-%Y")  # format as you prefer
    date_label.config(text=current_date)
    root.after(600000, update_date) # update date every 10 minutes
    


def update_workout():
    
    # for workout in workouts:
    #     if workout[0] == datetime.now().strftime("%Y-%m-%d"):
    #         workout_info = workout[1]
    #     else:
    #         workout_info = "Rest Day"

    workout_info = "Rest Day"  # Placeholder value
    
    workout_label.config(text=f"Today's Workout: {workout_info}")
    root.after(600000, update_workout)  # update workout every minute



# Initialize all the labels
update_time()

update_date()
update_temp()
update_workout()

root.mainloop()
