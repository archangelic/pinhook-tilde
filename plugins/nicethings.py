import random

import pinhook.plugin

@pinhook.plugin.register('!nicethings')
def nicethings(**kwargs):
    with open('/home/m455/code/projects/nicethings/list.txt') as n:
        msg = random.choice(n.readlines()).strip()
    return pinhook.plugin.message(msg)
