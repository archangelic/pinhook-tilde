#!/usr/bin/env python3
import json
import os
import re

import markovify
import nltk
import toml

ignored_users = ['cosnok', 'pinhook', 'quote_bot', 'tracer', 'sedbot']
regex = re.compile(b"\x01|\x1f|\x02|\x12|\x0f|\x16|\x03(?:\d{1,2}(?:,\d{1,2})?)?")

with open('/home/archangelic/irc/log', 'rb') as i:
        lines = i.readlines()

with open('/home/pinhook/pinhook/optout') as o:
    for x in o.readlines():
        if x:
            ignored_users.append(x)

class POSifiedText(markovify.NewlineText):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [w for w in words if len(w) > 0]
        words = [":-:".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split(":-:")[0] for word in words)
        return sentence

def get_patterns():
    patterns = toml.load('ebooks_patterns.toml')['patterns']
    patterns = {k: re.compile(v, re.IGNORECASE) for k,v in patterns.items()}
    return patterns

def make_sentence(sentence):
    word_list = sentence.split()
    if word_list[0].endswith(':'):
        word_list.pop(0)
    if word_list[0].startswith(('!', ',')):
        word_list = []
    sentence = ''.join([i + ' ' for i in word_list if not i.startswith('http')]).strip()
    return sentence

def check_line(pattern, sentence):
    s = sentence.split('\t')
    try:
        if s[1] not in ignored_users and not s[2].startswith('pinhook:'):
            results = pattern.search(sentence)
        if results:
            sentence = make_sentence(s[2])
        else:
            sentence = None
        return sentence
    except:
        return None

def make_model(sentences, filename):
    corpus = ''.join([_+'\n' for _ in sentences])
    model_json = POSifiedText(corpus).to_json()
    with open(os.path.join('plugins', 'ebooks', filename), 'w') as j:
        json.dump(model_json, j)

if __name__=='__main__':
    patterns = get_patterns()
    for p in patterns:
        sentences = []
        filename = p + '.json'
        pattern = patterns[p]
        for line in lines:
            line = regex.sub(b'', line)
            line = line.decode('UTF-8', errors='replace').replace('ACTION', '')
            sentence = check_line(pattern, line)
            if sentence:
                sentences.append(sentence)
        make_model(sentences, filename)

