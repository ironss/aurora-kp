#! /usr/bin/python3

import datetime
import os.path
import requests
import sys

import solar_wind_realtime


def download(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None

    return r.text


def fetch():
    text = download(solar_wind_realtime.url)
    measurements = solar_wind_realtime.parse(text)
    measurement = measurements[-1]

    t_now_dt = datetime.datetime.now(tz=datetime.timezone.utc)
    t_measurement_dt = measurement[0]
    measurement_age_s = (t_now_dt - t_measurement_dt).total_seconds()

    if measurement_age_s < 7.5*60:  # 7.5 minutes
        print("bx_gsm.value  {:0.2f}".format(measurement[1]))
        print("by_gsm.value  {:0.2f}".format(measurement[2]))
        print("bz_gsm.value  {:0.2f}".format(measurement[3]))
        print("lon_gsm.value {:0.2f}".format(measurement[4]))
        print("lat_gsm.value {:0.2f}".format(measurement[5]))
        print("bt_gsm.value  {:0.2f}".format(measurement[6]))
    else:
        print("bx_gsm.value  U")
        print("by_gsm.value  U")
        print("bz_gsm.value  U")
        print("lon_gsm.value U")
        print("lat_gsm.value U")
        print("bt_gsm.value  U")


def config():
    print("host_name worldwide.place")
    print()
    print("graph_title Magnetic field")
    print("graph_category astro")
    print("graph_vlabel Field stength (nT)")
    print("graph_args --lower-limit 0 --upper-limit 100 --rigid")
    print("bx_gsm.label Bx")
    print("by_gsm.label By")
    print("bz_gsm.label Bz")
    print("bt_gsm.label Bt")
    print()


if len(sys.argv) > 1:
    cmd = sys.argv[1]
    if cmd == 'config':
        config()
        if True:  # if we support dirtyconfig
            fetch()
        sys.exit(0)

    if cmd == 'suggest':
        sys.exit(0)

    verboselog('unknown argument "{}"'.format(cmd))
    exit(1)

fetch()
