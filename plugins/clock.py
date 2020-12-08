import math
import json
import time

from pinhook import plugin as p

with open('emojis.json', 'r', encoding='utf-8') as e:
    emojis = json.load(e)

emojis = sorted(emojis.items(), key=lambda x: x[0])

emoji_list = {}
c = 0
for k,v in emojis:
    emoji_list[str(c)] = v
    c += 1

@p.command('!emojitime')
def emojitime(msg):
    e_len = len(emoji_list)
    now = int(time.time() * 100)
    s = math.floor(now % e_len)
    s = emoji_list[str(s)]

    m = math.floor((now % e_len**2)/e_len)
    m = emoji_list[str(m)]

    h = math.floor((now % e_len**3)/e_len**2)
    h = emoji_list[str(h)]
    return p.message(u':'.join([h,m,s]))
