import time
import json

from pinhook import plugin as p

with open('emojis.json', 'r', encoding='utf-8') as e:
    emojis = json.load(e)

emoji_list = {}
c = 0
for k,v in emojis.items():
    emoji_list[str(c)] = v
    c += 1

def check_emoji(num):
    num = int(num.lstrip('0'))
    if num > len(emoji_list):
        num = int(num)//10
    return emoji_list[str(num)]

@p.command('!emojitime')
def emojitime(msg):
    code = str(int(time.time() * 100))
    h = check_emoji(code[:4])
    m = check_emoji(code[4:8])
    s = check_emoji(code[8:])
    return p.message(u':'.join([h,m,s]))
