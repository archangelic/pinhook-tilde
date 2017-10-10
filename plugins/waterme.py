import random
import pinhook.plugin


verbs = [
    'wriggles slightly',
    'sighs cutely',
    'wriggles',
    'smiles',
]


@pinhook.plugin.register('!water')
def run(msg):
    if msg.arg == msg.botnick:
        return pinhook.plugin.action(random.choice(verbs))
    else:
        return None
