"""
"""

import datetime
import re

url = 'https://services.swpc.noaa.gov/text/3-day-forecast.txt'

month_number = {
    'Jan': 1, 
    'Feb': 2, 
    'Mar': 3, 
    'Apr': 4, 
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12,
}


def parse(text):
    kp_table_re = re.compile('NOAA Kp index breakdown ([^ ]+) ([^-]+)-([^ ]+) ([^ ]+) (\S+)\s')
    matches = kp_table_re.search(text)

    month_str, day_str, _, _, year_str = matches.groups()
    year = int(year_str)
    month = month_number[month_str]
    day = int(day_str)
    
    table_start_pos = matches.end()
    table = text[table_start_pos:table_start_pos+500]
    lines = table.split('\n')
    
    kp_forecasts = []
    for l in lines[2:-2]:
        hour = int(l[0:2])
        v1 = float(l[14:18])
        g1 = l[20:22]
        v2 = float(l[27:31])
        g2 = l[33:35]
        v3 = float(l[40:44])
        g3 = l[46:48]
        
        dt1 = datetime.datetime(year, month, day, hour, tzinfo=datetime.timezone.utc)
        dt2 = dt1 + datetime.timedelta(days=1)
        dt3 = dt2 + datetime.timedelta(days=1)

        kp_forecasts.append((dt1, v1, g1))
        kp_forecasts.append((dt2, v2, g2))
        kp_forecasts.append((dt3, v3, g3))

    kp_forecasts = { f[0]: ( f[1], f[2]) for f in kp_forecasts }
    
    return kp_forecasts


if __name__ == '__main__':
    import requests
    import zoneinfo

    r = requests.get(url)
    kp_forecasts = parse(r.text)

    for dt, f in kp_forecasts.items():
        print(dt, f[0], f[1])

