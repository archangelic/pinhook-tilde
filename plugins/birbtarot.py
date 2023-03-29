import json
import random

import pinhook.plugin as p

with open('birbtarot.json') as b:
    tarot = json.load(b)

cards = [_ for _ in tarot]

orientations = {
    'up': [
        "",
        " (dropped out of a tree)",
        " (found in a bird's nest)",
        " (slightly askew)"
    ],
    'down': [
        " (reversed)",
        " (found in a birdcage)",
        " (pecked at)",
        " (found under a tree)"
    ]
}


@p.command('!birbtarot', help_text='bird themed tarot cards')
def birb(msg):
    card = random.choice(cards)
    orientation = random.choice(list(orientations.keys()))
    position = random.choice(orientations[orientation])
    description = f'{card}{position} - {tarot[card][orientation]}'.strip('- ')
    return p.message(description)
