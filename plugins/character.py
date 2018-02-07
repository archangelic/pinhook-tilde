from random import choice

import pinhook.plugin as p

lvl = [n for n in range(1,21)]
align_lc = [
    'Lawful',
    'Neutral',
    'Chaotic',
]
align_ge = [
    'Good',
    'Neutral',
    'Evil'
]
race = [
    'Dwarf',
    'Elf',
    'Halfling',
    'Human',
    'Dragonborn',
    'Gnome',
    'Half-Elf',
    'Half-Orc',
    'Tiefling'
]
cls = [
    'Barbarian',
    'Bard',
    'Cleric',
    'Fighter',
    'Monk',
    'Rogue',
    'Sorcerer',
    'Warlock',
    'Wizard'
]

def get_alignment():
    lc = choice(align_lc)
    ge = choice(align_ge)
    if lc == ge:
        return 'Neutral'
    else:
        return lc + '-' + ge

@p.listener('character')
def character(msg):
    if 'roll a character' in msg.text.lower():
        alignment = get_alignment()
        out = '{} {} {}'.format(alignment, choice(race), choice(cls))
        return p.message(out)
