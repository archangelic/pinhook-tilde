import json
import random
from os import listdir, path
import re

import markovify
import nltk
import pinhook.plugin


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [w for w in words if len(w) > 0]
        words = [":-:".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split(":-:")[0] for word in words)
        return sentence


def get_sentence(nick, user):
    if user in listdir('json'):
        with open(path.join('json', user)) as f:
            text = json.load(f)
        text_model = POSifiedText.from_json(text)
        return text_model.make_short_sentence(random.randrange(30, 201, 5), tries=100)
    else:
        return '{}: Sorry, {} was not found'.format(nick, user)

def fuse_users(user1, user2):
    if user1 in listdir('json') and user2 in listdir('json'):
        with open(path.join('json', user1)) as u1:
            user1_text = POSifiedText.from_json(json.load(u1))
        with open(path.join('json', user2)) as u2:
            user2_text = POSifiedText.from_json(json.load(u2))
        markov_model = markovify.combine(models=[user1_text, user2_text])
        return markov_model.make_short_sentence(random.randrange(30, 201, 5), tries=100)
    elif user1 not in listdir('json'):
        return '{} was not found'.format(user1)
    elif user2 not in listdir('json'):
        return '{} was not found'.format(user2)

def check_optout():
    with open('optout') as o:
        optout = [i.strip() for i in o.readlines() if i.strip()]
    return optout

def write_optout(optoutlist):
    with open('optout', 'w') as o:
        for i in optoutlist:
            o.write(i+'\n')

@pinhook.plugin.register('!talklike', help_text='talklike someone (yourself by default)')
@pinhook.plugin.register('!fuse', help_text='combine two users and try to talk like them')
def run(msg):
    optout = check_optout()
    nick = msg.nick
    if msg.arg:
        user = msg.arg
    else:
        user = msg.nick
    if msg.cmd == '!talklike':
        if user in optout:
            return pinhook.plugin.message('{}: {} has chosen not to be imitated by this bot'.format(msg.nick, user))
        msg = get_sentence(nick, user)
        if not msg:
            msg = '{}: could not generate text for {}'.format(nick, user)
    elif msg.cmd == '!fuse':
        try:
            user1, user2 = user.split()
            if user1 in optout:
                return pinhook.plugin.message('{}: {} has chosen not to be imitated by this bot'.format(msg.nick, user1))
            elif user2 in optout:
                return pinhook.plugin.message('{}: {} has chosen not to be imitated by this bot'.format(msg.nick, user2))
            msg = fuse_users(user1, user2)
            if not msg:
                msg = '{}: could not generate text for {} and {}'.format(nick, user1, user2)
        except:
            msg = "{}: Please give only 2 users".format(nick)
    return pinhook.plugin.message(msg)

@pinhook.plugin.register('!tloptin', help_text='opt into talklike if you opted out')
@pinhook.plugin.register('!tloptout', help_text='opt out of talklike')
def optinout(msg):
    optout = check_optout()
    if msg.cmd == '!tloptin':
        if msg.nick in optout:
            optout.remove(msg.nick)
            write_optout(optout)
            message = '{}: you have been removed from the opt out list'.format(msg.nick)
        else:
            message = '{}: you are already opted in'.format(msg.nick)
    if msg.cmd == '!tloptout':
        if msg.nick not in optout:
            optout.append(msg.nick)
            write_optout(optout)
            message = '{}: you have opted out of !talklike'.format(msg.nick)
        else:
            message = '{}: you have already opted out of !talklike'.format(msg.nick)
    return pinhook.plugin.message(message)

