from flask import Flask, redirect, render_template, request, url_for
from helpers import getloc, getweather, getword
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weather", methods=['GET', 'POST'])
def weather():
    # 

    '''get postcode and check validity'''
    if request.method == "POST":
        postcode = request.form.get("postcode")
        postcode_url = f"http://api.postcodes.io/postcodes/{postcode}"
        response = requests.get(postcode_url)
        
        # if postcode is valid, redirect
        if response.status_code == 200:
            return redirect(url_for("weatherd", postcode=postcode))
        elif response.status_code == 404:
            return redirect("/")

    return render_template("weather.html")

@app.route("/weatherd", methods=['GET', 'POST'])
def weatherd():
    '''get postcode from url and return location and weather data'''
    # turn postcode into location data
    if request.method == "GET":
        #TODO reject symbols
        postcode = request.args.get("postcode")
        location = getloc(postcode)

        # get weather data
        #TODO get unit
        #weather = getweather(location['latitude'], location['longitude'], 'metric')
        weather = {'dt': '15:43:42', 'sunrise': '05:09:10', 'sunset': '18:58:03', 'temp': 11.14, 'feels_like': 10.48, 'pressure': 1028, 'humidity': 83, 'dew_point': 8.36, 'uvi': 1.56, 'clouds': 11, 'visibility': 10000, 'wind_speed': 6.24, 'wind_deg': 58, 'wind_gust': 8.01, 'main': 'Clouds', 'description': 'few clouds'}
        word = getword()
    return render_template("weatherd.html", location=location, weather=weather, word=word)






if __name__ == "__main__": 
    app.run()