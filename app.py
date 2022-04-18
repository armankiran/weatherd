from flask import Flask, redirect, render_template, request, url_for
from helpers import getcity, getloc, getpostcode, getweather, getall, getdrink, getword
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
            return redirect("/")
    # get rain status
    rain = getall()[1]
    random_postcode = getpostcode()
    location = getloc(random_postcode)
    print(location)
    return render_template("weather.html", rain=rain, random_postcode=random_postcode)

@app.route("/weatherd", methods=['GET', 'POST'])
def weatherd():
    '''get postcode from url and return location and weather data'''
    # turn postcode into location data
    if request.method == "GET":
        #TODO reject symbols
        postcode = request.args.get("postcode")
        location = getloc(postcode)

        # get weather data
        #weather = getweather(location['latitude'], location['longitude'])
        weather = {'dt': '15:43:42', 'sunrise': '05:09:10', 'sunset': '18:58:03', 'temp': 9.1, 'feels_like': 10.48, 'pressure': 1028, 'humidity': 83, 'dew_point': 8.36, 'uvi': 1.56, 'clouds': 11, 'visibility': 10000, 'wind_speed': 6.24, 'wind_deg': 58, 'wind_gust': 8.01, 'id': '501', 'main': 'Clouds', 'description': 'few clouds'}
        rain = False if int(weather['id']) > 700 else True
        average_temp = getall()[0] 
        random_cities = getall(weather['temp'])[2]
        print(random_cities)
        drink = getdrink()
        word = getword()
    return render_template("weatherd.html", location=location, weather=weather, average_temp=average_temp, postcode=postcode, rain=rain, random_cities=random_cities, drink=drink, word=word)






if __name__ == "__main__": 
    app.run()