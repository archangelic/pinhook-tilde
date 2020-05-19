import json
from os import listdir, path

import pinhook.plugin

json_file = path.join(path.dirname(path.abspath(__file__)), 'pronouns.json')

if 'pronouns.json' not in listdir(path.dirname(path.abspath(__file__))):
    pronouns = {}
    with open(json_file, 'w') as f:
        json.dump(pronouns, f)

with open(json_file) as f:
    pronouns = json.load(f)

def get_dot_files():
    dot_pronouns = {}
    homedirs = [user for user in listdir('/home') if path.isdir(path.join('/home', user))]
    for user in homedirs:
        dot_file = path.join('/home', user, '.pronouns')
        if path.exists(dot_file):
            with open(dot_file) as d:
                dot_pronouns[user] = d.read().strip().replace('\n', '/')
        else:
            dot_pronouns[user] = ''
    return dot_pronouns

def my_pronouns(user, p):
    if user in get_dot_files():
        return pinhook.plugin.message("{}: Please use `echo '{}' > ~/.pronouns` to set your pronouns".format(user, p))
    else:
        pronouns[user] = p
        with open(json_file, 'w') as j:
            json.dump(pronouns, j)
        return pinhook.plugin.message('{}: your pronouns have been set to "{}"'.format(user,p))

def get_pronouns(user):
    dot_pronouns = get_dot_files()
    if user in dot_pronouns:
        if dot_pronouns[user]:
            is_dot_user = True
        else:
            is_dot_user = False
    else:
        is_dot_user = False
    if is_dot_user:
        msg = 'Pronouns for {}: {}'.format(user, dot_pronouns[user])
    elif user in pronouns:
        msg = 'Pronouns for {}: {}'.format(user, pronouns[user])
    elif user == '':
        msg = "Please enter a valid user, or use `echo '<pronouns here>' > ~/.pronouns` to declare your pronouns"
    else:
        msg = "{} has not declared any pronouns. Use `echo '<pronouns here>' > ~/.pronouns` to add your pronouns!".format(user)
    return pinhook.plugin.message(msg)

@pinhook.plugin.command('!pronouns', help_text='list pronouns for a user (yourself by default)')
@pinhook.plugin.command('!mypronouns', help_text='deprecated method to set pronouns')
def run(msg):
    if msg.cmd == '!pronouns':
        if not msg.arg:
            msg.arg = msg.nick
        return get_pronouns(msg.arg)
    elif msg.cmd == '!mypronouns':
        if msg.arg:
            return my_pronouns(msg.nick, msg.arg)
        else:
            return get_pronouns(msg.nick)

