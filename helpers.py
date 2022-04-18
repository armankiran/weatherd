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


def getweather(lat, lon):
    '''get weather details from API'''
    lat = round(int(lat))
    lon = round(int(lon))
    api_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&units=metric&appid={API_KEY}"
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
        'main': response['current']['weather'][0]['id'],
        'main': response['current']['weather'][0]['main'],
        'description': response['current']['weather'][0]['description'],
        'daily_temp': response['daily'][0]['temp']['day'],
        'daily_id': response['daily'][0]['weather'][0]['id'],
        'daily_main': response['daily'][0]['weather'][0]['main']
    }
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
  file = open('totaldb.csv', 'r+', newline='')
  reader = csv.reader(file)
  total_list = list(reader)
  # check the file and update by turn citydb to nested lists by turning into dict 
  # if file isn't up-to-date
  date = datetime.now().date()
  if total_list[0][4] != str(date):
    # iterating through it and adding cities to the city list
    city_dict = getcitylist('citydb1.csv')
    city_list = []
    for key, value in city_dict.items():
      # get city lat lon
      city = getcity(key, value)
      # round lat and lon for weather data
      weather = getweather(round(int(city['lat'])), round(int(city['lon'])))
      # list to be added every iteration
      prop_list = []
      prop_list.append(key)
      prop_list.append(value)
      prop_list.append(round(int(weather['daily_temp'])))
      prop_list.append(weather['daily_id'])
      prop_list.append(str(date))
      city_list.append(prop_list) 
    file.close()
    # open file in a mode to truncate as can't modify while file is in 'with open' state
    tfile = open('totaldb.csv', 'a', newline='')
    tfile.truncate(0)
    # write city list to csv file
    writer = csv.writer(tfile)
    writer.writerows(city_list)
    tfile.close()

  # get average weather and rain ino
  file = open('totaldb.csv', 'r', newline='')
  reader = csv.reader(file)
  average_list = list(reader)
  average_temp = 0
  rain_status = False
  for i in average_list:
    average_temp += int(i[2])
    if int(i[3]) < 700:
      rain_status = True
  return (average_temp, rain_status)
  
print(getall()[0])

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

