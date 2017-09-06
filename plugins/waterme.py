import random

commands = ['!water']

verbs = [
    'wriggles slightly',
    'sighs cutely',
    'wriggles',
    'smiles',
]


def run(**kwargs):
    if kwargs['arg'] == 'pinhook':
        return ('action', random.choice(verbs))
    else:
        return None
