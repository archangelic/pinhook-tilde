import re

import pinhook.plugin as p

pattern = re.compile(r'(#?[\w-]*f+u+(cc|c+k|k|q)+[\w-]*)', re.IGNORECASE)
new_fucks = []

def check_fuck(fuck, unique_fucks):
    check = False
    if fuck not in unique_fucks and fuck not in new_fucks:
        check = True
    if 'brainfuck' in fuck.lower():
        check = False
    return check


@p.listener('newfuckdetector')
def fucklistener(msg):
    if msg.channel != '#tildetown':
        return None
    with open('/home/archangelic/public_html/unique_fucks.txt') as u:
        unique_fucks = [f.strip() for f in u.readlines()]
    results = pattern.findall(msg.text)
    new_u_f = []
    for r in results:
        fuck = r[0]
        if check_fuck(fuck, unique_fucks):
            new_u_f.append(fuck)
            new_fucks.append(fuck)
    if new_u_f:
        msg.logger.debug(new_u_f)
        return p.message(f'{msg.nick}: new fuck(s) detected: {", ".join(new_u_f)}')
    else:
        return None


