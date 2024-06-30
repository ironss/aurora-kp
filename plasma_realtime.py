# Process 3-day Kp forecast


import datetime
import json
import re

url = 'https://services.swpc.noaa.gov/products/solar-wind/plasma-5-minute.json'


def parse(text):
    data = json.loads(text)
    values = []
    for tt_str, density_str, speed_str, temperature_str in data[1:]:
        tt = datetime.datetime.strptime(tt_str[:-4] + '+0000', "%Y-%m-%d %H:%M:%S%z")
        density = float(density_str)
        speed = float(speed_str)
        temperature = float(temperature_str)

        values.append((tt, density, speed, temperature))
    return values


if __name__ == '__main__':
    import requests

    r = requests.get(url)
    values = parse(r.text)
    print(values)
