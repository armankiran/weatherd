from flask import Flask, redirect, render_template, request, url_for
from helpers import getloc, getweather
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
        postcode = request.args.get("postcode")
        location = getloc(postcode)

        # get weather data
        #TODO get unit
        #weather = getweather(location['latitude'], location['longitude'], 'metric')
    return render_template("weatherd.html", location=location, weather=weather)






if __name__ == "__main__": 
    app.run()