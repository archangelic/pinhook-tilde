import pinhook.plugin

@pinhook.plugin.listener('numanuma')
def numanuma(msg):
    if 'numa numa' in msg.text.lower() or 'numanuma' in msg.text.lower():
        return pinhook.plugin.action("dances with {}".format(msg.nick))
