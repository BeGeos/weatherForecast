
import requests
import json
import datetime

lat = '55.952061'
lon = '-3.19648'
appid ='b7adec848b0680cb9a2518e37b256861'
url = 'https://api.openweathermap.org/data/2.5/onecall?'
payload = {'lat': lat, 'lon': lon, 'exclude': 'minutely', 'appid': appid}
uh = requests.get(url, params=payload)
fh = uh.json()
# data = json.dumps(fh, indent=2)
# print(data)
description = fh['current']['weather'][0]['description'].title()
current_temp = fh['current']['temp']
current_temp_Celsius = int(current_temp - 273.73)
current_humidity = fh['current']['humidity']
current_clouds = fh['current']['clouds']
uvi = fh['current']['uvi']

tempC, humidity, clouds, times, rain = [], [], [], [], []
n = 0
for i in enumerate(fh['hourly']):
    tK = fh['hourly'][n]['temp']
    tC = int(tK - 273.73)
    tempC.append(tC)
    humidity.append(fh['hourly'][n]['humidity'])
    clouds.append(fh['hourly'][n]['clouds'])
    unix_dt = fh['hourly'][n]['dt']
    hour = datetime.datetime.fromtimestamp(unix_dt).strftime('%H')
    times.append(hour)
    if int(fh['hourly'][n]['pop']) != 0:
        rain.append(fh['hourly'][0]['rain']['1h'])
    n += 1




