from pinhook.plugin import listener, action

@listener('honk')
def honk(msg):
    if msg.text.lower().strip() == 'y':
        return action('HONK')
