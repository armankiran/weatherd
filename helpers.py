from dotenv import load_dotenv
from datetime import datetime
import os
import requests
import csv
import random

load_dotenv()
API_KEY = os.getenv("API_KEY")
DATE = os.getenv("DATE")

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
    api_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&units={unit}&appid={API_KEY}"
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
        'description': response['current']['weather'][0]['description'],
        'daily_temp': response['daily'][0]['temp']['day'],
        'daily_id': response['daily'][0]['weather'][0]['id'],
        'daily_main': response['daily'][0]['weather'][0]['main']
    }
    print(weather)
    return weather


def getcitylist(city_list):
  '''get city list from db and return dict with maximum len of 59 cities to the api limitations'''
  with open(city_list, newline='') as cities:
    reader = csv.reader(cities)
    next(reader)
    results = dict(reader)
    # remove random cities if list size 
    if len(results) > 58:
      for i in range(len(results) - 58):
        results.pop(random.choice(list(results.keys())))

    # get weather data for cities
  return results


def getall():
  '''get overall data from cities with '''
  with open('totaldb.csv', 'r+', newline='') as total:
    reader = csv.reader(total)
    total_list = list(reader)
    date = datetime.now().date()
    if total_list[1][4] != date:
      total_list[1][4] = date
      #TODO copy city data to totaldb csv
      # turn citydb to nested lists
      city_dict = getcitylist('citydb.csv')
      city_list = []
      # for key, value in city_dict.items():
      #   prop_list = []
      #   prop_list.append(key)
      #   prop_list.append(value)
      #   city_list.append(prop_list
      print(city_list)
      total.truncate(0)
      writer = csv.writer(total)
      writer.writerows(total_list)
  



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

