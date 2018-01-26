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


pattern = re.compile(r'(cryptocurrenc(ies|y)|bitcoin|ethereum|dogecoin|\bbtc\b|\beth\b|blockchain)', re.IGNORECASE)

with open('/home/archangelic/irc/log', 'rb') as i:
    lines = i.readlines()

regex = re.compile(b"\x01|\x1f|\x02|\x12|\x0f|\x16|\x03(?:\d{1,2}(?:,\d{1,2})?)?")
cryptotalk = []
for line in lines:
    line = regex.sub(b'', line)
    line = line.decode('UTF-8', errors='replace').replace('ACTION', '')
    if pattern.search(line):
        s = line.split('\t')
        if s[1] != 'cosnok' and s[1] != 'pinhook' and not s[2].startswith('pinhook:'):
            cryptotalk.append(s[2].strip())
            print(s[2].strip())

corpus = ''.join([c + '\n' for c in cryptotalk])

text_model = POSifiedText(corpus)
model_json = text_model.to_json()
with open(os.path.join('plugins', 'btc.json'), 'w') as j:
    json.dump(model_json, j)

