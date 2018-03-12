import pinhook.plugin
import os

cmd = '/home/l0010o0001l/go/src/github.com/l0010o0001l/ud/main'

@pinhook.plugin.register('!ud')
def ud(msg):
    out = os.popen('%s %s', cmd, msg.arg).read()
    out = out.replace('\n', '').replace('\r', '')
    return pinhook.plugin.message(out)
