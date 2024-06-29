# Process 3-day Kp forecast


import datetime
import json
import re

url = 'https://services.swpc.noaa.gov/products/solar-wind/mag-5-minute.json'


def parse(text):
    data = json.loads(text)
    values = []
    for tt_str, bx_str, by_str, bz_str, lon_str, lat_str, bt_str in data[1:]:
        tt = datetime.datetime.strptime(tt_str[:-4] + '+0000', "%Y-%m-%d %H:%M:%S%z")
        bx = float(bx_str)
        by = float(by_str)
        bz = float(bz_str)
        lon = float(lon_str)
        lat = float(lat_str)
        bt = float(bt_str)

        values.append((tt, bx, by, bz, lon, lat, bt))
    return values


if __name__ == '__main__':
    import requests

    r = requests.get(url)
    values = parse(r.text)
    print(values)
