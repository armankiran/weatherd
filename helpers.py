from dotenv import load_dotenv
from datetime import datetime
import os
import requests
import csv
import random

load_dotenv()
API_KEY = os.getenv("API_KEY")
DATE = os.getenv("DATE")

def getpostcode():
  '''get random postcode for default value'''
  random_postcode_url = requests.get('https://www.doogal.co.uk/CreateRandomPostcode.ashx?output=csv&count=1')
  lines = random_postcode_url.text.splitlines()
  reader = csv.reader(lines)
  random_postcode = list(reader)[0][0]
  return random_postcode

def getloc(postcode):
    '''get location details from postcode'''
    #TODO reject incorrect postcodes
    # get lat and lon, include country as openweather refers all UK as GB
    postcode_url = f"http://api.postcodes.io/postcodes/{postcode}"
    data = requests.get(postcode_url).json()["result"]
    location = {
    'postcode': data['postcode'],
    'city': '',
    'country': data['country'],
    'region': data['region'],
    'latitude': data['latitude'],
    'longitude': data['longitude']
    }
    # get city name as postcode api isn't reliable
    city_url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={location['latitude']}&lon={location['longitude']}&limit=1&appid={API_KEY}"
    location['city'] = requests.get(city_url).json()[0]['name']

    return location

def getcity(city, country):
  '''get city lat and lon by name'''
  api_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&appid={API_KEY}"
  response = requests.get(api_url).json()[0]
  city = {
    'name': response['name'],
    'lat': response['lat'],
    'lon': response['lon'],
    'country': response['country']
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
        'id': response['current']['weather'][0]['id'],
        'main': response['current']['weather'][0]['main'],
        'description': response['current']['weather'][0]['description'],
        'daily_temp': response['daily'][0]['temp']['day'],
        'daily_id': response['daily'][0]['weather'][0]['id'],
        'daily_main': response['daily'][0]['weather'][0]['main']
    }
    print('apicall')
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


def getall(temp=10):
  '''get overall data from cities with selected'''
  file = open('totaldb.csv', 'r+', newline='')
  reader = csv.reader(file)
  total_list = list(reader)
  # check the file and update by turn citydb to nested lists by turning into dict 
  # if file isn't up-to-date
  date = datetime.now().date()
  if total_list[0][4] != str(date):
    # iterating through it and adding cities to the city list
    city_dict = getcitylist('citydb.csv')
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
      print('api call') 
    file.close()
    # open file in a mode to truncate as can't modify while file is in 'with open' state
    tfile = open('totaldb.csv', 'a', newline='')
    tfile.truncate(0)
    # write city list to csv file
    writer = csv.writer(tfile)
    writer.writerows(city_list)
    tfile.close()

  # get average weather and rain status
  file = open('totaldb.csv', 'r', newline='')
  reader = csv.reader(file)
  average_list = list(reader)
  average_temp = 0
  rain_status = False
  # collect temp average and record rain status
  for i in average_list:
    average_temp += int(i[2])
    if int(i[3]) < 700:
      rain_status = True
  # get list of randomly selected cities hotter than current city
  city_rain_list = []
  
  for city in average_list:
    # if int(city[2]) > int(temp):
    if int(city[3]) > 700:
      city_rain_list.append(city)
  #random_cities = []
  #random_cities = random.sample(city_rain_list, 5)
  return (average_temp / len(average_list), rain_status, city_rain_list)


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

def getrandomcity():
  '''get a dict of random cities for comparasion by reading database'''

def getdrink():
  '''get a random drink from api'''
  response = requests.get("http://www.thecocktaildb.com/api/json/v1/1/random.php?a=Alcoholic").json()['drinks'][0]
  drink = {
    'name': response['strDrink'],
    'category': response['strCategory'],
    'glass': response['strGlass'],
    'instructions': response['strInstructions'],
    'thumb': response['strDrinkThumb'],
    'ingredients': {}
  }
  i = 1
  while response[f'strIngredient{i}'] != None:
    ing = response[f'strIngredient{i}']
    mes = response[f'strMeasure{i}']
    drink['ingredients'][ing] = mes
    i+= 1
  return drink

  