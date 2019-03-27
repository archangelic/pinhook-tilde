import subprocess

import pinhook.plugin

@pinhook.plugin.register('!date')
def get_time(msg):
    out = subprocess.check_output(['date']).decode().strip()
    return pinhook.plugin.message(out)

@pinhook.plugin.register('!load')
@pinhook.plugin.register('!uptime')
def uptime(msg):
    out = subprocess.check_output(['uptime']).decode().strip()
    if msg.cmd == '!load':
        out = ', '.join(out.split(',')[-3:]).strip()
    return pinhook.plugin.message(out)
