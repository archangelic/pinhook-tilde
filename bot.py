#!/usr/bin/env python3
import json
import sys

import pinhook.bot

with open('config.json') as c:
    config = json.load(c)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--test-mode':
            channels = ['#arch-dev']
        else:
            channels = config['channels']
    else:
        channels = config['channels']
    bot = pinhook.bot.Bot(channels, 'pinhook', 'localhost', ops=['archangelic'], ns_pass=config['password'], nickserv='nickserv')
    bot.start()
