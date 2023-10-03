from flask import Flask, render_template, request, flash, get_flashed_messages, jsonify, redirect
from currency_converter import CurrencyConverter
from translate import Translator
import datetime, requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

currencies = {'CNY', 'USD', 'SEK', 'JPY', 'GBP', 'ISK', 'PHP', 'EEK', 'MXN', 'IDR', 'ZAR', 'RON', 'BGN', 'CHF', 'LVL', 'PLN', 'CZK', 'SGD', 'EUR', 'KRW', 'SKK', 'ROL', 'NZD', 'NOK', 'MYR', 'SIT', 'CAD', 'UAH', 'ILS', 'HRK', 'LTL', 'TRY', 'INR', 'HKD', 'TRL', 'THB', 'CYP', 'MTL', 'AUD', 'BRL', 'HUF', 'DKK'}
week = ["ПН", "ВТ", 'СР', 'ЧТ', 'ПТ', 'СБ', 'НД']
today = datetime.datetime.now()
currency = CurrencyConverter()
textToSmile={"кілька хмар":"🌤️", "чисте небо":"☀️", "уривчасті хмари":"☁️", "легкий дощ":"🌧️", "рвані хмари":"🌥️", "хмарно":"🌫️"}


def translate(text, from_lang, to_lang):
    Language={'Afar':"aa", 'Abkhazian':"ab", 'Avestan':"ae", 'Afrikaans':"af", 'Akan':"ak", 'Amharic':"am", 'Aragonese':"an", 'Arabic':"ar", 'Assamese':"as", 'Avaric':"av", 'Aymara':"ay", 'Azerbaijani':"az", 'Bashkir':"ba", 'Bulgarian':"bg", 'Bihari':"bh", 'Bislama':"bi", 'Bambara':"bm", 'Bengali':"bn", 'Tibetan':"bo", 'Breton':"br", 'Bosnian':"bs", 'Catalan':"ca", 'Chechen':"ce", 'Chamorro':"ch", 'Corsican':"co", 'Cree':"cr", 'Czech':"cs", "Church Slavic":"cu", 'Chuvash':"cv", 'Welsh':"cy", 'Danish':"da", 'German':"de", 'Divehi':"dv", 'Dzongkha':"dz", 'Ewe':"ee", 'Greek':"el", 'English':"en", 'Esperanto':"eo", 'Spanis':"es", 'Estonia':"et", 'Basqu':"eu", 'Persian':"fa", 'Fulah':"ff", 'Finnish':"fi", 'Fijian':"fj", 'Faroese':"fo", 'French':"fr", "Western Frisian":"fy", 'Irish':"ga", 'Gaelic':"gd", 'Galician':"gl", 'Guaraní':"gn", 'Gujarati':"gu", 'Manx':"gv", 'Hausa':"ha", 'Hebrew':"he", 'Hindi':"hi", "Hiri Motu":"ho", 'Croatian':"hr", 'Haitian':"ht", 'Hungarian':"hu", 'Armenian':"hy", 'Herero':"hz", 'Interlingua':"ia", 'Indonesian':"id", 'Interlingue':"ie", 'Igbo':"ig", "Sichuan Yi":"ii", 'Inupiaq':"ik", 'Ido':"io", 'Icelandic':"is", 'Italian':"it", 'Inuktitut':"iu", 'Japanese':"ja", 'Javanese':"jv", 'Georgian':"ka", 'Kongo':"kg", 'Kikuyu':"ki", 'Kuanyama':"kj", 'Kazakh':"kk", 'Kalaallisut':"kl", 'Khmer':"km", 'Kannada':"kn", 'Korean':"ko", 'Kanuri':"kr", 'Kashmiri':"ks", 'Kurdish':"ku", 'Komi':"kv", 'Cornish':"kw", 'Kirghiz':"ky", 'Latin':"la", 'Luxembourgish':"lb", 'Ganda':"lg", 'Limburgish':"li", 'Lingala':"ln", 'Lao':"lo", 'Lithuanian':"lt", "Luba-Katanga":"lu", 'Latvian':"lv", 'Malagasy':"mg", 'Marshallese':"mh", 'Māori':"mi", 'Macedonian':"mk", 'Malayalam':"ml", 'Mongolian':"mn", 'Moldavian':"mo", 'Marathi':"mr", 'Malay':"ms", 'Maltese':"mt", 'Burmese':"my", 'Nauru':"na", "Norwegian Bokmål":"nb", "North Ndebele":"nd", 'Nepali':"ne", 'Ndonga':"ng", 'Dutch':"nl", "Norwegian Nynorsk":"nn", 'Norwegian':"no", "South Ndebele":"nr", 'Navajo':"nv", 'Chichewa':"ny", 'Occitan':"oc", 'Ojibwa':"oj", 'Oromo':"om", 'Oriya':"or", 'Ossetian':"os", 'Panjabi':"pa", 'Pāli':"pi", 'Polish':"pl", 'Pashto':"ps", 'Portuguese':"pt", 'Quechua':"qu", "Raeto-Romance":"rm", 'Kirundi':"rn", 'Romanian':"ro", 'Kinyarwanda':"rw", 'Sanskrit':"sa", 'Sardinian':"sc", 'Sindhi':"sd", "Northern Sami":"se", 'Sango':"sg", "Serbo-Croatian":"sh", 'Sinhala':"si", 'Slovak':"sk", 'Slovenian':"sl", 'Samoan':"sm", 'Shona':"sn", 'Somali':"so", 'Albanian':"sq", 'Serbian':"sr", 'Swati':"ss", "Southern Sotho":"st", 'Sundanese':"su", 'Swedish':"sv", 'Swahili':"sw", 'Tamil':"ta", 'Telugu':"te", 'Tajik':"tg", 'Thai':"th", 'Tigrinya':"ti", 'Turkmen':"tk", 'Tagalog':"tl", 'Tswana':"tn", 'Tonga':"to", 'Turkish':"tr", 'Tsonga':"ts", 'Tatar':"tt", 'Twi':"tw", 'Tahitian':"ty", 'Uighur':"ug", 'Ukrainian':"uk", 'Urdu':"ur", 'Uzbek':"uz", 'Venda':"ve", 'Vietnamese':"vi", 'Volapük':"vo", 'Walloon':"wa", 'Wolof':"wo", 'Xhosa':"xh", 'Yiddish':"yi", 'Yoruba':"yo", 'Zhuang':"za", 'Chinese':"zh", 'Zulu':"zu"}
    translator= Translator(from_lang=Language[from_lang], to_lang=Language[to_lang])
    return translator.translate(text)
@app.route('/convert', methods=['POST'])
def convert():
    from_currency = request.form['from']
    to_currency = request.form['to']
    amount = float(request.form['input_num'])

    uah = 36.66
    
    if from_currency == "UAH":
        output= currency.convert(amount, "USD", to_currency) / uah
    elif to_currency == "UAH":
        output= currency.convert(amount, from_currency, "USD") * uah
    else: output= currency.convert(amount, from_currency, to_currency)
    output = round(output, 2)
    return jsonify(result=output)
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
        list_for_week.append((weather, temperature, f'{i["wind"]["speed"]} м/с'))
    return list_for_week