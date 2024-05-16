import requests
from datetime import datetime
from datetime import timedelta
from workouts import workoutlist
import robin_stocks as rh
import getpass
from IT8951.display import AutoEPDDisplay
from PIL import Image, ImageDraw, ImageFont

# Replace these with your Robinhood login credentials
username = 'sam@bowerman.org'
password = 'hidden'
rh.robinhood.authentication.login(username, password)

account_info = rh.robinhood.profiles.load_portfolio_profile()
equity = account_info['equity']
print("Current Buying Power: $", account_info['equity'])

# Initialize the ePaper display
display = AutoEPDDisplay(vcom=-1.52)  # Adjust vcom value as needed
display.clear()

# Load fonts
font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 48)
font_medium = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)

def update_display():
    # Create a new image with white background
    image = Image.new('1', display.dimensions, 255)
    draw = ImageDraw.Draw(image)
    
    # Add time
    current_time = datetime.now().strftime("%I:%M %p")
    draw.text((10, 10), current_time, font=font_large, fill=0)
    
    # Add date
    current_date = datetime.now().strftime("%m-%d-%Y")
    draw.text((10, 70), f"Date: {current_date}", font=font_medium, fill=0)
    
    # Add equity
    account_info = rh.robinhood.profiles.load_portfolio_profile()
    equity = account_info['equity']
    draw.text((10, 100), f"Equity: ${equity}", font=font_medium, fill=0)
    
    # Add temperature
    api_key = "f02c0176f2d7633e788328570828db4e"
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=St. Louis,us&appid={api_key}")
    weather_data = response.json()
    current_temp = weather_data['main']['temp']
    current_temp_f = round((current_temp - 273.15) * 9/5 + 32)
    draw.text((10, 130), f"Temperature: {current_temp_f}°F", font=font_medium, fill=0)
    
    # Add workout
    workout_info = "Rest Day"
    for i in range(len(workoutlist)):
        if workoutlist[i][0] == datetime.now().strftime("%m-%d-%Y"):
            workout_info = workoutlist[i][1]
            break
    draw.text((10, 160), f"Today's Workout: {workout_info}", font=font_medium, fill=0)
    
    # Display the image
    display.show_image(image)

    # Schedule the next update
    display.epd.wait_for_busy(timeout=60)
    update_display()

# Initial update
update_display()
