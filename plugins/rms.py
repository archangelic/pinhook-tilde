import pinhook.plugin

@pinhook.plugin.register('!rms')
def rms(msg):
    return pinhook.plugin.message('https://rms.sexy')

