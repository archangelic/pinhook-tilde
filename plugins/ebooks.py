import json
import re
from os import path

import markovify
import nltk
import requests
import pinhook.plugin

shakespeare = path.join(path.dirname(path.abspath(__file__)), 'shakespeare.json')

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [w for w in words if len(w) > 0]
        words = ["::".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

with open(shakespeare) as s:
    shakespeare = POSifiedText.from_json(json.load(s))

@pinhook.plugin.register('!shakespear')
@pinhook.plugin.register('!cyber')
def run(msg):
    if msg.cmd == '!shakespeare' or msg.cmd == '!shakespear':
        out = shakespeare.make_sentence()
    elif msg.cmd == '!cyber':
        out = requests.get('http://cyber.archangelic.space/snippet').content.decode()
    return pinhook.plugin.message(out)

