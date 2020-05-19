import json

import pinhook.plugin

@pinhook.plugin.command('!hecksgiven', 'alias of !fucksgiven')
@pinhook.plugin.command('!fucksgiven', 'gives the number of fucks you have said in #tildetown')
def run(msg):
    with open('/home/archangelic/public_html/fucks.json') as f:
        fucks = json.load(f)
    if msg.nick in fucks['users']:
        count = fucks['users'][msg.nick]['total']
        if count != 1:
            ending = 's'
        else:
            ending = ''
        return pinhook.plugin.message('{} gives exactly {} fuck{}'.format(msg.nick, count, ending))
    else:
        return pinhook.plugin.message("Sorry, I couldn't find your username. I'm sure you'll show up in my data soon!")
