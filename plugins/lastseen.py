from datetime import datetime
import re

import pinhook.plugin

@pinhook.plugin.register('!seen', help_text="determine when user last spoke in main chat")
@pinhook.plugin.register('!lastseen', help_text="alias of !seen")
def last_seen(msg):
    pattern = re.compile(r'^(?P<stamp>\d+)\t{}\t'.format(msg.arg))
    entries = []
    with open('/home/archangelic/irc/log', 'rb') as f:
        lines = f.readlines()
    for line in lines:
        line = line.decode('utf-8', 'ignore')
        result = pattern.search(line)
        if result:
            entries.append(float(result.group('stamp')))
    if entries:
        entries.sort()
        last_entry = entries[-1]
        if msg.arg in msg.nick_list and msg.channel == '#tildetown':
            leader = '{} is currently online and in the channel!'.format(msg.arg)
        else:
            leader = msg.arg
        out = '{} last spoke in #tildetown on {}'.format(leader, datetime.fromtimestamp(last_entry))
    else:
        out = 'Sorry, {} was not found'.format(msg.arg)
    return pinhook.plugin.message(out)
