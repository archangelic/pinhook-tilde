#!/usr/bin/env python3

import pinhook.plugin
import random
# Example usage
# Input: !confetti
# Meaning: Output some confetti emoji

@pinhook.plugin.register('!confetti', help_text='string of confetti')
def confetti(msg):
    message = u'\U0001F389\U0001F389\U0001F389\U0001F389\U0001F389\U0001F389\U0001F389\U0001F38A\U0001F389\U0001F389\U0001F389\U0001F38A\U0001F389\U0001F38A\U0001F389\U0001F38A\U0001F389\U0001F38A'
    return pinhook.plugin.message(''.join(random.sample(message,len(message))))
