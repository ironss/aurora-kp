# Utilities for weather forecast handling
#
# service
# location is a dict with keys name, lat, lon, alt, used to replace fields in the URL, URL params and headers
# secrets is a dict with arbitrary keys that are used to replace fields in the URL, URL params and headers

import collections
import datetime
import requests


Weather_report = collections.namedtuple('Weather_report', [
    'time_dt',
    'summary',
    'code',
    'icon',
    'temperature_C',
    'pressure_hPa',
    'wind_speed_m_s',
    'wind_gust_m_s',
    'wind_direction_deg',
    'wind_vector_E',
    'wind_vector_N',
    'rain',
    'rain_1h_mm',
    'rain_3h_mm',
    'rain_24h_mm',
    'relative_humidity_pc',
    'cloud_cover_pc',
    'visibility_m',
])


def _load_report(service, location, secrets):
    params = { k: v.format(**location, **secrets) for k, v in service['url_params'].items() }
    headers = { k: v.format(**location, **secrets) for k, v in service['url_headers'].items() }
    url = service['url_base'].format(**location, **secrets)
    
    req = requests.get(url, headers=headers, params=params)
    return req.text

def load_report(service, location, secrets):
    report_text = _load_report(service, location, secrets)
    report = service['handler'](report_text)
    return report


if __name__ == '__main__':
    import json
    import openweathermap
    import weatherkit

    secrets_fn = 'secrets.json'
    with open(secrets_fn) as f:
        secrets = json.load(f)
        
    locations = [
        ( 'Christchurch, NZ'       , -43.4821,  172.5500,   37),
        #( 'Lyttelton, NZ'          , -43.6000,  172.7200,    0),
        #( 'Nelson, NZ'             , -41.2980,  173.2210,    5),
        #( 'Scott Base, NZ'         , -77.8491,  166.7682,   10),
        #( 'SANAE IV, ZA'           , -71.6724,   -2.8249,  850),
        #( 'Wichita, KA, US'        ,  37.6889,  -97.3361,  400),
        #( 'Amundsen-Scott Base, US', -90.0000,    0.0000, 2835),
    ]

    for location in locations:
        location_dict = { k: location[i] for i, k in enumerate(['name', 'lat', 'lon', 'alt']) }
        print(location)
        
        report = load_report(openweathermap.service, location_dict, secrets['openweathermap'])
        print(report)
        print()
       
        report = load_report(weatherkit.service, location_dict, secrets['weatherkit'])
        print(report)
        print()

