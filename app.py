from flask import Flask, redirect, render_template, request, url_for
from helpers import getcity, getloc, getpostcode, getweather, getall, getdrink, getword, getfact, getpubs
import requests
import csv

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weather", methods=['GET', 'POST'])
def weather():
    '''get postcode and check validity'''
    if request.method == "POST":
        postcode = request.form.get("postcode")
        if postcode == '':
            postcode = request.form.get("random-postcode")
        postcode_url = f"http://api.postcodes.io/postcodes/{postcode}"
        response = requests.get(postcode_url)
        
        # if postcode is valid, redirect
        if response.status_code == 200:
            return redirect(url_for("weatherd", postcode=postcode))
        elif response.status_code == 404:
            return redirect("/weather")
    # get rain status
    rain = getall()[1]
    random_postcode = getpostcode()
    return render_template("weather.html", rain=rain, random_postcode=random_postcode)



@app.route("/weatherd", methods=['GET', 'POST'])
def weatherd():
    '''get postcode from url and return location and weather data'''
    # turn postcode into location data
    if request.method == "GET":
        #TODO reject symbols
        #TODO exclude own city from raining list
        postcode = request.args.get("postcode")  
        location = getloc(postcode)

        # get weather data
        #weather = getweather(location['latitude'], location['longitude'])
        weather = {'dt': '15:43:42', 'sunrise': '05:09:10', 'sunset': '18:58:03', 'temp': 9.1, 'feels_like': 10.48, 'pressure': 1028, 'humidity': 83, 'dew_point': 8.36, 'uvi': 1.56, 'clouds': 11, 'visibility': 10000, 'wind_speed': 6.24, 'wind_deg': 58, 'wind_gust': 8.01, 'id': '801', 'main': 'Clouds', 'description': 'few clouds'}
        rain = False if int(weather['id']) > 700 else True
        city_tuple = getall(weather['temp'], rain)
        average_temp = city_tuple[0]
        cities = city_tuple[2]
        wet_cities_size = city_tuple[3]

        drink = getdrink()
        word = getword(rain)
        fact = getfact()
        pubs = getpubs(location['postcode'])
    return render_template("weatherd.html", location=location, weather=weather, average_temp=average_temp, rain=rain, cities=cities, wet_cities_size=wet_cities_size, drink=drink, word=word, fact=fact, pubs=pubs)



if __name__ == "__main__": 
    app.run()