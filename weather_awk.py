#
# Weather service for Apple WeatherKit
#
# * TODO: auth_token is a JWT which could be calculated from first principles. At present, it has been
#   pre-created with a 400-day lifetime.
#

import json
import datetime
import math

import weather


debug = False

def _parse(report_text):
    report_raw = json.loads(report_text)
    if debug:
        print(report_raw)

    report = weather.Weather_report(
        datetime.datetime.strptime(report_raw['currentWeather']['asOf'], '%Y-%m-%dT%H:%M:%S%z'),
        None,  # summary
        None,  # code
        None,  # icon
        report_raw['currentWeather']['temperature'],
        report_raw['currentWeather']['pressure'],
        report_raw['currentWeather']['windSpeed'] * 0.278,  # Reported as km/h, but stored as m/s
        report_raw['currentWeather']['windGust'] * 0.278,
        report_raw['currentWeather']['windDirection'],
        math.cos(math.radians(90-report_raw['currentWeather']['windDirection'])),
        math.sin(math.radians(90-report_raw['currentWeather']['windDirection'])),
        report_raw['currentWeather']['precipitationIntensity'],
        None,  # rain 1h
        None,  # rain 3h
        None,  # rain 24h
        report_raw['currentWeather']['humidity'] * 100,
        report_raw['currentWeather']['cloudCover'] * 100,
        report_raw['currentWeather']['visibility'],
    )
    return report

service = {
    'name': 'Apple WeatherKit',
    'url_base': 'https://weatherkit.apple.com/api/v1/weather/en_NZ/{lat}/{lon}',
    'url_params': {
        'dataSets': 'currentWeather',
    },
    'url_headers': {
        'Authorization': 'Bearer {auth_token}',
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

        report = weather.load_report(service, location, secrets['weatherkit'])
        print(report)
        print()

