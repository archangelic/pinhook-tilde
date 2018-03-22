import json
import os
import re

import markovify
import nltk

class POSifiedText(markovify.NewlineText):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [w for w in words if len(w) > 0]
        words = ["::".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

def make_sentence(sentence):
    word_list = sentence.split()
    if word_list[0].endswith(':'):
        word_list.pop(0)
    if word_list[0].startswith('!'):
        word_list = []
    sentence = ''.join([i + ' ' for i in word_list if not i.startswith('http')]).strip()
    return sentence


pattern = re.compile(r'(cryptocurrenc(ies|y)|bitcoin|ethereum|dogecoin|\bbtc\b|\beth\b|blockchain)', re.IGNORECASE)

with open('/home/archangelic/irc/log', 'rb') as i:
    lines = i.readlines()

bad_users = ['cosnok', 'pinhook', 'quote_bot']
regex = re.compile(b"\x01|\x1f|\x02|\x12|\x0f|\x16|\x03(?:\d{1,2}(?:,\d{1,2})?)?")
cryptotalk = []
for line in lines:
    line = regex.sub(b'', line)
    line = line.decode('UTF-8', errors='replace').replace('ACTION', '')
    if pattern.search(line):
        s = line.split('\t')
        if s[1] not in bad_users and not s[2].startswith('pinhook:'):
            sentence = make_sentence(s[2])
            if sentence:
                cryptotalk.append(sentence)
                print(sentence)

corpus = ''.join([c + '\n' for c in cryptotalk])

text_model = POSifiedText(corpus)
model_json = text_model.to_json()
with open(os.path.join('plugins', 'btc.json'), 'w') as j:
    json.dump(model_json, j)

