import time
import requests
import logging
from datetime import datetime, timedelta
from waveshare_epd import epd7in5_V2
from PIL import Image, ImageDraw, ImageFont
from workouts import workoutlist
# import robin_stocks.robinhood as rh

# Configure logging
logging.basicConfig(filename='epaper_display.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Robinhood login
# username = 'sam@bowerman.org'
# password = 'e'
# rh.login(username, password)

# Set up the ePaper display
epd = epd7in5_V2.EPD()
epd.init()

# Create a blank image for drawing
width, height = epd7in5_V2.EPD_HEIGHT, epd7in5_V2.EPD_WIDTH
image = Image.new('1', (width, height), 255)  # 255: clear the frame
draw = ImageDraw.Draw(image)

# Load fonts
font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 48)
font_medium = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)

# Define update functions
def update_time(draw):
    current_time = datetime.now().strftime("%I:%M %p")
    draw.text((10, 10), current_time, font=font_large, fill=0)

# def update_equity(draw):
#     account_info = rh.profiles.load_portfolio_profile()
#     equity = account_info['equity']
#     draw.text((10, 70), f"Equity: ${equity}", font=font_medium, fill=0)

def update_temp(draw):
    api_key = "f02c0176f2d7633e788328570828db4e"
    try:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=Chicago,us&appid={api_key}")
        response.raise_for_status()  # Raise an error for bad responses
        weather_data = response.json()
        current_temp = weather_data['main']['temp']
        current_temp_f = round((current_temp - 273.15) * 9/5 + 32)
        draw.text((10, 130), f"Temperature: {current_temp_f}°F", font=font_medium, fill=0)
    except requests.RequestException as e:
        logging.error(f"Failed to fetch weather data: {e}")
        draw.text((10, 130), "Temperature: Error", font=font_medium, fill=0)

def update_date(draw):
    current_date = datetime.now().strftime("%m-%d-%Y")
    draw.text((10, 190), current_date, font=font_medium, fill=0)

def update_workout(draw):
    try:
        for i in range(len(workoutlist)):
            if workoutlist[i][0] == datetime.now().strftime("%m-%d-%Y"):
                workout_info = workoutlist[i][1]
                break
        else:
            workout_info = "Rest Day"
        draw.text((10, 250), f"Today's Workout: {workout_info}", font=font_medium, fill=0)
    except Exception as e:
        logging.error(f"Failed to update workout info: {e}")
        draw.text((10, 250), "Today's Workout: Error", font=font_medium, fill=0)

# Update the display
def main():
    last_temp_update = datetime.min
    
    while True:
        try:
            image = Image.new('1', (width, height), 255)
            draw = ImageDraw.Draw(image)
            
            update_time(draw)
            update_date(draw)
            update_workout(draw)
            
            current_time = datetime.now()
            if current_time - last_temp_update >= timedelta(hours=1):
                update_temp(draw)
                last_temp_update = current_time
            
            epd.display(epd.getbuffer(image))
            epd.sleep()
            
            logging.info("Display updated successfully")
        except Exception as e:
            logging.error(f"Failed to update display: {e}")
        
        time.sleep(30)  # Update every 30 seconds

if __name__ == "__main__":
    main()
