import json
import re
import os

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

ebooksdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ebooks')

def get_subjects():
    return sorted([os.path.splitext(i)[0] for i in os.listdir(ebooksdir) if i != 'evil.json'])

def generate_message(ebook):
    with open(os.path.join(ebooksdir, ebook)) as e:
        model = POSifiedText.from_json(json.load(e))
    return pinhook.plugin.message(model.make_short_sentence(512))

with open(os.path.join(ebooksdir, 'evil.json')) as e:
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

@pinhook.plugin.register('!talkabout')
def talkabout(msg):
    if msg.arg.lower() in get_subjects():
        return generate_message('{}.json'.format(msg.arg.lower()))
    else:
        return pinhook.plugin.message('please select one of the following: {}'.format(', '.join(get_subjects())))
