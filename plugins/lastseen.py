from datetime import datetime

import pinhook.plugin

@pinhook.plugin.register('!seen')
@pinhook.plugin.register('!lastseen')
def last_seen(msg):
    entries = []
    with open('/home/archangelic/irc/log', 'rb') as f:
        lines = f.readlines()
    for line in lines:
        try:
            l = line.split(b'\t')
            d = l[0]
            u = l[1]
            if u.decode() == msg.arg[:9]:
                entries.append(float(d))
        except:
            continue
    if entries:
        entries.sort()
        last_entry = entries[-1]
        if msg.arg in msg.nick_list:
            leader = '{} is currently online and in the channel!'.format(msg.arg)
        else:
            leader = msg.arg
        out = '{} last spoke in chat on {}'.format(leader, datetime.fromtimestamp(last_entry))
    else:
        out = 'Sorry, {} was not found'.format(msg.arg)
    return pinhook.plugin.message(out)
