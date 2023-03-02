"""
Weather service file for OpenWeatherMap
"""

import json
import datetime

import weather

def _parse(report_text):
    report_owm = json.loads(report_text)
    report = weather.Weather_report(
        datetime.datetime.fromtimestamp(report_owm['dt'], tz=datetime.timezone.utc),
        report_owm['weather'][0]['main'],
        report_owm['weather'][0]['id'],
        report_owm['weather'][0]['icon'],
        report_owm['main']['temp'],
        report_owm['main']['pressure'],
        report_owm['wind']['speed'],
        report_owm['wind']['deg'],
        None,
        report_owm['main']['humidity'],
        report_owm['clouds']['all'],
        report_owm['visibility'],
    )
    return report

_location_params = [
    'name',
    'lat',
    'lon',
    'alt',
]

service = {
    'name': 'OpenWeatherMap',
    'url_base': 'https://api.openweathermap.org/data/2.5/weather',
    'url_params': {
        'appid': '{api_key}',
        'lat': '{lat}',
        'lon': '{lon}',
        'units': 'metric',
    },
    'url_headers': {
    },
    'handler': _parse,
    'location': lambda l: { n: l[i] for i, n in enumerate(_location_params) }
}


if __name__ == '__main__':
    import json
    import weather

    secrets_fn = 'secrets.json'
    with open(secrets_fn) as f:
        secrets = json.load(f)
        
    location = ( 'Christchurch Airport', -43.4821, 172.5500, 30 )
    
    report = weather.load_report(service, location, secrets['openweathermap'])
    print(report)

