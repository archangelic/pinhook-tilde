import random

import pinhook.plugin as p

@p.listener('personality')
def personality(msg):
    if msg.text.startswith(msg.botnick):
        acts = [
            'wiggles',
            'wriggles',
            'looks expectantly',
            'looks happily',
            'looks lazily',
            f'looks at {msg.nick}'
        ]
        return p.action(random.choice(acts))
