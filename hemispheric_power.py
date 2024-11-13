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
    forecast = power_forecasts[-1]

    t_now_dt = datetime.datetime.now(tz=datetime.timezone.utc)
    t_forecast_dt = forecast[0]
    forecast_age_s = (t_now_dt - t_forecast_dt).total_seconds()

    if forecast_age_s < 7.5*60:  # 7.5 minutes
        print("power_N.value {:0.2f}".format(forecast[2]))
        print("power_S.value {:0.2f}".format(forecast[3]))
    else:
        print("power_N.value U")
        print("power_S.value U")


def config():
    print("host_name worldwide.place")
    print("graph_title Hemispheric power index forecast")
    print("graph_category astro")
    print("graph_vlabel Power index (GW)")
    print("graph_args --lower-limit 0 --upper-limit 100 --rigid")
    print("power_N.label HPI North")
    print("power_S.label HPI South")
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
