import forecastio
from geopy.geocoders import Nominatim
import pinhook.plugin as p
import requests
import toml

geolocator = Nominatim(user_agent='pinhook')
deg = '°'

keys = toml.load('secrets.toml')
# weather_key = keys['darksky']['key']
aqi_key = keys['airvisual']['key']

# @p.command('!weather', help_text='look up weather for a given area')
def weather(msg):
    location = geolocator.geocode(msg.arg)
    msg.logger.info('{}, {}'.format(location.latitude, location.longitude))
    forecast = forecastio.load_forecast(api_key, location.latitude, location.longitude, units='us')
    forecast = forecast.currently()
    tempf = int(forecast.temperature)
    tempc = int((tempf - 32) * (5/9))
    return p.message('Weather for: {}\n{}{}f/{}{}c {}'.format(location.raw['display_name'], tempf, deg, tempc, deg, forecast.summary))

@p.command('!whereis', help_text='debugging tool to find out where a given string is thought to be')
def whereis(msg):
    location = geolocator.geocode(msg.arg)
    msg.logger.info(location.raw)
    return p.message('{}, {}'.format(location.latitude, location.longitude))

@p.command('!aqi')
def aqi(msg):
    location = geolocator.geocode(msg.arg)
    payload = {'key': aqi_key, 'lat': location.latitude, 'lon': location.longitude}
    r = requests.get('http://api.airvisual.com/v2/nearest_city', params=payload).json()['data']
    city = r['city']
    state = r['state']
    country = r['country']
    quality = int(r['current']['pollution']['aqius'])
    if quality <= 50:
        concern = 'Good'
    elif quality <= 100:
        concern = 'Moderate'
    elif quality <= 150:
        concern = 'Unhealthy for Sensitive Groups'
    elif quality <= 200:
        concern = 'Unhealthy'
    elif quality <= 300:
        concern = 'Very Unhealthy'
    elif quality >= 301:
        concern = 'Hazardous'
    return p.message('AQI for {}, {}, {} is {} - {}'.format(city, state, country, quality, concern))
