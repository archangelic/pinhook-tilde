import subprocess

commands = ['!toot']

def run(**kwargs):
    msg = kwargs['arg']
    subprocess.call('toot "{}"'.format(msg.replace('"', '\\"')), shell=True)
    return ('message', 'Your message has been posted to mastodon')
