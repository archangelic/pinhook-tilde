import pinhook.plugin as p

@p.register('!dolphin')
def dolphin(msg):
    if msg.arg:
        eee = ''.join(format(ord(x), '08b') for x in msg.arg)
        eee = eee.replace('0', 'e')
        eee = eee.replace('1', 'E')
        n = 400
        eee = '\n'.join([eee[i:i+n] for i in range(0, len(eee), n)]).strip()
        msg.logger.info(eee)
        return p.message(eee)
    else:
        pass
