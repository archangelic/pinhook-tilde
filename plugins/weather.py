import forecastio
from geopy.geocoders import Nominatim
import pinhook.plugin as p

geolocator = Nominatim()
deg = '°'

with open('key.txt') as k:
    api_key = k.read().strip()

@p.command('!weather', help_text='look up weather for a given area')
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
