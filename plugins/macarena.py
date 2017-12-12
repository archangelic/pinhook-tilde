import pinhook.plugin

@pinhook.plugin.listener('macarena')
def macarena(msg):
    if 'macarena' in msg.text.lower():
        return pinhook.plugin.action('dances')
