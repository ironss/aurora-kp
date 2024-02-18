# Weather forecast processing for OpenWeatherMap

import json
import datetime
import math

import weather


debug = False

def _parse(forecast_text):
    forecast_owm = json.loads(forecast_text)
    if debug:
        print(forecast_owm)

    reports = []
    for fc in forecast_owm['list']:
        report = weather.Weather_report(
            datetime.datetime.fromtimestamp(fc['dt'], tz=datetime.timezone.utc),
            fc['weather'][0]['main'],
            fc['weather'][0]['id'],
            fc['weather'][0]['icon'],
            fc['main']['temp'],
            fc['main']['pressure'],
            fc['wind']['speed'],
            fc['wind']['gust'] if 'gust' in fc['wind'] else None,
            fc['wind']['deg'],
            math.cos(math.radians(90-fc['wind']['deg'])),
            math.sin(math.radians(90-fc['wind']['deg'])),
            None,  # rain
            fc['rain']['3h'] / 3 if 'rain' in fc else 0,  # rain 1h
            #None,  # rain 3h
            #None,  # rain 24h
            fc['main']['humidity'],
            fc['clouds']['all'],
            fc['visibility'],
        )
        print(report)
        reports.append(report)
    return reports

service = {
    'name': 'OpenWeatherMap',
    'url_base': 'https://api.openweathermap.org/data/2.5/forecast',
    'url_params': {
        'appid': '{api_key}',
        'lat': '{lat}',
        'lon': '{lon}',
        'units': 'metric',
    },
    'url_headers': {
    },
    'handler': _parse,
}


if __name__ == '__main__':
    import json
    import weather

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

    debug = True
    for loc in locations:
        location = { k: loc[i] for i, k in enumerate(['name', 'lat', 'lon', 'alt']) }
        print(location)

        forecasts = weather.load(service, location, secrets['openweathermap'])
        print(forecasts)
        print()


