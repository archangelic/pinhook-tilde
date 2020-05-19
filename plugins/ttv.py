import json

import pinhook.plugin as p

@p.command('!ttv', help_text='output tilde tv stuff')
def ttv(msg):
    with open('/home/karlen/public_html/tv/videos.json') as tv:
        vids = json.load(tv)
    videos = ''
    for vid in vids:
        videos += '~{}: {} <{}>\n'.format(vid['user'], vid['title'], vid['youtubelink'])
    return p.message(videos.strip())
