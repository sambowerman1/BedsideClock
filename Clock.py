import os
import requests
from datetime import datetime
from workouts import workoutlist
import robin_stocks.robinhood as rh
from getpass import getpass
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd7in5_V2  # Adjust for your display

# Path to the pickle file
pickle_path = os.path.expanduser("~/.robinhood.pickle")

# Function to login to Robinhood
def login_robinhood():
    username = 'sam@bowerman.org'
    password = getpass("Enter Robinhood password: ")
    mfa_code = getpass("Enter MFA code (if applicable, else leave blank): ")
    try:
        if mfa_code:
            login = rh.login(username, password, mfa_code=mfa_code)
        else:
            login = rh.login(username, password)
        return login
    except Exception as e:
        print(f"Error during login: {e}")
        return None

# Try to delete the existing pickle file if it exists
if os.path.exists(pickle_path):
    try:
        os.remove(pickle_path)
        print("Deleted existing pickle file.")
    except Exception as e:
        print(f"Error deleting pickle file: {e}")

# Call the login function
login = login_robinhood()
if not login:
    print("Login failed. Exiting.")
    exit()

# Retrieve account information
try:
    account_info = rh.profiles.load_portfolio_profile()
    equity = account_info['equity']
    print("Current Buying Power: $", account_info['equity'])
except Exception as e:
    print(f"Error retrieving account info: {e}")
    exit()

# Initialize the ePaper display
epd = epd7in5_V2.EPD()
epd.init()
epd.Clear()

# Load fonts
font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 48)
font_medium = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)

def update_display():
    # Create a new image with white background
    image = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(image)
    
    # Add time
    current_time = datetime.now().strftime("%I:%M %p")
    draw.text((10, 10), current_time, font=font_large, fill=0)
    
    # Add date
    current_date = datetime.now().strftime("%m-%d-%Y")
    draw.text((10, 70), f"Date: {current_date}", font=font_medium, fill=0)
    
    # Add equity
    try:
        account_info = rh.profiles.load_portfolio_profile()
        equity = account_info['equity']
        draw.text((10, 100), f"Equity: ${equity}", font=font_medium, fill=0)
    except Exception as e:
        draw.text((10, 100), "Equity: Error", font=font_medium, fill=0)
        print(f"Error retrieving equity info: {e}")
    
    # Add temperature
    try:
        api_key = "f02c0176f2d7633e788328570828db4e"
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=St. Louis,us&appid={api_key}")
        weather_data = response.json()
        current_temp = weather_data['main']['temp']
        current_temp_f = round((current_temp - 273.15) * 9/5 + 32)
        draw.text((10, 130), f"Temperature: {current_temp_f}°F", font=font_medium, fill=0)
    except Exception as e:
        draw.text((10, 130), "Temperature: Error", font=font_medium, fill=0)
        print(f"Error retrieving temperature info: {e}")
    
    # Add workout
    workout_info = "Rest Day"
    try:
        for i in range(len(workoutlist)):
            if workoutlist[i][0] == datetime.now().strftime("%m-%d-%Y"):
                workout_info = workoutlist[i][1]
                break
        draw.text((10, 160), f"Today's Workout: {workout_info}", font=font_medium, fill=0)
    except Exception as e:
        draw.text((10, 160), "Workout: Error", font=font_medium, fill=0)
        print(f"Error retrieving workout info: {e}")
    
    # Display the image
    epd.display(epd.getbuffer(image))

    # Schedule the next update
    epd.sleep()
    update_display()

# Initial update
update_display()
