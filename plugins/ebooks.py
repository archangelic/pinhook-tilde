import json
import random
from os import listdir, path
import re

import markovify
import nltk
import pinhook.plugin

shakespeare = path.join(path.dirname(path.abspath(__file__)), 'shakespeare.json')
cyber = path.join(path.dirname(path.abspath(__file__)), 'cyber.json')

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [w for w in words if len(w) > 0]
        words = ["::".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


@pinhook.plugin.register('!shakespeare')
@pinhook.plugin.register('!shakespear')
@pinhook.plugin.register('!cyber')
def run(msg):
    if msg.cmd == '!shakespeare' or msg.cmd == '!shakespear':
        json_file = shakespeare
    elif msg.cmd == '!cyber':
        json_file = cyber
    with open(json_file) as f:
        text = json.load(f)
    text_model = POSifiedText.from_json(text)
    return pinhook.plugin.message(text_model.make_sentence())

