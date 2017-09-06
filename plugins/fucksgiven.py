from os import listdir, path
import re

commands = ['!fucksgiven']

def run(**kwargs):
    nick = kwargs['nick']
    trunc_nick = nick[:9]
    if trunc_nick in listdir('users'):
        with open(path.join('users', trunc_nick)) as u:
            text = u.read()
            count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape('fuck'), text))
        if count != 1:
            ending = 's'
        else:
            ending = ''
        return ('message', '{} gives exactly {} fuck{}'.format(nick, count, ending))
