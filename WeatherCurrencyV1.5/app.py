from settings import *

app = Flask(__name__)

currencies = {'$':"USD", "€":"EUR"}

@app.route('/')
def index_page():
    return render_template("index.html")

@app.route('/currency', methods=['GET', 'POST'])
def currency_page():
    return render_template("currency.html", currencies=list(currencies.values()),currencies_icons=list(currencies.keys()))

@app.route('/convert', methods=['POST'])
def convert():
    from_currency = currencies[request.form['from']]
    to_currency = currencies[request.form['to']]
    amount = float(request.form['input_num'])
    
    output= currency.convert(amount, from_currency, to_currency)
    output = round(output, 2)
    return jsonify(result=output)

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