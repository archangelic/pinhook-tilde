import shlex
import subprocess

import emoji
import pinhook.plugin

WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000

def widen(s):
        return s.translate(WIDE_MAP)

@pinhook.plugin.register('!toot')
def run(msg):
    if msg.arg:
        subprocess.call(['/usr/local/bin/toot', msg.arg])
        out = 'Your message has been posted to mastodon'
    else:
        out = 'Please enter a message to toot!'
    return pinhook.plugin.message(out)

@pinhook.plugin.register('!vapourtoot')
@pinhook.plugin.register('!vaportoot')
@pinhook.plugin.register('!tootwave')
def tootwave(msg):
    if msg.arg:
        message = emoji.emojize(msg.arg, use_aliases=True)
        wide = widen(message)
        subprocess.call(['/usr/local/bin/toot', wide])
        return pinhook.plugin.message('Your message "{}" has been posted to mastodon'.format(wide))
