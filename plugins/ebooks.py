import json
import re
from os import path

import markovify
import nltk
import requests
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


@pinhook.plugin.register('!cyber')
def run(msg):
    if msg.cmd == '!cyber':
        out = requests.get('http://cyber.archangelic.space/snippet').content.decode()
    return pinhook.plugin.message(out)

