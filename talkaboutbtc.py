#!/usr/bin/env python3
import json
import os
import re

import markovify
import nltk

bot_users = ['cosnok', 'pinhook', 'quote_bot', 'tracer', 'sedbot']
regex = re.compile(b"\x01|\x1f|\x02|\x12|\x0f|\x16|\x03(?:\d{1,2}(?:,\d{1,2})?)?")
btc_pattern = re.compile(r'(cryptocurrenc(ies|y)|bitcoin|ethereum|dogecoin|\bbtc\b|\beth\b|blockchain)', re.IGNORECASE)
lisp_pattern = re.compile(r'\b(scheme|clojure(script)?|e?lisp[sy]?|racket|hy|guile|haskell|urn)\b', re.IGNORECASE)
nude_pattern = re.compile(r'n(ud(es?|ity)|ake(d(ness)?|e|y)|sfw)', re.IGNORECASE)
python_pattern = re.compile(r'python(ic|ista)?', re.IGNORECASE)
patterns = {
    'bitcoin.json': btc_pattern,
    'lisp.json': lisp_pattern,
    'naked.json': nude_pattern,
    'python.json': python_pattern,
}

with open('/home/archangelic/irc/log', 'rb') as i:
        lines = i.readlines()

class POSifiedText(markovify.NewlineText):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [w for w in words if len(w) > 0]
        words = [":-:".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split(":-:")[0] for word in words)
        return sentence

def make_sentence(sentence):
    word_list = sentence.split()
    if word_list[0].endswith(':'):
        word_list.pop(0)
    if word_list[0].startswith('!'):
        word_list = []
    sentence = ''.join([i + ' ' for i in word_list if not i.startswith('http')]).strip()
    return sentence

def check_line(pattern, sentence):
    s = sentence.split('\t')
    try:
        if s[1] not in bot_users and not s[2].startswith('pinhook:'):
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
    for p in patterns:
        sentences = []
        filename = p
        pattern = patterns[p]
        for line in lines:
            line = regex.sub(b'', line)
            line = line.decode('UTF-8', errors='replace').replace('ACTION', '')
            sentence = check_line(pattern, line)
            if sentence:
                sentences.append(sentence)
        make_model(sentences, filename)

