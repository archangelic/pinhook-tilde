import random
import pinhook.plugin


verbs = [
    'wriggles slightly',
    'sighs cutely',
    'wriggles',
    'smiles',
]


@pinhook.plugin.register('!water')
def run(**kwargs):
    if kwargs['arg'] == 'pinhook':
        return pinhook.plugin.action(random.choice(verbs))
    else:
        return None
