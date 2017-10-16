import subprocess

import pinhook.plugin

@pinhook.plugin.register('!toot')
def run(msg):
    if msg.arg:
        subprocess.call(['toot', msg.arg])
        out = 'Your message has been posted to mastodon'
    else:
        out = 'Please enter a message to toot!'
    return pinhook.plugin.message(out)
