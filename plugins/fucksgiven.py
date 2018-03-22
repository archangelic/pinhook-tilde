from os import listdir, path
import re

import pinhook.plugin

@pinhook.plugin.register('!fucksgiven')
def run(msg):
    if msg.nick in listdir('users'):
        with open(path.join('users', msg.nick)) as u:
            text = u.read().lower()
            count = sum(1 for _ in re.finditer(r'\bfuck[a-z]*\b', text))
        if count != 1:
            ending = 's'
        else:
            ending = ''
        return pinhook.plugin.message('{} gives exactly {} fuck{}'.format(msg.nick, count, ending))
    else:
        return pinhook.plugin.message("Sorry, I couldn't find your username")
