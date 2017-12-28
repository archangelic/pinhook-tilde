import re
import pinhook.plugin

@pinhook.plugin.register('!temp')
def convert(msg):
    if re.match(r'^-?\d+[c,f]$', msg.arg.lower()):
        if msg.arg.lower().endswith('f'):
            t = int(msg.arg[:-1])
            c = int((t - 32) * 5 / 9)
            out = str(c) + 'c'
        elif msg.arg.lower().endswith('c'):
            t = int(msg.arg[:-1])
            c = int((t * 9/5) + 32)
            out = str(c) + 'f'
        return pinhook.plugin.message(out)
