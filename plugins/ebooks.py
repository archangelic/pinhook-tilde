import random

commands = ['!doctorow']

def doctorow():
    with open('doctorow_ebooks.txt', 'r') as ebooks:
        lines = ebooks.read().split('\n')
        quotes = [line for line in lines if line]
    return ('message', random.choice(quotes))

def cyber():
    with open('cyber_ebooks.txt', 'r') as ebooks:
        lines = ebooks.read().split('\n')
        quotes = [line for line in lines if line]
    return random.choice(quotes)

def run(**kwargs):
    return doctorow()
