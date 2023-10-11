import json

import tracery
from tracery.modifiers import base_english
import pinhook.plugin as p


@p.listener('character')
def character(msg):
    if 'roll a character' in msg.text.lower():
        with open(f'/home/archangelic/.tracery/dnd.json') as m:
            magic_rules = json.load(m)

        magic = tracery.Grammar(magic_rules)
        magic.add_modifiers(base_english)
        out = magic.flatten('#origin#')
        return p.message(out)
