import pinhook.plugin as p

@p.register('!dolphin')
def dolphin(msg):
    if msg.arg:
        eee = ''.join(format(ord(x), 'b') for x in msg.arg)
        eee = eee.replace('0', 'e')
        eee = eee.replace('1', 'E')
        return p.message(eee)
    else:
        pass