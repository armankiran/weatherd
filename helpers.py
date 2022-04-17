from dotenv import load_dotenv
import os
import requests
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("API_KEY")

def getloc(postcode):
    '''get location details from postcode'''
    #TODO reject incorrect postcodes
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

    return location

def getcity(city, country):
  '''get city lat and lon by name'''
  api_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&appid={API_KEY}"
  response = requests.get(api_url).json()[0]
  city = {
    'name': response['name'],
    'lat': response['lat'],
    'lon': response['lon']
  }

  return city


def getweather(lat, lon, unit):
    '''get weather details from API'''
    lat = round(int(lat))
    lon = round(int(lon))
    api_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily,alerts&units={unit}&appid={API_KEY}"
    response = requests.get(api_url).json()
    weather = {
        'dt': datetime.utcfromtimestamp(response['current']['dt']).strftime('%H:%M:%S'),
        'sunrise': datetime.utcfromtimestamp(response['current']['sunrise']).strftime('%H:%M:%S'),
        'sunset': datetime.utcfromtimestamp(response['current']['sunset']).strftime('%H:%M:%S'),
        'temp': response['current']['temp'],
        'feels_like': response['current']['feels_like'],
        'pressure': response['current']['pressure'],
        'humidity': response['current']['humidity'],
        'dew_point': response['current']['dew_point'],
        'uvi': response['current']['uvi'],
        'clouds': response['current']['clouds'],
        'visibility': response['current']['visibility'],
        'wind_speed': response['current']['wind_speed'],
        'wind_deg': response['current']['wind_deg'],
        'wind_gust': response['current']['wind_gust'],
        'main': response['current']['weather'][0]['id'],
        'main': response['current']['weather'][0]['main'],
        'description': response['current']['weather'][0]['description']
    }
    return weather


def getword():
    '''get the word meaning from dict api'''
    api_url = "https://api.dictionaryapi.dev/api/v2/entries/en/severe"
  # itireate through list, find adjective, itr through definitions, create dict
    try:
        response = requests.get(api_url).json()[0]
        for i in range(len(response['meanings'])):
            if response['meanings'][i]['partOfSpeech'] == 'adjective':
                meaning = {
                    'word': response['word'],
                    'definitions': response['meanings'][i]['definitions']
                }
    # remove synonyms and antonyms
        for i in range(len(meaning['definitions'])):
          meaning['definitions'][i].pop('synonyms', None)
          meaning['definitions'][i].pop('antonyms', None)
        return meaning
    # return error if word doesn't exist
    except:
        return "Can't find the word"

