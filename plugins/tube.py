import re
import shlex
import subprocess

import pinhook.plugin as p

@p.listener('tube')
def tube(msg):
    match = re.match(r'.*(https:\/\/hooktube.com/watch\?v=[a-zA-z0-9\-_]+).*', msg.text)
    if match:
        msg.logger.debug(match.group(1))
        cmd = shlex.split(r'youtube-dl -e "{}"'.format(match.group(1)))
        title = subprocess.check_output(cmd).decode().strip()
        out = '["{}"]'.format(title)
        return p.message(out)
