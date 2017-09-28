import subprocess

import pinhook.plugin

@pinhook.plugin.register('!toot')
def run(**kwargs):
    msg = kwargs['arg']
    subprocess.call('toot "{}"'.format(msg.replace('"', '\\"')), shell=True)
    return pinhook.plugin.message('Your message has been posted to mastodon')
