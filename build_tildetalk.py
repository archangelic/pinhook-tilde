#!/usr/bin/env python3
import json
from os import chmod, path, listdir
import re
import shlex
import string
import subprocess
import traceback

import markovify
import nltk

valid_chars = string.ascii_letters + string.digits
valid_chars = tuple([i for i in valid_chars])

cosnok_pattern = re.compile(r'^\[\".*\"\]$')
demoji_pattern = re.compile(r'^<.+>.*:[\w\d_]+:')

class POSifiedText(markovify.NewlineText):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [w for w in words if len(w) > 0]
        words = [":-:".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split(":-:")[0] for word in words)
        return sentence


def make_sentence(word_list):
    if word_list[0].endswith(':'):
        word_list.pop(0)
    elif word_list[0].startswith('!'):
        word_list = []
    sentence = ''.join([i + ' ' for i in word_list if not i.startswith('http')]).strip()
    if user == 'cosnok':
        sentence = sentence.strip('"[]')
    return sentence


def make_user_file(user, sentences):
    with open(path.join('users', user), 'w') as userfile:
        for sentence in sentences:
            userfile.write(sentence + '\n')
    chmod(path.join('users', user), 0o600)


def convert_to_json(user):
    with open(path.join('users', user)) as f:
        text = f.read()
    text_model = POSifiedText(text)
    model_json = text_model.to_json()
    with open(path.join('json', user), 'w') as juser:
        json.dump(model_json, juser)
    chmod(path.join('json', user), 0o600)

def user_changed(user, sentences):
    usertext = ''.join([s + '\n' for s in sentences])
    try:
        if user and user in listdir('users'):
            with open(path.join('users', user)) as f:
                text = f.read()
            if usertext != text:
                return True
        elif user:
            return True
    except:
        pass


with open('/home/archangelic/irc/log', 'rb') as log:
    regex = re.compile(b"\x01|\x1f|\x02|\x12|\x0f|\x16|\x03(?:\d{1,2}(?:,\d{1,2})?)?")
    log = regex.sub(b'', log.read())
    log = log.decode('UTF-8', errors='replace')
    log = log.replace('ACTION', '')

with open('/home/archangelic/wallflower/nick_merge.json') as c:
    canon = json.load(c)

last_line = ''
text_dict = {}
for line in log.split('\n'):
    try:
        user = line.split()[1]
        if user in canon:
            user = canon[user]
        if user == 'archangelic' and last_line.startswith('!'):
            user = 'pinhook'
        sentence = make_sentence(line.split()[2:])
        if user == 'archangelic' and demoji_pattern.match(sentence):
            user = 'demoji'
        if not user in text_dict and sentence:
            text_dict[user] = [sentence]
        elif sentence:
            text_dict[user].append(sentence)
        if cosnok_pattern.match(sentence):
            if 'cosnok' not in text_dict:
                text_dict['cosnok'] = [sentence]
            else:
                text_dict['cosnok'].append(sentence)
        last_line = sentence
    except IndexError:
        continue

changed_users = []
for entry in text_dict:
    valid = re.match('^[\w-]+$', entry)
    if valid and user_changed(entry, text_dict[entry]):
        changed_users.append(entry)
    if entry in changed_users:
        make_user_file(entry, text_dict[entry])

for user in listdir('users'):
    try:
        if user in changed_users:
            convert_to_json(user)
    except:
        print(user)
        traceback.print_exc()
        continue
