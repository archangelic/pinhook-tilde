import pinhook.plugin
import subprocess

cmd = '/home/l0010o0001l/go/src/github.com/l0010o0001l/ud/main'

@pinhook.plugin.register('!ud')
def ud(msg):
    out = subprocess.check_output([cmd, msg.arg]).decode()
    out = out.replace('\n', '').replace('\r', '')
    return pinhook.plugin.message(out)
