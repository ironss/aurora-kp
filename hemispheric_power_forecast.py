# Process 3-day Kp forecast


import datetime
import re

url = 'https://services.swpc.noaa.gov/text/aurora-nowcast-hemi-power.txt'

re_str = '(\S+)\s+(\S+)\s+(\S+)\s+(\S+)'
parse_re = re.compile(re_str)

def parse(text):
    forecasts = []

    text += '\n'
    lines = text.split('\n')
    for l in lines:
        if not l or l[0] == '#':
            continue

        matches = parse_re.match(l)

        try:
            date_model = datetime.datetime.strptime(matches.group(1), '%Y-%m-%d_%H:%M').replace(tzinfo=datetime.timezone.utc)
        except ValueError:
            continue

        try:
            date_forecast = datetime.datetime.strptime(matches.group(1), '%Y-%m-%d_%H:%M').replace(tzinfo=datetime.timezone.utc)
        except ValueError:
            continue

        try:
            power_N = int(matches.group(3))
        except ValueError:
            continue

        try:
            power_S = int(matches.group(4))
        except ValueError:
            continue

        forecast = (date_model, date_forecast, power_N, power_S)
        forecasts.append(forecast)

    return forecasts


if __name__ == '__main__':
    import requests

    r = requests.get(url)
    power_forecasts = parse(r.text)
    print(power_forecasts)

    for dt_model, dt_forecast, power_N, power_S in power_forecasts:
        print(dt_model, dt_forecast, power_N, power_S)
