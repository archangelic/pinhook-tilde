import pinhook.plugin as p

@p.command('!hotlines', help_text='suicide hotlines')
def hotlines(msg):
    output = [
        'National Suicide Prevention Lifeline (US): 1-800-273-8255',
        'Trans Lifeline: (US) 1-877-565-8860, (Canada) 1-877-330-6366',
    ]
    output = ''.join([i + '\n' for i in output]).strip()
    return p.message(output)
