import requests
s_city = ""
appid = "c4bb700a457b50d5c8702a4cb696837b"

res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                    params={'id': 703448, 'units': 'metric', 'lang': 'ua', 'APPID': appid})
data = res.json()
list_for_week = []
for i in data['list']:
    weather = (i['dt_txt'] + f" {int(i['main']['temp'])}  {i['weather'][0]['description']}")
    if weather[12] != '2': continue
    list_for_week.append(weather)
print(list_for_week)