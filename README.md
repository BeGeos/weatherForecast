# Weather Forecast and Current
The app is quite straightforward. The first part deals with user prompt for the name of a city.
Secondly, it fetches results from a database, compiled from a json file with the entire list of cities, with IDs, lat and lon, name etc.
It triggers 2 functions: get_weather_now and get_weather_forecast, which in turn yields the information that are later plotted onto the final .png image. 
I have done quite a lot of error handling, especially to reduce ambiguity in the city's name as well as no input. 

There are easier way to do it but this is a rough version .0.0 that constitutes the base for future improvement.
