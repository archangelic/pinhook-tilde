import pinhook.plugin

@pinhook.plugin.register('!phecho')
def echo(msg):
    return pinhook.plugin.message(msg.arg)
