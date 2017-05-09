from datetime import datetime, timedelta
import json

def run(nick):
    try:
        with open('/home/{}/.botany/{}_plant_data.json'.format(nick, nick)) as plant_json:
            plant = json.load(plant_json)
        
        last_watered = datetime.utcfromtimestamp(plant['last_watered'])
        water_diff = datetime.now() - last_watered

        if plant['is_dead'] or water_diff.days >= 5:
            return '{}: Your plant is dead'.format(nick)
        elif water_diff.days == 0:
            hours = str(round(water_diff.seconds / 3600))
            water_time = ''
            if hours == '0':
                water_time = str(round(water_diff.seconds/60)) + ' minutes'
            elif hours == '1':
                water_time = '1 hour'
            else:
                water_time = hours + ' hours'
            msg = '{}: Good job! You watered your plant today! (About {} ago)'.format(nick, water_time)
            return msg
        elif 1 <= water_diff.days:
            days = str(water_diff.days)
            w_days = ''
            if days == '1':
                w_days = '1 day'
            else:
                w_days = days + ' days'
            hours = str(round(water_diff.seconds / 3600))
            w_hours = ''
            if hours == '1':
                w_hours = '1 hour'
            else:
                w_hours = hours + ' hours'
            msg = "{}: You haven't watered your plant today! (Last watered about {} and {} ago)".format(nick, w_days, w_hours)
            return msg
    except FileNotFoundError:
        return 'Are you sure you have a plant in our beautiful garden?'

