from bs4 import BeautifulSoup
import pinhook.plugin
import requests

@pinhook.plugin.register('!rms')
def rms(msg):
    soup = BeautifulSoup(requests.get('https://rms.sexy').content)
    image = 'https://rms.sexy' + soup.find(class_='stallman')['src']
    return pinhook.plugin.message(image)

