import re

from bs4 import BeautifulSoup
import requests
import pinhook.plugin as p

@p.listener('tube')
def tube(msg):
    match = re.match(r'.*((https:\/\/)?((hook|you)tube.com\/watch\?v=|youtu.be\/)[a-zA-z0-9\-_]+).*', msg.text)
    if match and not msg.text.startswith(('!supdate', '!sotd')):
        msg.logger.debug(match.group(1))
        r = requests.get('https://'+ match.group(1))
        s = BeautifulSoup(r.text, "html.parser")
        msg.logger.info(s)
        msg.logger.info(s.title)
        title = s.title.string
        msg.logger.info(title)
        out = '["{}"]'.format(title)
        return p.message(out)

