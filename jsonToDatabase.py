import json
import sqlite3

conn = sqlite3.connect('weatherAPI_jsondb.sqlite')
cur = conn.cursor()

cur.executescript('''

DROP TABLE IF EXISTS Cities;
DROP TABLE IF EXISTS Coordinates;

CREATE TABLE Cities (
    id INTEGER NOT NULL PRIMARY KEY UNIQUE,
    name TEXT,
    state TEXT,
    country TEXT
);

CREATE TABLE Coordinates (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    city_id INTEGER,
    lat FLOAT,
    lon FLOAT
);
''')

# Opening of the json file about cities and their information
with open('city.list.json') as json_file:
    data = json.load(json_file)

for entry in data:
    id = int(entry['id'])
    name = entry['name']
    state = entry['state']
    country = entry['country']
    lat = entry['coord']['lat']
    lon = entry['coord']['lon']

    cur.execute('''
    INSERT INTO Cities (id, name, state, country) 
    VALUES (?,?,?,?)''', (id, name, state, country))
    cur.execute('''
    SELECT id FROM Cities WHERE name = ?''', (name,))
    city_id = cur.fetchone()[0]

    cur.execute('''
    INSERT INTO Coordinates (city_id,lat, lon) 
    VALUES (?, ?, ?)''', (city_id, lat, lon))

    conn.commit()





