from zalgo import zalgo
import pinhook.plugin as p

#@p.register('!zalgo')
def zalgoize(msg):
    output = zalgo.zalgo(msg.arg, intensity=20)
    msg.logger.info(len(output))
    output = output.encode('utf-8', errors='replace')[:512].decode(errors='replace')
    msg.logger.info(len(output))
    msg.logger.info(len(output.encode('utf-8', errors='ignore')))
    return p.message(output)
