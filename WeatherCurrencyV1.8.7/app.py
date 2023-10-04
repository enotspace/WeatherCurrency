from settings import *
from databases import *
 
@app.route('/ip/')
def get_user_ip():
    ip = request.headers.get('X-Real-IP')
    return ip

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

@app.route('/del-post/<int:id>', methods=['GET', 'POST'])
def post_delete(id):
    if request.method == "POST":
        if request.form['password'] == '1234':
            article = Article.query.get(id)
            db.session.delete(article)
            db.session.commit()
            return redirect('/posts')

    return render_template("post_del.html")


@app.route('/currency', methods=['GET', 'POST'])
def currency_page():
    return render_template("currency.html", currencies=currencies)
@app.route('/translator', methods=['GET', 'POST'])
def translator_page():
    return render_template("translator.html")
@app.route('/weather', methods=['GET', 'POST'])
def weather_page():
    will_weather = []
    try: city = requests.get(f"http://ip-api.com/json/{get_user_ip()}?lang=uk").json()['city']
    except: city = "Polonne"
    if request.method == 'POST':
        city = request.form['city']
    for i in range(7):
        day_index = int(today.strftime("%w"))+i
        if day_index > 7: day_index-=7
        will_weather.append(week[day_index-1])
    return render_template("weather.html", seven_days=will_weather, weather=get_weather(city), City=city)

# with app.app_context():
#     db.create_all()
if __name__ == '__main__':
    app.run(debug=True)