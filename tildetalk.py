import json
import random
from os import listdir, path
import re

import markovify
import nltk


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [w for w in words if len(w) > 0]
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


def get_sentence(nick, user):
    sentence_sizes = [i for i in range(30,201) if i%5==0]
    user_dir = 'json'
    if user not in listdir('json') and len(user) > 8:
        user = user[:9]
    elif user not in listdir('json'):
        if user not in listdir('users') and len(user) > 8:
            user = user[:9]
        if user not in listdir('users'):
            return '{}: Sorry, {} not found.'.format(nick, user)
        else:
            user_dir = 'users'
    try:
        if user_dir == 'json':
            with open(path.join('json', user)) as f:
                text = json.load(f)

            text_model = POSifiedText.from_json(text)
        elif user_dir == 'users':
            with open(path.join(user_dir, user)) as f:
                text = f.read
            text_model = markovify.Text(text)

        return text_model.make_short_sentence(random.choice(sentence_sizes))

    except:
        return "{}: I'm sorry, I don't have enough info to talk like {}".format(nick, user)

def run(nick, user):
    msg = get_sentence(nick, user)
    x = 0
    while not msg:
        msg = get_sentence(nick, user)
        x += 1
        if x == 10 and not msg:
            msg = "Sorry, there was an error"
    return msg

