#!/usr/bin/env python3
import time

import ebooks
import irc.bot
import pronouns
import tildetalk
import tv
import swatch
import watered
import waterme

irc.client.ServerConnection.buffer_class.errors = 'replace'


class TVBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channels, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.chanlist = channels
        self.bot_nick = nickname

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
        if cmd == '!tv':
            show = text.lstrip('!tv').strip()
            message = tv.next_up(show)
            c.privmsg(chan, message)
        if cmd == '!tvalias':
            text = text.lstrip('!tvalias').strip()
            message = tv.alias_show(text)
            c.privmsg(chan, message)
        if cmd == '!rollcall':
            message = 'Available commands: !tv, !doctorow, !botany, !talklike'
            c.privmsg(chan, message)
        if cmd == '!doctorow':
            message = ebooks.doctorow()
            c.privmsg(chan, message)
        if cmd == '!botany':
            message = watered.run(nick)
            c.privmsg(chan, message)
        if cmd == '!talklike':
            user = text.lstrip('!tildetalk').strip()
            message = tildetalk.run(nick, user)
            c.privmsg(chan, message)
        if text.strip() == '!water ' + self.bot_nick:
            message = waterme.water()
            c.action(chan, message)
        if cmd == '!beats':
            message = swatch.swatch()
            c.privmsg(chan, message)
        if cmd == '!mypronouns':
            text = text.lstrip(cmd).strip()
            message = pronouns.my_pronouns(nick, text)
            c.privmsg(chan, message)
        if cmd == '!pronouns':
            pronouns = text.lstrip(cmd).strip()
            message = pronouns.get_pronouns(user)
            c.privmsg(chan, message)


if __name__ == '__main__':
    channels = [
        '#tildetown',
        '#bots',
    ]
    bot = TVBot(channels, 'pinhook', 'localhost')
    bot.start()
