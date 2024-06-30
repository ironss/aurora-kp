#! /usr/bin/python3

import datetime
import os.path
import requests
import sys

import plasma_realtime


def download(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None

    return r.text


def fetch():
    text = download(plasma_realtime.url)
    measurements = plasma_realtime.parse(text)
    measurement = measurements[-1]

    t_now_dt = datetime.datetime.now(tz=datetime.timezone.utc)
    t_measurement_dt = measurement[0]
    measurement_age_s = (t_now_dt - t_measurement_dt).total_seconds()

    if measurement_age_s < 7.5*60:  # 7.5 minutes
        print("multigraph plasma_density")
        print("density.value  {:0.2f}".format(measurement[1]))

        print("multigraph plasma_speed")
        print("speed.value  {:0.2f}".format(measurement[2]))

        print("multigraph plasma_temperature")
        print("temperature.value  {:0.2f}".format(measurement[3]))
    else:
        print("multigraph plasma_density")
        print("density.value  U")

        print("multigraph plasma_speed")
        print("speed.value  U")

        print("multigraph plasma_temperature")
        print("temperature.value  U")


def config():
    print("host_name worldwide.place")

    print("multigraph plasma_density")
    print("graph_title Plasma density")
    print("graph_category astro")
    print("graph_vlabel Density (cm-3)")
#    print("graph_args --lower-limit 0 --upper-limit 100 --rigid")
    print("density.label Plasma density")
    print()

    print("multigraph plasma_speed")
    print("graph_title Plasma speed")
    print("graph_category astro")
    print("graph_vlabel Speed (m.s-1)")
#    print("graph_args --lower-limit 0 --upper-limit 100 --rigid")
    print("speed.label Plasma speed")
    print()

    print("multigraph plasma_temperature")
    print("graph_title Plasma temperature")
    print("graph_category astro")
    print("graph_vlabel Temperature (K)")
#    print("graph_args --lower-limit 0 --upper-limit 100 --rigid")
    print("temperature.label Plasma temperature")
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
