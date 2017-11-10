import subprocess

import pinhook.plugin

@pinhook.plugin.register('!uptime')
def uptime(msg):
    out = subprocess.check_output(['uptime'])
    return pinhook.plugin.message(out.decode().strip())
