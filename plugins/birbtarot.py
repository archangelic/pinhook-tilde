import json
import random

import pinhook.plugin as p

with open('birbtarot.json') as b:
    tarot = json.load(b)

cards = [_ for _ in tarot]
orientation = [
    " (reversed)",
    " (slightly askew)",
    " (pecked at)",
    " (found in a bird's nest)",
    " (found in a birdcage)",
    " (dropped out of a tree)",
    " (found under a tree)",
    "",
    "",
    ""
]

@p.register('!birbtarot', help_text='bird themed tarot cards')
def birb(msg):
    return p.message(random.choice(cards) + random.choice(orientation))
