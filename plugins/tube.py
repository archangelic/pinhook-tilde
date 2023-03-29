import re

import pinhook.plugin as p
import yt_dlp

yt_opts = {'quiet': True, 'no_warnings': True}

@p.listener('tube')
def tube(msg):
    match = re.match(r'.*((https:\/\/)?((hook|you)tube.com\/watch\?v=|youtu.be\/)[a-zA-z0-9\-_]+).*', msg.text)
    if match and not msg.text.startswith('!'):
        with yt_dlp.YoutubeDL(yt_opts) as ydl:
            info = ydl.extract_info(f'https://{match.group(1)}', download=False)
            title = ydl.sanitize_info(info)['title']
        return p.message(f'["{title}"]')
