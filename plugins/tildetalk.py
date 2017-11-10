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
        words = ["::".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


def get_sentence(nick, user):
    trunc_user = user[:9]
    if trunc_user in listdir('json'):
        with open(path.join('json', trunc_user)) as f:
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

@pinhook.plugin.register('!talklike')
@pinhook.plugin.register('!fuse')
def run(msg):
    nick = msg.nick
    user = msg.arg
    if msg.cmd == '!talklike':
        msg = get_sentence(nick, user)
        if not msg:
            msg = '{}: could not generate text for {}'.format(nick, user)
    elif msg.cmd == '!fuse':
        try:
            user1, user2 = user.split()
            user1 = user1[:9]
            user2 = user2[:9]
            msg = fuse_users(user1, user2)
            if not msg:
                msg = '{}: could not generate text for {} and {}'.format(nick, user1, user2)
        except:
            msg = "{}: Please give only 2 users".format(nick)
    return pinhook.plugin.message(msg)
