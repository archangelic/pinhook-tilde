import pinhook.plugin

@pinhook.plugin.command('!phecho', ops=True)
def echo(msg):
    if msg.nick in msg.ops:
        msg.privmsg('#arch-dev', msg.arg)
        msg.action('#arch-dev', msg.arg)
        msg.notice('archangelic', msg.arg)
        msg.logger.debug(pinhook.plugin.cmds)
        return pinhook.plugin.message(msg.arg)
