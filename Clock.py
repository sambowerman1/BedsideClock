import time
import requests
from datetime import datetime


from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory

Device.pin_factory = PiGPIOFactory()

from waveshare_epd import epd7in5
import gpiozero
import atexit


from waveshare_epd import epd7in5
from PIL import Image, ImageDraw, ImageFont
import robin_stocks as rh

# Robinhood login
username = 'sam@bowerman.org'
password = 'e'
rh.robinhood.authentication.login(username, password)

# Set up the ePaper display
epd = epd7in5.EPD()
epd.init()

# Create a blank image for drawing.
width, height = epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT
image = Image.new('1', (width, height), 255)  # 255: clear the frame
draw = ImageDraw.Draw(image)

# Load a font
font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 48)
font_medium = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)

# Define update functions
def update_time(draw):
    current_time = datetime.now().strftime("%I:%M %p")
    draw.text((10, 10), current_time, font=font_large, fill=0)
    epd.display(epd.getbuffer(image))
    epd.sleep()
    
def update_equity(draw):
    account_info = rh.robinhood.profiles.load_portfolio_profile()
    equity = account_info['equity']
    draw.text((10, 70), f"Equity: ${equity}", font=font_medium, fill=0)
    epd.display(epd.getbuffer(image))
    epd.sleep()

def update_temp(draw):
    api_key = "f02c0176f2d7633e788328570828db4e"
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=St. Louis,us&appid={api_key}")
    weather_data = response.json()
    current_temp = weather_data['main']['temp']
    current_temp_f = round((current_temp - 273.15) * 9/5 + 32)
    draw.text((10, 130), f"Temperature: {current_temp_f}°F", font=font_medium, fill=0)
    epd.display(epd.getbuffer(image))
    epd.sleep()

def update_date(draw):
    current_date = datetime.now().strftime("%m-%d-%Y")
    draw.text((10, 190), current_date, font=font_medium, fill=0)
    epd.display(epd.getbuffer(image))
    epd.sleep()

def update_workout(draw):
    for i in range(len(workoutlist)):
        if workoutlist[i][0] == datetime.now().strftime("%m-%d-%Y"):
            workout_info = workoutlist[i][1]
            break
    else:
        workout_info = "Rest Day"
    draw.text((10, 250), f"Today's Workout: {workout_info}", font=font_medium, fill=0)
    epd.display(epd.getbuffer(image))
    epd.sleep()

# Update the display
def main():
    while True:
        image = Image.new('1', (width, height), 255)
        draw = ImageDraw.Draw(image)
        
        update_time(draw)
        update_equity(draw)
        update_temp(draw)
        update_date(draw)
        update_workout(draw)
        
        time.sleep(600)  # Update every 10 minutes

if __name__ == "__main__":
    main()
