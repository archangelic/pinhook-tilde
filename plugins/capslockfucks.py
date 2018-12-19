import pinhook.plugin
import subprocess

cmd = '/home/l0010o0001l/go/src/github.com/l0010o0001l/fucks/main'

@pinhook.plugin.register('!capsfucks')
def capsfucks(msg):
    out = subprocess.check_output([cmd, msg.arg]).decode()
    out = out.replace('\n', ' - ')
    return pinhook.plugin.message(out)
