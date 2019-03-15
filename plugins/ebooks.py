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
        words = [":-:".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split(":-:")[0] for word in words)
        return sentence

ebooksdir = path.join(path.dirname(path.abspath(__file__)), 'ebooks')

def generate_message(ebook):
    with open(path.join(ebooksdir, ebook)) as e:
        model = POSifiedText.from_json(json.load(e))
    return pinhook.plugin.message(model.make_short_sentence(512))

with open(path.join(ebooksdir, 'evil.json')) as e:
    evil = POSifiedText.from_json(json.load(e))

@pinhook.plugin.register('!cyber')
def cyber(msg):
    out = requests.get('http://cyber.archangelic.space/snippet').content.decode()
    return pinhook.plugin.message(out)

@pinhook.plugin.register('!lordmarkov')
def lordmarkov(msg):
    out = 'If I Ever Become an Evil Overlord: '
    out += evil.make_short_sentence(476)
    return pinhook.plugin.message(out)

@pinhook.plugin.register('!bitcoin')
def btc(msg):
    return generate_message('btc.json')

@pinhook.plugin.register('!lisp')
def lisp(msg):
    return generate_message('lisp.json')

@pinhook.plugin.register('!naked')
def naked(msg):
    return generate_message('naked.json')

@pinhook.plugin.register('!python')
def python(msg):
    return generate_message('python.json')
