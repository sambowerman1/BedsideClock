import sys
import os
import time
import requests
from datetime import datetime
from waveshare_epd import epd7in5_V2
from PIL import Image, ImageDraw, ImageFont
import robin_stocks.robinhood as rh
import logging
from workouts import workoutlist

# Setup paths
base_dir = os.path.dirname(os.path.realpath(__file__))
picdir = os.path.join(base_dir, 'pic')
libdir = os.path.join(base_dir, 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

logging.basicConfig(level=logging.DEBUG)

# Robinhood login
username = 'sam@bowerman.org'
password = 'e'
rh.login(username, password)

# Function to update display
def update_display(epd):
    try:
        logging.info("init and Clear")
        epd.init()
        epd.Clear()

        # Create a blank image for drawing
        width, height = epd7in5_V2.EPD_HEIGHT, epd7in5_V2.EPD_WIDTH
        image = Image.new('1', (width, height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(image)

        # Load fonts
        font_path = os.path.join(picdir, 'Font.ttc')
        if not os.path.exists(font_path):
            logging.error(f"Font file not found: {font_path}")
            font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 48)
            font_medium = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
            font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
        else:
            font_large = ImageFont.truetype(font_path, 48)
            font_medium = ImageFont.truetype(font_path, 24)
            font_small = ImageFont.truetype(font_path, 20)

        # Update time
        current_time = datetime.now().strftime("%I:%M %p")
        logging.info(f"Updating time: {current_time}")
        draw.text((10, 10), current_time, font=font_large, fill=0)

        # Update equity
        try:
            account_info = rh.profiles.load_portfolio_profile()
            equity = account_info['equity']
            logging.info(f"Updating equity: {equity}")
            draw.text((10, 70), f"Equity: ${equity}", font=font_medium, fill=0)
        except Exception as e:
            logging.error(f"Error fetching equity: {e}")

        # Update temperature
        try:
            api_key = "f02c0176f2d7633e788328570828db4e"
            response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=St. Louis,us&appid={api_key}", timeout=10)
            weather_data = response.json()
            current_temp = weather_data['main']['temp']
            current_temp_f = round((current_temp - 273.15) * 9/5 + 32)
            logging.info(f"Updating temperature: {current_temp_f}°F")
            draw.text((10, 130), f"Temperature: {current_temp_f}°F", font=font_medium, fill=0)
        except Exception as e:
            logging.error(f"Error fetching temperature: {e}")

        # Update date
        current_date = datetime.now().strftime("%m-%d-%Y")
        logging.info(f"Updating date: {current_date}")
        draw.text((10, 190), current_date, font=font_medium, fill=0)

        # Update workout
        workout_info = "Rest Day"
        for workout in workoutlist:
            if workout[0] == datetime.now().strftime("%m-%d-%Y"):
                workout_info = workout[1]
                break
        logging.info(f"Updating workout: {workout_info}")
        draw.text((10, 250), f"Today's Workout: {workout_info}", font=font_medium, fill=0)

        # Display the image
        epd.display(epd.getbuffer(image))

    except IOError as e:
        logging.error(f"IOError: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        epd.sleep()

# Main loop
def main():
    epd = epd7in5_V2.EPD()
    while True:
        update_display(epd)
        time.sleep(30)  # Update every 10 minutes

if __name__ == "__main__":
    main()
