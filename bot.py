#!/usr/bin/env python3
import configparser
import sys

import pinhook.bot

config = configparser.ConfigParser()
config.read('config.ini')

if __name__ == '__main__':
    default_channels = ['#'+_ for _ in config['channels']]
    print(config['main']['password'])
    if len(sys.argv) > 1:
        if sys.argv[1] == '--test-mode':
            channels = ['#arch-dev']
        else:
            channels = default_channels
    else:
        channels = default_channels
    bot = pinhook.bot.Bot(channels, 'pinhook', 'localhost', ops=['archangelic'], ns_pass=config['main']['password'], nickserv='nickserv')
    bot.start()
