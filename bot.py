#!/usr/bin/env python3
import sys

import pinhook.bot

if __name__ == '__main__':
    default_channels = [
        '#arch-dev',
        '#tildetown',
        '#bots',
    ]
    if len(sys.argv) > 1:
        if sys.argv[1] == '--test-mode':
            channels = ['#arch-dev']
        else:
            channels = default_channels
    else:
        channels = default_channels
    bot = pinhook.bot.Bot(channels, 'pinhook-test', 'localhost', ops=['archangelic'])
    bot.start()
