import pinhook.plugin

@pinhook.plugin.register('!phecho')
@pinhook.plugin.ops('!phecho')
def echo(msg):
    if msg.nick in msg.ops:
        msg.privmsg('#arch-dev', msg.arg)
        msg.action('#arch-dev', msg.arg)
        msg.notice('archangelic', msg.arg)
        msg.logger.debug(pinhook.plugin.cmds)
        return pinhook.plugin.message(msg.arg)
