import json
import re
import os

import markovify
import nltk
import requests
import pinhook.plugin
import toml

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
    return sorted([os.path.splitext(i)[0] for i in os.listdir(ebooksdir)])

def generate_message(ebook, tries=50):
    patterns = toml.load('ebooks_patterns.toml')['patterns']
    patterns = {k: re.compile(v, re.IGNORECASE) for k,v in patterns.items()}
    with open(os.path.join(ebooksdir, ebook)) as e:
        model = POSifiedText.from_json(json.load(e))
    for x in range(tries):
        sentence = model.make_short_sentence(400)
        if patterns[ebook].search(sentence):
            return pinhook.plugin.message(sentence)
    return None

@pinhook.plugin.command('!cyber', help_text='markov cyberpunk snippet')
def cyber(msg):
    out = requests.get('http://cyber.archangelic.space/snippet').content.decode()
    return pinhook.plugin.message(out)

@pinhook.plugin.command('!talkabout', help_text='talk about several topics using markov chains')
def talkabout(msg):
    if msg.arg.lower() in get_subjects():
        return generate_message('{}.json'.format(msg.arg.lower()))
    else:
        return pinhook.plugin.message('please select one of the following: {}'.format(', '.join(get_subjects())))
