from bs4 import BeautifulSoup
import pinhook.plugin
import requests

@pinhook.plugin.register('!rms')
def rms(msg):
    result = requests.get("https://rms.sexy")
    soup = BeautifulSoup(result.content)
    image = 'https://rms.sexy' + soup.find(class_='stallman')['src']
    return pinhook.plugin.message(image)

