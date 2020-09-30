import requests
import sqlite3
import datetime
import matplotlib.pyplot as plt
import matplotlib
import time

# Fetching data from database instead of from json file from user input
conn = sqlite3.connect('weatherAPI_jsondb.sqlite')
cur = conn.cursor()

city = input('Enter city name: ').title()

cur.execute('SELECT id, name, state, country FROM Cities WHERE name = ?', (city,))
output = cur.fetchall()
# If return is one value then it goes on
if len(output) == 1:
    city_id = output[0][0]
    cur.execute('SELECT lat, lon FROM Coordinates WHERE city_id = ?', (city_id,))
    coordinates = cur.fetchone()

# In case it doesn't return anything, city not found or misspelled
elif len(output) == 0:
    print(city, 'cannot be found')
    quit()
# If search yields more than one result
else:
    print('Please, make a selection, by number ')
    for row in output:
        if len(row[2]) != 0:
            print(row[1:])
        else:
            print("('{}', '{}')".format(row[1], row[3]))

    inp = input()
    iinp = int(inp)
    city_id = output[iinp - 1][0]
    cur.execute('SELECT lat, lon FROM Coordinates WHERE city_id = ?', (city_id,))
    coordinates = cur.fetchone()

# print(coordinates)

def KtoC(temp):
    tC = temp - 273.73
    return int(tC)


def get_weather_now(coordinates):
    lat = coordinates[0]
    lon = coordinates[1]
    appid = 'b7adec848b0680cb9a2518e37b256861'
    url = 'https://api.openweathermap.org/data/2.5/onecall?'
    payload = {'lat': lat, 'lon': lon, 'exclude': 'minutely', 'appid': appid}
    uh = requests.get(url, params=payload)
    if uh.status_code != 200:
        print(uh.status_code)
        quit()
    else:
        fh = uh.json()
        # data = json.dumps(fh, indent=2)
        # print(data)

    description = fh['current']['weather'][0]['description'].title()
    current_temp = fh['current']['temp']
    current_temp_Celsius = KtoC(current_temp)
    current_humidity = fh['current']['humidity']
    current_clouds = fh['current']['clouds']
    uvi = fh['current']['uvi']

    return description, current_temp_Celsius, current_humidity, current_clouds, uvi


def get_weather_forecast(coordinates):
    lat = coordinates[0]
    lon = coordinates[1]
    appid = 'b7adec848b0680cb9a2518e37b256861'
    url = 'https://api.openweathermap.org/data/2.5/onecall?'
    payload = {'lat': lat, 'lon': lon, 'exclude': 'minutely', 'appid': appid}
    uh = requests.get(url, params=payload)
    if uh.status_code != 200:
        print(uh.status_code)
        quit()
    else:
        fh = uh.json()

    tempC, humidity, clouds, times, rain = [], [], [], [], []
    n = 0
    for i in range(len(fh['hourly'])):
        tK = fh['hourly'][n]['temp']
        tC = KtoC(tK)
        tempC.append(tC)
        humidity.append(fh['hourly'][n]['humidity'])
        clouds.append(fh['hourly'][n]['clouds'])
        unix_dt = fh['hourly'][n]['dt']
        hour = datetime.datetime.fromtimestamp(unix_dt).strftime('%H')
        times.append(hour)
        if int(fh['hourly'][n]['pop']) != 0:
            try:
                rain.append(fh['hourly'][0]['rain']['1h'])
            except:
                pass
        n += 1
    return tempC, humidity, clouds, times, rain


# start1 = time.time()
current = get_weather_now(coordinates)
# end1 = time.time()
# delta1 = end1 - start1
# print('Done current in {} sec'.format(delta1))
# start2 = time.time()
forecast = get_weather_forecast(coordinates)
# end2 = time.time()
# delta2 = end2 - start2
# print('Done forecast in {} sec'.format(delta2))

# print('{}, {} °C , humidity {}%, cloudiness {}%'.format(city, current[1], current[2], current[3]))
# print(current[0], 'UVI:', current[4])

if len(forecast[4]) != 0:
    rain_perc = str(int(forecast[4][0] * 100)) + ' %'
else:
    rain_perc = '0 %'

suptitle = city + ', ' + str(current[1]) + '°C' + ', ' + current[0] + '\n' + 'humidity: ' + str(current[2]) + '%'\
           + ' cloudiness: ' + str(current[3]) + '% \n' + 'UVI ' + str(current[4]) + ', rain: ' + rain_perc

figure = plt.figure(figsize=(15, 8))

matplotlib.rc('xtick', labelsize=7)
matplotlib.rc('ytick', labelsize=10)
plt.suptitle(suptitle)
plt.subplot(221)
plt.bar(forecast[3], forecast[0])
plt.xlabel('hour')
plt.ylabel('temperature in °C')
matplotlib.rc('xtick', labelsize=7)
matplotlib.rc('ytick', labelsize=10)
plt.subplot(223)
plt.bar(forecast[3], forecast[1], color='m')
plt.xlabel('hour')
plt.ylabel('humidity in %')
matplotlib.rc('xtick', labelsize=7)
matplotlib.rc('ytick', labelsize=10)
plt.subplot(222)
plt.bar(forecast[3], forecast[2], color='g')
plt.xlabel('hour')
plt.ylabel('cloudiness in %')
plt.tight_layout(h_pad=2, w_pad=3)
plt.show()
