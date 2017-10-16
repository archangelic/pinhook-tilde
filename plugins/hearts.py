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
]

@pinhook.plugin.register('!hearts')
def make_hearts(msg):
    message = ''
    for i in range(0, 10):
        message += ' ' + random.choice(hearts)
    message = emoji.emojize(message.replace(' ', ''), use_aliases=True)
    return pinhook.plugin.message(message)
