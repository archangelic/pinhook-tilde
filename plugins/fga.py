import pinhook.plugin
import subprocess

cmd = '/home/l0010o0001l/go/bin/tilde-fucksgiven-analytics'

@pinhook.plugin.register('!fga')
def fga(msg):
    out = subprocess.check_output([cmd, msg.arg]).decode()
    return pinhook.plugin.message(out)
