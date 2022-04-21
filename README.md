# weathered
Get weather and area data based in your postcode in UK!

This my final project for [Harvard CS50x](https://cs50.harvard.edu/x/2022/project/) - a Flask weather application with some tweaks works solely on UK postcodes. Now you can check if it always rain in UK!
## Files
* [main](https://github.com/armankiran/weatherd/blob/main/README.md##main)
	* [app.py](##https://github.com/armankiran/weatherd/blob/main/README.md##app.py)
	* [helpers.py](##https://github.com/armankiran/weatherd/blob/main/README.md##helpers.py)
*  databases
	* citydb.csv
	* totaldb.csv
	* pubs.db
	* sunnywords.csv
	* rainywords.csv
* templates
	* layout.html
	* weather.html
	* weatherd.html
* static
	* styles.css

## APIs
* doogal.co.uk
to get random postcodes and postcodes in a certain area

* postcodes.io
to get UK postcode details such as longitude and latitude

* [dictionaryapi.dev](dictionaryapi.dev)
to get word definitions
* [thecocktaildb.com](thecocktaildb.com/api.php)
to get random coctail recipes
* uselessfacts.jsph.pl
to get random useless fact
* openweathermap.org
to get weather data

## main
## app.py
Main file of the Flask application. 

**def weather()** renders the weather.html page. 
Requests postcode from form input. Value of the input is set random with doogal.co.uk API call for random search.
Also rain status returned by [getall()](###getall) function. 

**def weatherd()** renders the weatherd.html page based on the postcode returned by **def weather()**. Location details are returned by [getloc()](https://github.com/armankiran/weatherd/blob/main/README.md###getloc()) and passed into the [getweather()](https://github.com/armankiran/weatherd/blob/main/README.md###getweather()) for the weather info. 

 Temperature and rain status is used in [getall()](https://github.com/armankiran/weatherd/blob/main/README.md###getall()) function to get a tuple of values gathered from [totaldb.csv](https://github.com/armankiran/weatherd/blob/main/README.md##databases) 
 
Then [getdrink()](https://github.com/armankiran/weatherd/blob/main/README.md###getdrink()), [getword()](https://github.com/armankiran/weatherd/blob/main/README.md###getword()), [getfact()](https://github.com/armankiran/weatherd/blob/main/README.md###getfact()), [getpubs()](https://github.com/armankiran/weatherd/blob/main/README.md###getpubs()) functions are called respectively.


##  helpers.py
Helper functions
### getpostcode()
Gets a random postcode from doogal.co.uk
### getloc()
Passes 'postcode' value to postcodes.io to return location data such as 'latitude' and 'longitude' to be used in .  I wasn't able to receve a reliable city name from postcodes.io to pass [Open Weather API](https://openweathermap.org/api) therefore had to use [OpenWeather Geocoding API](https://openweathermap.org/api/geocoding-api).

### getcity()
Returns city information. Added this functing as [getpostcode()](https://github.com/armankiran/weatherd/blob/main/README.md###getpostcode()) was returning countries in UK individually and was messing with other functions requiring them as GB.

### getweather()
Get weather data through [Open Weather API](https://openweathermap.org/api) call.

### getcitylist()
Returns a list of cities to be used in [totaldb.csv](https://github.com/armankiran/weatherd/blob/main/README.md##databases). [Open Weather API](https://openweathermap.org/api) has a limit of 60 calls per minute, therefore list is maxed at 58 entries. 
[citiesdb.csv](https://github.com/armankiran/weatherd/blob/main/README.md##databases) can be modified to include other cities in the app but the app will start removing random entries if the list size is over 58.

### getall()
Returns overall data from [totaldb.csv](https://github.com/armankiran/weatherd/blob/main/README.md##databases) to be used for average temperatureof the cities, rain status, and dry-wet cities from the [citiesdb.csv](https://github.com/armankiran/weatherd/blob/main/README.md##databases)  provided. 

Due to [Open Weather API](https://openweathermap.org/api) call limitations per month, function checks the date in the database and if it doesn't match, updated the database. Therefore the list is only updated in the first access to the webpage per day.

Even though first API call is slower than I expected, all the other city weather data requests are considerably faster as data is stored once only accessed through CSV module.

Rest of the function divies cities to wet and dry based on if they received/are going to receive rain during the day. Again 'daily' design choice made based on API limitations.

Lastly, function will return a list of randomly selected 5 cities based on if it is raining in the input location or not. The list is limited at 5 as it fits with the layout of the page.

### getword()
Passes a random word from [sunnywords.csv](databases) or [rainywords.csv](https://github.com/armankiran/weatherd/blob/main/README.md##databases) files based on if it is raining or not in input location and returns definitions for that word. Only adjective definitions are returned.

### getdrink()
Returns a random alcoholic drink from [thecocktaildb.com](thecocktaildb.com/api.php). Ingredient values are added to returned dictionary by iterating through the response rather than direct copy. as it is easier to loop over in Jinja instead of checking for None values in [weatherd.html](https://github.com/armankiran/weatherd/blob/main/README.md###weatherd.html).

### getfact()
Returns a random fact from uselessfacts.jsph.pl

### getpub()
Gets postcodes around 500 meters of input from doogal.co.uk then checks [pubs.db](https://github.com/armankiran/weatherd/blob/main/README.md##databases) SQL file to return a list of pubs around.
[pubs.db](https://github.com/armankiran/weatherd/blob/main/README.md##databases) data is gathered by [getthedata.com](https://www.getthedata.com/open-pubs).

500 metresseemed to be optimal amount as in most locations, over that returned an overpopulated list. In places where there wasn't a pub in 500 metres radius, also didn't include many in 1 kilometres and 2 kilometres respectively.

## databases
### citydb.csv
-   totaldb.csv
includes city name, country code, daily temperature, weather code, date updated
-   pubs.db
UK pub names and locations
-   sunnywords.csv
words for to be used if it's not raining in location
-   rainywords.csv
words for to be used if it's raining in location

## templates
-   layout.html
-   weather.html
-   weatherd.html
