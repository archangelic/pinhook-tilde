import json
from os import path

import markovify
import nltk
import pinhook.plugin as p

class POSifiedText(markovify.NewlineText):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [w for w in words if len(w) > 0]
        words = ["::".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

@p.listener('bitcoin')
def bitcoin(msg):
    if msg.text.lower() == msg.botnick + ': how do you feel about bitcoin?':
        with open(path.join(path.dirname(path.abspath(__file__)), 'btc.json'), 'r') as b:
                text = json.load(b)
        text_model = POSifiedText.from_json(text)
        return p.message(text_model.make_sentence())
