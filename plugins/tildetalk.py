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
        return text_model.make_short_sentence(random.randrange(30, 201, 5))
    else:
        return '{}: Sorry, {} was not found'.format(nick, user)


def run(nick, user):
    msg = get_sentence(nick, user)
    x = 0
    while not msg:
        msg = get_sentence(nick, user)
        x += 1
        if x == 10 and not msg:
            msg = "Sorry, there was an error"
    return msg
