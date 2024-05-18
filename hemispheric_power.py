#! /usr/bin/python3

import datetime
import os.path
import requests
import sys

import hemispheric_power_forecast


def download(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None

    return r.text


def fetch():
    text = download(hemispheric_power_forecast.url)
    power_forecasts = hemispheric_power_forecast.parse(text)

    print("power_N.value {:0.2f}".format(power_forecasts[-1][2]))
    print("power_S.value {:0.2f}".format(power_forecasts[-1][3]))


def config():
    print("host_name worldwide.place")
    print("graph_title Hemispheric power index")
    print("graph_category astro")
    print("graph_vlabel Power index (GW)")
    print("graph_args --lower-limit 0 --upper-limit 100 --rigid")
    print("power_N.label HPI North")
    print("power_S.label HPI North")
    #print("kp_forecast.line 7")


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
