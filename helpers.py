from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_KEY = os.getenv("API_KEY")

def getloc(postcode):
    '''get location details from postcode'''
    postcode_url = f"http://api.postcodes.io/postcodes/{postcode}"
    data = requests.get(postcode_url).json()["result"]
    location = {
    'postcode': data['postcode'],
    'country': data['country'],
    'region': data['region'],
    'latitude': data['latitude'],
    'longitude': data['longitude'],
    'layer': ''.join(data['lsoa'].split(' ')[0:1])
    }

    
    print(API_KEY)


    return location

def getweather(lat, lon, unit):
    '''get weather details from API'''
    lat = round(int(lat))
    lon = round(int(lon))
    api_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily,alerts&units={unit}&appid={API_KEY}"
    weather = requests.get(api_url).json()
    print('yo')
    return weather