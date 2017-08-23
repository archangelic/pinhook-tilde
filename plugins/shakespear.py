import json
import random
from os import listdir, path
import re

import markovify
import nltk

json_file = path.join(path.dirname(path.abspath(__file__)), 'shakespear.json')

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [w for w in words if len(w) > 0]
        words = ["::".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


def get_sentence():
    with open(json_file) as f:
        text = json.load(f)
    text_model = POSifiedText.from_json(text)
    return text_model.make_sentence()

