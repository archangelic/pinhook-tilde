import json

import pinhook.plugin

@pinhook.plugin.command('!hecksgiven', 'alias of !fucksgiven')
@pinhook.plugin.command('!fucksgiven', 'gives the number of fucks you have said in #tildetown')
def run(msg):
    if msg.arg:
        user = msg.arg
    else:
        user = msg.nick
    with open('/home/archangelic/public_html/fucks.json') as f:
        fucks = json.load(f)
    if user in fucks['users']:
        count = fucks['users'][user]['total']
        if count != 1:
            ending = 's'
        else:
            ending = ''
        return pinhook.plugin.message('{} gives exactly {} fuck{}'.format(user, count, ending))
    else:
        return pinhook.plugin.message("Sorry, I couldn't find fucks for {}. I'm sure you'll show up in my data soon!".format(user))
