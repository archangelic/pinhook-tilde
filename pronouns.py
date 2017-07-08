import json
from os import listdir

if 'pronouns.json' not in listdir():
    pronouns = {}
    with open('pronouns.json', 'w') as f:
        json.dump(pronouns, f)

with open('pronouns.json') as f:
    pronouns = json.load(f)

def my_pronouns(user, p):
    pronouns[user] = p
    with open('pronouns.json', 'w') as f:
        json.dump(pronouns, f)
    return '{}: Your pronouns have been saved'.format(user)

def get_pronouns(user):
    if user in pronouns:
        msg = 'Pronouns for {}: {}'.format(user, pronouns[user])
    else:
        msg = '{} has not declared any pronouns'.format(user)
    return msg
