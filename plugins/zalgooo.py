from zalgo import zalgo
import pinhook.plugin as p

@p.register('!zalgo')
def zalgoize(msg):
    return p.message(zalgo.zalgo(msg.arg, intensity=20))
