#!/usr/bin/env python3
import imp
import os
import time
import sys

import irc.bot

irc.client.ServerConnection.buffer_class.errors = 'replace'


class TVBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channels, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.chanlist = channels
        self.bot_nick = nickname
        self.operator = 'archangelic'

        # load the plugins
        plugins = {}
        for m in os.listdir('plugins'):
            if m.endswith('.py'):
                name = m[:-3]
                fp, pathname, description = imp.find_module(name, ['plugins'])
                plugins[name] = imp.load_module(name, fp, pathname, description)

        # load the commands
        self.cmds = {}
        for i in plugins:
            for c in plugins[i].commands:
                self.cmds[c] = plugins[i]

    def on_welcome(self, c, e):
        for channel in self.chanlist:
            c.join(channel)

    def on_pubmsg(self, c, e):
        self.process_command(c, e, e.arguments[0])

    def on_privmsg(self, c, e):
        self.process_command(c, e, e.arguments[0])

    def process_command(self, c, e, text):
        nick = e.source.nick
        if e.target == self.bot_nick:
            chan = nick
        else:
            chan = e.target
        cmd = text.split(' ')[0]
        if len(text.split(' ')) > 1:
            arg = ''.join([i + ' ' for i in text.split(' ')[1:]]).strip()
        else:
            arg = ''
        output = ()
        if cmd == '!join' and nick == self.operator:
            c.join(arg)
            c.privmsg(chan, '{}: joined {}'.format(nick, arg))
        elif cmd == '!quit' and nick == self.operator:
            c.quit("See y'all later!")
            quit()
        elif cmd in self.cmds:
            output = self.cmds[cmd].run(cmd=cmd, arg=arg, nick=nick)

        if not output:
            pass
        elif output[0] == 'message':
            c.privmsg(chan, output[1])
        elif output[0] == 'action':
            c.action(chan, output[1])


if __name__ == '__main__':
    default_channels = [
        '#arch-dev',
        '#tildetown',
        '#bots',
    ]
    if len(sys.argv) > 1:
        if sys.argv[1] == '--test-mode':
            channels = ['#arch-dev']
        else:
            channels = default_channels
    else:
        channels = default_channels
    bot = TVBot(channels, 'pinhook', 'localhost')
    bot.start()
