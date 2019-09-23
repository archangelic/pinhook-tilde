import random

import emoji
import pinhook.plugin

hearts = [
    ':heart:',
    ':blue_heart:',
    ':yellow_heart:',
    ':purple_heart:',
    ':green_heart:',
    ':heartbeat:',
    ':heartpulse:',
    ':two_hearts:',
    ':revolving_hearts:',
    ':cupid:',
    ':sparkling_heart:',
    ':gift_heart:',
    ':hearts:',
    ':heart_decoration:',
]

def make_hearts_str():
    message = ''
    for i in range(0, 10):
        message += ' ' + random.choice(hearts)
    message = emoji.emojize(message.replace(' ', ''), use_aliases=True)
    return message

@pinhook.plugin.register('!hearts', help_text='share some love by printing heart emojis')
def make_hearts(msg):
    return pinhook.plugin.message(make_hearts_str())

@pinhook.plugin.register('!rainbowhearts', help_text='!hearts but with more color')
def make_rainbow_hearts(msg):
    return pinhook.plugin.message("!rainbow {}".format(make_hearts_str()))

