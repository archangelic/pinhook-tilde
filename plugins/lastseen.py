from datetime import datetime
import re
import shlex
import subprocess

import pinhook.plugin

@pinhook.plugin.command('!seen', help_text="determine when user last spoke in main chat")
@pinhook.plugin.command('!lastseen', help_text="alias of !seen")
def last_seen(msg):
    pattern = re.compile(r'^(?P<stamp>\d+)\t{}\t(?P<message>.*)$'.format(msg.arg))
    entries = []
    messages = {}
    with open('/home/archangelic/irc/log', 'rb') as f:
        lines = f.readlines()
    for line in lines:
        line = line.decode('utf-8', 'ignore')
        result = pattern.search(line)
        if result:
            entries.append(float(result.group('stamp')))
            messages[str(float(result.group('stamp')))] = result.group('message')
    if entries:
        entries.sort()
        last_entry = entries[-1]
        if msg.arg in msg.nick_list and msg.channel == '#tildetown':
            leader = '{} is currently online and in the channel!'.format(msg.arg)
        else:
            leader = msg.arg
        out = '{} last spoke in #tildetown on {} and said "{}"'.format(leader, datetime.fromtimestamp(last_entry), messages[str(last_entry)])
    else:
        out = 'Sorry, {} was not found'.format(msg.arg)
    return pinhook.plugin.message(out)

@pinhook.plugin.command('!mentions', 'get your mentions')
def mentions(msg):
    cmd = "/home/archangelic/bin/mensch -u {} -t 24 -z +0".format(msg.nick)
    cmd = [bytes(i, 'utf-8') for i in shlex.split(cmd)]
    menschns = subprocess.check_output(cmd).decode().replace("\t", ": ").split("\n")
    for mention in menschns:
        if mention:
            msg.privmsg(msg.nick, mention)

