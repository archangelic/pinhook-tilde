import time

import pinhook.plugin

def beats(b='swatch'):
    t = time.gmtime()
    h, m, s = t.tm_hour, t.tm_min, t.tm_sec

    utc = 3600 * h + 60 * m + s  # UTC
    if b == 'swatch':
        bmt = utc + 3600  # Biel Mean Time (BMT)
    elif b == 'tilde':
        bmt = utc

    beat = bmt / 86.4

    if beat > 1000:
        beat -= 1000

    return beat


@pinhook.plugin.register('!beat')
@pinhook.plugin.register('!beats')
def swatch(msg):
    return pinhook.plugin.message('@%06.2f' % (beats()))

@pinhook.plugin.register('!ttocks')
@pinhook.plugin.register('!tocks')
def tildetocks(msg):
    return pinhook.plugin.message('@%06.2f' % (beats('tilde')))

