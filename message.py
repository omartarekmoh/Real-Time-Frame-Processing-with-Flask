from twilio.rest import Client
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Function to generate Google Maps URL
def generate_maps_url(latitude, longitude):
    return f"https://www.google.com/maps?q={latitude},{longitude}"

# Function to get current location using ipinfo.io for accuracy
def get_current_location():
    response = requests.get('https://ipinfo.io/json')
    data = response.json()
    # Extract latitude and longitude from ipinfo.io response
    location = data.get('loc').split(',')
    latitude = 31.0470343
    longitude = 31.3538818
    return latitude, longitude

# Function to send SMS using Twilio
def send_sms(destination_phone_number, message_body):
    # Twilio credentials
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_phone_number = os.getenv('TWILIO_AUTH_NUMBER')

    # Create an instance of the Twilio client
    client = Client(account_sid, auth_token)

    # Send the SMS
    message = client.messages.create(
        body=message_body,
        from_=twilio_phone_number,
        to=destination_phone_number
    )

    print(f"Message sent with SID: {message.sid}")

# Function to integrate all steps
def send_location_sms(destination_phone_number):
    # Get current location
    latitude, longitude = get_current_location()

    # Generate Google Maps URL
    maps_url = generate_maps_url(latitude, longitude)

    # Create message body
    message_body = f"Fire Detected, Current Location: {maps_url}"

    # Send SMS
    send_sms(destination_phone_number, message_body)

