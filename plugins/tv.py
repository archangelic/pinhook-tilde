from datetime import datetime
import os

from configobj import ConfigObj
from tvdb_api import Tvdb, tvdb_shownotfound

cmds = {
    '!tv': "Tells you the next air date for shows you look up.",
    '!tvalias': "Adds an alias to quickly search for shows"
}
t = Tvdb()
conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tv.conf')
config = ConfigObj(conf_file)
aliases = config["aliases"]


def get_datekey(date):
    dkey = "%Y-%m-%d"
    datekey = datetime.strptime(date, dkey).strftime("%Y%m%d")
    datekey = int(datekey)
    return datekey


def remove_bad_dates(show):
    eps = {}
    datelist = []
    if len(show) == 1:
        for e in range(len(show[1])):
            e += 1
            if show[1][e]['firstaired']:
                datekey = get_datekey(show[1][e]['firstaired'])
                eps[datekey] = (1, e)
                datelist.append(datekey)
    elif len(show) > 1:
        for s in range(len(show) + 1):
            s += 1
            try:
                for e in range(len(show[s])):
                    e += 1
                    if show[s][e]['firstaired']:
                        datekey = get_datekey(show[s][e]['firstaired'])
                        eps[datekey] = (s, e)
                        datelist.append(datekey)
            except:
                pass
    datelist.sort()
    return (eps, datelist)


def next_ep(show, eps, datelist, today):
    scenario = 0
    for t in range(0, len(datelist)):
        if t != len(datelist) - 1:
            if datelist[t] > today:
                future = True
            else:
                future = False
            prev = datelist[t - 1] - today
            if prev > 0:
                prev_ep_in_future = True
            else:
                prev_ep_in_future = False
        if t == len(datelist) - 1:
            if datelist[t] > today:
                future = True
            else:
                future = False
            prev_ep_in_future = False

        if future and not prev_ep_in_future:
            s, e = eps[datelist[t]]
            scenario = 1
            break
        elif datelist[t] == today:
            s, e = eps[datelist[t]]
            scenario = 2
            break
        elif not future and not prev_ep_in_future:
            s, e = eps[datelist[t]]
            scenario = 3
    return s, e, scenario


def ep_marker(show, s, e):
    ep = show[s][e]
    if int(ep['seasonnumber']) < 10:
        snum = '0' + ep['seasonnumber']
    else:
        snum = ep['seasonnumber']
    if int(ep['episodenumber']) < 10:
        enum = '0' + ep['episodenumber']
    else:
        enum = ep['episodenumber']
    return 'S' + snum + 'E' + enum


def modify_alias(text):
    try:
        key, alias = text.split("=>")
        key = key.strip().lower()
        alias = alias.strip().lower()
    except:
        return("An error occurred adding alias")
    if key in aliases:
        aliases[key] = alias
        config.write()
        return("Successfully modified alias")
    else:
        aliases[key] = alias
        config.write()
        return("Successfully added alias")


def build_string(show, s, e, scen):
    ep = show[s][e]
    d = ep['firstaired']
    airdate = datetime.strptime(d, "%Y-%m-%d").strftime("%A, %m-%d-%Y")
    oldair = datetime.strptime(d, "%Y-%m-%d").strftime("%m-%d-%Y")
    status = show['status']
    sname = show['seriesname']
    airtime = show['airs_time']
    network = show['network']
    ename = ' "' + ep['episodename'] + '"'
    epmarker = ep_marker(show, s, e)
    if ep['imdb_id']:
        imdb = "http://www.imdb.com/title/" + ep['imdb_id'] + "/"
    else:
        imdb = "http://www.imdb.com/title/" + show['imdb_id'] + "/"

    if scen == 1:
        showstring = (sname + ' - Next Episode: ' + epmarker + ename +
                      ' - Airs: ' + airdate + ' at ' + airtime +
                      ' on ' + network + " - " + imdb)
    elif scen == 2:
        showstring = (sname + ' - Next Episode: ' + epmarker + ename +
                      ' - Airs: Today, ' + airdate + ' at ' + airtime +
                      ' on ' + network + " - " + imdb)
    elif scen == 3:
        if status == 'Ended':
            showstring = (sname + ' - Last Aired: ' + oldair +
                          ' - Show has ended')
        else:
            showstring = (sname + ' - Last Aired: ' + epmarker + ename + " on " + airdate +
                          ' - No new air dates have been announced')
    else:
        showstring = "There was an error."
    return showstring


def next_up(text):
    message = ''
    try:
        if text.lower() in aliases:
            stext = aliases[text.lower()]
        else:
            stext = text
        show = t[stext]
        sname = show['seriesname']
        today = int(datetime.now().strftime("%Y%m%d"))
        eps, datelist = remove_bad_dates(show)
        s, e, scenario = next_ep(show, eps, datelist, today)
        showstring = build_string(show, s, e, scenario)
        message = showstring
    except tvdb_shownotfound:
        message = 'Cannot find show "' + text + '"'
    except:
        message = "An error occured."
    return message


def alias_show(text):
    return modify_alias(text)
