from settings import *
from databases import *

@app.route('/')
def index_page():
    return render_template("index.html")
@app.route('/create-article', methods=['GET', 'POST'])
def create_article_page():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']

        if title=='' or text=='' or len(title) > 30:
            return redirect('/create-article')

        article = Article(title = title, text = text)

        db.session.add(article)
        db.session.commit()
        return redirect('/posts')
    return render_template("create-article.html")
@app.route('/posts')
def posts_page():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)

@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)

@app.route('/del-post/<int:id>')
def post_delete(id):
    article = Article.query.get(id)
    db.session.delete(article)
    db.session.commit()

    return redirect('/posts')

@app.route('/currency', methods=['GET', 'POST'])
def currency_page():
    return render_template("currency.html", currencies=list(currencies.values()),currencies_icons=list(currencies.keys()))
@app.route('/translator', methods=['GET', 'POST'])
def translator_page():
    if request.method == "POST":
        return render_template("translator.html", input=request.form['text'], output=translate(request.form['text'], request.form['from_language'], request.form['to_language']))
    return render_template("translator.html")
@app.route('/weather', methods=['GET', 'POST'])
def weather_page():
    will_weather = []
    city = "Київ"
    for i in range(7):
        day_index = int(today.strftime("%w"))+i
        if day_index > 7: day_index-=7
        will_weather.append(week[day_index-1])
    return render_template("weather.html", seven_days=will_weather, weather=get_weather(city), City=city)

# with app.app_context():
#     db.create_all()
if __name__ == '__main__':
    app.run(debug=True)