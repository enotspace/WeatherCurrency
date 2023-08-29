from flask import Flask, render_template, url_for, request, redirect
from translate import Translator
import requests
import datetime

week = ["ПН", "ВТ", 'СР', 'ЧТ', 'ПТ', 'СБ', 'НД']
today = datetime.datetime.now()
textToSmile={"кілька хмар":"🌤️", "чисте небо":"☀️", "уривчасті хмари":"☁️", "легкий дощ":"🌧️", "рвані хмари":"🌥️"}

def translate(text, from_lang, to_lang):
    Language={'English':"en", 'Ukrainian':"uk"}
    print(from_lang)
    translator= Translator(from_lang=Language[from_lang], to_lang=Language[to_lang])
    return translator.translate(text)

def get_weather(s_city="Київ"):
    appid = "c4bb700a457b50d5c8702a4cb696837b"
    
    res = requests.get("http://api.openweathermap.org/data/2.5/find",
                 params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
    data = res.json()

    city_id = data['list'][0]['id']

    res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                        params={'id': city_id, 'units': 'metric', 'lang': 'ua', 'APPID': appid})
    data = res.json()
    list_for_week = []
    temperature = 0
    for i in data['list']:
        temperature = int(i['main']['temp'])
        weather = i['weather'][0]['description']
        if i['dt_txt'][12] != '2': continue
        try: weather = textToSmile[weather]
        except: ...
        list_for_week.append((weather, temperature))
    return list_for_week

app = Flask(__name__)

@app.route('/')
def index_page():
    return render_template("index.html")

@app.route('/translator', methods=['GET', 'POST'])
def translator_page():
    if request.method == "POST":
        output= request.form['text']
        from_lang=request.form['from_language']
        to_lang=request.form['to_language']
        return render_template("translator.html", input=output, output=translate(output, from_lang, to_lang))
    return render_template("translator.html")

@app.route('/weather', methods=['GET', 'POST'])
def weather_page():
    will_weather = []
    city = "Київ"
    for i in range(7):
        day_index = int(today.strftime("%w"))+i
        if day_index > 7: day_index-=7
        will_weather.append(week[day_index-1])
    if request.method == "POST":
        city = request.form['city']
    return render_template("weather.html", seven_days=will_weather, weather=get_weather(city), City=city)

if __name__ == '__main__':
    app.run()