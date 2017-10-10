import subprocess

import pinhook.plugin

@pinhook.plugin.register('!toot')
def run(msg):
    subprocess.call('toot "{}"'.format(msg.arg.replace('"', '\\"')), shell=True)
    return pinhook.plugin.message('Your message has been posted to mastodon')
