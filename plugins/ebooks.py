import random

import pinhook.plugin

@pinhook.plugin.register('!doctorow')
def doctorow(msg):
    with open('doctorow_ebooks.txt', 'r') as ebooks:
        lines = ebooks.read().split('\n')
        quotes = [line for line in lines if line]
    return pinhook.plugin.message(random.choice(quotes))

