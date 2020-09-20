from datetime import datetime, timedelta
import json
import random
import time

import pinhook.plugin

verbs = [
    'wriggles slightly',
    'sighs cutely',
    'wriggles',
    'smiles',
]


@pinhook.plugin.command('!botany', help_text='look up a plant to see if it has been watered (yourself by default)')
def run(msg):
    who = msg.nick
    if msg.arg:
        nick = msg.arg
    else:
        nick = msg.nick

    if who == nick:
        greeting = '{}: Your'.format(who)
    else:
        greeting = '{}: {}\'s'.format(who, nick)
    try:
        with open('/home/{}/.botany/{}_plant_data.json'.format(nick, nick)) as plant_json:
            plant = json.load(plant_json)
    except FileNotFoundError:
        return pinhook.plugin.message('{}: Are you sure {} has a plant in our beautiful garden?'.format(who, nick))
    try:
        with open('/home/{}/.botany/visitors.json'.format(nick)) as visitors_json:
            visitors = json.load(visitors_json)
        if visitors:
            last_visit = visitors[-1]['timestamp']
            visitor = visitors[-1]['user']
        else:
            last_visit = 0
            visitor = ''
    except FileNotFoundError:
        last_visit = 0
        visitor = ''

    if last_visit > plant['last_watered']:
        last_watered = last_visit
    else:
        last_watered = plant['last_watered']
        visitor = nick

    last_watered = datetime.utcfromtimestamp(last_watered)

    water_diff = datetime.now() - last_watered

    if plant['is_dead'] or water_diff.days >= 5:
        condolences = ['RIP', 'Press F to Pay Respects']
        return pinhook.plugin.message('{} {} is dead. {}'.format(greeting, plant['description'], random.choice(condolences)))
    elif water_diff.days == 0:
        hours = str(round(water_diff.seconds / 3600))
        water_time = ''
        if hours == '0':
            water_time = str(round(water_diff.seconds / 60)) + ' minutes'
        elif hours == '1':
            water_time = '1 hour'
        else:
            water_time = hours + ' hours'
        msg = '{} {} was watered today! (About {} ago by {})'.format(
            greeting, plant['description'], water_time, visitor)
        return pinhook.plugin.message(msg)
    elif 1 <= water_diff.days:
        days = str(water_diff.days)
        w_days = ''
        if days == '1':
            w_days = '1 day'
        else:
            w_days = days + ' days'
        hours = str(round(water_diff.seconds / 3600))
        w_hours = ''
        if hours == '0':
            w_hours = ''
        elif hours == '1':
            w_hours = ' and 1 hour'
        else:
            w_hours = ' and {} hours'.format(hours)
        msg = "{} {} hasn't been watered today! (Last watered about {}{} ago by {})".format(
            greeting, plant['description'], w_days, w_hours, visitor)
        return pinhook.plugin.message(msg)

@pinhook.plugin.command('!water', help_text='water a plant (yours by default)')
def water(msg):
    if msg.arg == msg.botnick:
        return pinhook.plugin.action(random.choice(verbs))
    elif msg.arg == "gamebot":
        return None
    elif not msg.arg:
        nick = msg.nick
    else:
        nick = msg.arg

    try:
        filename = '/home/{}/.botany/visitors.json'.format(nick)
        with open(filename) as v:
            visitors = json.load(v)
        visitors.append({'timestamp': int(time.time()), 'user': 'pinhook'})
        with open(filename, 'w') as v:
            json.dump(visitors, v, indent=2)
        with open('/home/{}/.botany/{}_plant_data.json'.format(nick, nick)) as plant_json:
            desc = json.load(plant_json)['description']
        return pinhook.plugin.action("waters {}'s {}".format(nick, desc))
    except Exception as e:
        msg.logger.error(e)
        return pinhook.plugin.message("{}: could not find plant for {}".format(msg.nick, nick))
