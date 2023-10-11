import random

import emoji
import pinhook.plugin

hearts = [
    ':cupid:',
    ':gift_heart:',
    ':sparkling_heart:',
    ':heartpulse:',
    ':heartbeat:',
    ':revolving_hearts:',
    ':two_hearts:',
    ':heart_decoration:',
    ':heart_exclamation:',
    ':broken_heart:',
    ':heart_on_fire:',
    ':mending_heart:',
    ':heart:',
    ':pink_heart:',
    ':orange_heart:',
    ':yellow_heart:',
    ':green_heart:',
    ':blue_heart:',
    ':light_blue_heart:',
    ':purple_heart:',
    ':brown_heart:',
    ':black_heart:',
    ':grey_heart:',
    ':white_heart:',
]

def make_hearts_str():
    message = ''
    for i in range(0, 10):
        message += ' ' + random.choice(hearts)
    message = emoji.emojize(message.replace(' ', ''), language='alias')
    return message

@pinhook.plugin.command('!hearts', help_text='share some love by printing heart emojis')
def make_hearts(msg):
    return pinhook.plugin.message(make_hearts_str())

@pinhook.plugin.command('!rainbowhearts', help_text='!hearts but with more color')
def make_rainbow_hearts(msg):
    return pinhook.plugin.message("!rainbow {}".format(make_hearts_str()))

