from nltk.corpus import cmudict
import pinhook.plugin as p

d = cmudict.dict()

def nsyl(word):
    return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]

line_syls = {}
lines = {}

@p.listener('findku')
def findku(msg):
    global line_syls
    global lines

    cont = True
    syllables = []
    if msg.channel not in line_syls:
        line_syls[msg.channel] = []
    if msg.channel not in lines:
        lines[msg.channel] = []
    if len(lines[msg.channel]) > 2:
        lines[msg.channel].pop(0)
        line_syls[msg.channel].pop(0)
    for w in msg.text.split():
        try:
            syls = nsyl(w.strip('.,:()\'"'))
            syllables.append(syls[0])
        except:
            cont = False
    if cont:
        line_syls[msg.channel].append(sum(syllables))
        lines[msg.channel].append(msg.text)
        if line_syls[msg.channel] == [5, 7, 5]:
            msg.privmsg(msg.channel, 'haiku found: ' + ' / '.join(lines[msg.channel]))
    else:
        line_syls[msg.channel] = []
        lines[msg.channel] = []

@p.command('!findku', ops=True, ops_msg='finds bugs in findku')
def find_bug(msg):
    global line_syls
    global lines
    msg.logger.info(lines)
    msg.logger.info(line_syls)
