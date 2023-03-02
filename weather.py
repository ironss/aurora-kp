"""
Utilities for weather forecast handling
"""

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
    'wind_direction_deg',
    'wind_vector_E',
    'wind_vector_N',
    'precipitation_mm',
    'relative_humidity_pc',
    'cloud_cover_pc',
    'visibility_m',
])


def load_report(service, location, secrets):
    location_dict = service['location'](location)
    params = { k: v.format(**location_dict, **secrets) for k, v in service['url_params'].items() }
    headers = { k: v.format(**location_dict, **secrets) for k, v in service['url_headers'].items() }
    url = service['url_base'].format(**location_dict, **secrets)
    
    req = requests.get(url, headers=headers, params=params)
    report = service['handler'](req.text)
    return report


if __name__ == '__main__':
    import json
    import openweathermap

    secrets_fn = 'secrets.json'
    with open(secrets_fn) as f:
        secrets = json.load(f)
        
    location = ( 'Christchurch Airport', -43.4821, 172.5500, 30 )
    
    report = load_report(openweathermap.service, location, secrets['openweathermap'])
    print(report)

