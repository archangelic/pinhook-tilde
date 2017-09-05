#!/usr/bin/env python3
import time
import sys

import irc.bot
from plugins import *

irc.client.ServerConnection.buffer_class.errors = 'replace'


class TVBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channels, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.chanlist = channels
        self.bot_nick = nickname
        self.operator = 'archangelic'

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
        message = ''
        action = ''
        if cmd == '!join' and nick == self.operator:
            c.join(arg)
            message = '{}: joined {}'.format(nick, arg)
        if cmd == '!quit' and nick == self.operator:
            c.quit("See y'all later!")
            quit()
        if cmd == '!tv':
            message = tv.next_up(arg)
        if cmd == '!tvalias':
            message = tv.alias_show(arg)
        if cmd == '!rollcall':
            message = 'Available commands: !tv, !doctorow, !botany, !talklike, !beats, !pronouns'
        if cmd == '!doctorow':
            message = ebooks.doctorow()
        if cmd == '!botany':
            message = watered.run(nick)
        if cmd == '!talklike':
            message = tildetalk.run(nick, arg)
        if text.strip() == '!water ' + self.bot_nick:
            action = waterme.water()
        if cmd == '!beats':
            message = swatch.swatch()
        if cmd == '!mypronouns':
            message = pronouns.my_pronouns(nick, arg)
        if cmd == '!pronouns':
            message = pronouns.get_pronouns(arg)
        if cmd == '!fucksgiven':
            message = fucksgiven.run(nick)
        if cmd == '!shakespear' or cmd == '!shakespeare':
            message = shakespeare.get_sentence()

        if message:
            c.privmsg(chan, message)
        elif action:
            c.action(chan, action)


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
