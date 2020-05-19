import subprocess

import pinhook.plugin

@pinhook.plugin.command('!date', help_text='current date')
def get_time(msg):
    out = subprocess.check_output(['date']).decode().strip()
    return pinhook.plugin.message(out)

@pinhook.plugin.command('!load', help_text='current cpu load')
@pinhook.plugin.command('!uptime', help_text='current server uptime')
def uptime(msg):
    out = subprocess.check_output(['uptime']).decode().strip()
    if msg.cmd == '!load':
        out = ', '.join(out.split(',')[-3:]).strip()
    return pinhook.plugin.message(out)
