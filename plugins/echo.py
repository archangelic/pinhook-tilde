import pinhook.plugin

@pinhook.plugin.register('!phecho')
def echo(msg):
    if msg.nick in msg.ops:
        return pinhook.plugin.message(msg.arg)
