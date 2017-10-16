import random

import pinhook.plugin

nicelist = '/home/m455/code/projects/nicethings/list.txt'

@pinhook.plugin.register('!nicethings')
def nicethings(message):
    with open(nicelist, 'r') as n:
        msg = random.choice(n.readlines()).strip()
    return pinhook.plugin.message(msg)

@pinhook.plugin.register('!addnicething')
def addnicething(message):
    with open(nicelist, 'a') as n:
        n.write(message.arg + '\n')
    out = '{}: thanks!'.format(message.nick)
    return pinhook.plugin.message(out)
